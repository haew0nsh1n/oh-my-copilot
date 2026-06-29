"""Small stdlib WebSocket client for text messages."""

import base64
import hashlib
import os
import socket
import ssl
import struct
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class WebSocketTarget:
    """Parsed WebSocket target."""

    secure: bool
    host: str
    port: int
    resource: str


class WebSocketClient:
    """Minimal RFC 6455 client for text-message workflows."""

    def __init__(self, url: str, timeout: float = 10.0):
        self.url = url
        self.timeout = timeout
        self.target = self.parse_target(url)
        self.socket: socket.socket | None = None

    @staticmethod
    def parse_target(url: str) -> WebSocketTarget:
        parsed = urlparse(url)
        if parsed.scheme not in {"ws", "wss"}:
            raise ValueError("WebSocket URL must use ws:// or wss://")
        if not parsed.hostname:
            raise ValueError("WebSocket URL must include a host")
        secure = parsed.scheme == "wss"
        port = parsed.port or (443 if secure else 80)
        resource = parsed.path or "/"
        if parsed.query:
            resource = f"{resource}?{parsed.query}"
        return WebSocketTarget(secure=secure, host=parsed.hostname, port=port, resource=resource)

    def connect(self) -> None:
        raw_socket = socket.create_connection((self.target.host, self.target.port), self.timeout)
        raw_socket.settimeout(self.timeout)
        if self.target.secure:
            context = ssl.create_default_context()
            raw_socket = context.wrap_socket(raw_socket, server_hostname=self.target.host)

        key = base64.b64encode(os.urandom(16)).decode("ascii")
        host_header = self.target.host
        if self.target.port not in {80, 443}:
            host_header = f"{self.target.host}:{self.target.port}"
        request = (
            f"GET {self.target.resource} HTTP/1.1\r\n"
            f"Host: {host_header}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        raw_socket.sendall(request.encode("ascii"))
        response = self._recv_until(raw_socket, b"\r\n\r\n")
        if b" 101 " not in response.split(b"\r\n", 1)[0]:
            raise ConnectionError(response.decode("latin1", errors="replace"))

        expected_accept = base64.b64encode(
            hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest()
        ).decode("ascii")
        if f"sec-websocket-accept: {expected_accept}".lower() not in response.decode(
            "latin1", errors="replace"
        ).lower():
            raise ConnectionError("WebSocket handshake accept header did not match")
        self.socket = raw_socket

    def send_text(self, message: str) -> None:
        if self.socket is None:
            raise ConnectionError("WebSocket is not connected")
        self.socket.sendall(self.build_client_frame(message.encode("utf-8"), opcode=0x1))

    def receive_text(self) -> str:
        if self.socket is None:
            raise ConnectionError("WebSocket is not connected")
        opcode, payload = self._receive_frame()
        if opcode == 0x8:
            self.close()
            raise ConnectionError("WebSocket closed by peer")
        if opcode != 0x1:
            raise ValueError(f"Expected text frame, received opcode {opcode}")
        return payload.decode("utf-8")

    def close(self) -> None:
        if self.socket is None:
            return
        try:
            self.socket.sendall(self.build_client_frame(b"", opcode=0x8))
        finally:
            self.socket.close()
            self.socket = None

    @staticmethod
    def build_client_frame(payload: bytes, opcode: int = 0x1) -> bytes:
        first_byte = 0x80 | opcode
        length = len(payload)
        if length < 126:
            header = struct.pack("!BB", first_byte, 0x80 | length)
        elif length < 65536:
            header = struct.pack("!BBH", first_byte, 0x80 | 126, length)
        else:
            header = struct.pack("!BBQ", first_byte, 0x80 | 127, length)
        mask = os.urandom(4)
        masked = bytes(payload[index] ^ mask[index % 4] for index in range(length))
        return header + mask + masked

    def _receive_frame(self) -> tuple[int, bytes]:
        header = self._recv_exact(2)
        first_byte, second_byte = header
        opcode = first_byte & 0x0F
        masked = bool(second_byte & 0x80)
        length = second_byte & 0x7F
        if length == 126:
            length = struct.unpack("!H", self._recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._recv_exact(8))[0]
        mask = self._recv_exact(4) if masked else b""
        payload = self._recv_exact(length)
        if masked:
            payload = bytes(payload[index] ^ mask[index % 4] for index in range(length))
        return opcode, payload

    def _recv_exact(self, size: int) -> bytes:
        assert self.socket is not None
        chunks: list[bytes] = []
        remaining = size
        while remaining:
            chunk = self.socket.recv(remaining)
            if not chunk:
                raise ConnectionError("Socket closed while reading WebSocket frame")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)

    @staticmethod
    def _recv_until(active_socket: socket.socket, delimiter: bytes) -> bytes:
        buffer = bytearray()
        while delimiter not in buffer:
            chunk = active_socket.recv(4096)
            if not chunk:
                raise ConnectionError("Socket closed during WebSocket handshake")
            buffer.extend(chunk)
        return bytes(buffer)

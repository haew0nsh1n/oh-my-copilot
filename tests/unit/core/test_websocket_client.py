"""Tests for the stdlib WebSocket client."""

import pytest

from core.websocket_client import WebSocketClient


class TestWebSocketClient:
    """Test WebSocket URL parsing and client frame construction."""

    def test_parse_ws_target(self):
        target = WebSocketClient.parse_target("ws://example.com/chat?room=1")

        assert target.secure is False
        assert target.host == "example.com"
        assert target.port == 80
        assert target.resource == "/chat?room=1"

    def test_parse_wss_target_with_port(self):
        target = WebSocketClient.parse_target("wss://example.com:8443/socket")

        assert target.secure is True
        assert target.port == 8443
        assert target.resource == "/socket"

    def test_rejects_non_websocket_scheme(self):
        with pytest.raises(ValueError, match="ws:// or wss://"):
            WebSocketClient.parse_target("https://example.com/socket")

    def test_build_client_text_frame_masks_payload(self):
        frame = WebSocketClient.build_client_frame(b"hello")

        assert frame[0] == 0x81
        assert frame[1] & 0x80
        assert frame[1] & 0x7F == 5
        assert len(frame) == 11
        assert frame[-5:] != b"hello"

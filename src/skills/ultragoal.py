"""Ultragoal skill for durable multi-goal execution."""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import List
from domain import (
    Ultragoal,
    Goal,
    GoalCheckpoint,
    UltragoalArtifact,
    UltragoalReport,
    GoalStatus,
    GoalPriority,
)


class UltragoalSkill:
    """
    A skill for durable multi-goal execution.
    
    This skill turns an approved plan into sequential goals with checkpoints
    and progress tracking.
    """
    
    def __init__(self):
        """Initialize the ultragoal skill."""
        self.name = "ultragoal"
        self.description = "Turn approved plans into durable multi-goal execution with checkpoints"
    
    def create_ultragoal(
        self,
        name: str,
        description: str,
        metadata: dict = None
    ) -> Ultragoal:
        """
        Create a new ultragoal.
        
        Args:
            name: Name of the ultragoal
            description: Description of what it achieves
            metadata: Optional metadata (plan info, context, etc.)
            
        Returns:
            A new Ultragoal
        """
        return Ultragoal(
            name=name,
            description=description,
            metadata=metadata or {}
        )

    def create_artifact_only_ultragoal(self, brief: str, metadata: dict = None) -> Ultragoal:
        """Create the default artifact-only OMC-style ultragoal ledger."""
        task = brief.strip()
        ultragoal = self.create_ultragoal(
            task,
            f"Artifact-only execution ledger for: {task}",
            metadata=metadata or {},
        )
        goals = [
            self.create_goal(
                "Clarify acceptance criteria",
                "Capture the user-visible outcome, boundaries, and verification evidence.",
                priority=GoalPriority.HIGH,
                criteria=[
                    "Brief is recorded",
                    "Acceptance criteria are explicit",
                    "Verification command or evidence path is identified",
                ],
            ),
            self.create_goal(
                "Execute implementation work",
                "Carry out the requested change or hand off to the active execution loop.",
                priority=GoalPriority.HIGH,
                criteria=[
                    "Implementation owner is clear",
                    "Changed files or handoff target are recorded",
                    "No competing active loop owns the same work",
                ],
            ),
            self.create_goal(
                "Verify and report completion",
                "Record the validation evidence required before treating the goal as complete.",
                priority=GoalPriority.HIGH,
                criteria=[
                    "Executable validation evidence is attached",
                    "Remaining blockers are recorded",
                    "Completion report is available",
                ],
            ),
        ]
        for goal in goals:
            self.add_checkpoint(
                goal,
                self.create_checkpoint("Evidence recorded", "Attach command output, review notes, or artifact paths."),
            )
            self.add_goal(ultragoal, goal)
        return ultragoal

    def auto_plan_id(self, brief: str, timestamp: datetime = None) -> str:
        """Create an OMC-style epoch-plus-slug plan id."""
        now = timestamp or datetime.now()
        slug = re.sub(r"[^0-9A-Za-z가-힣_-]+", "-", brief.strip()).strip("-").lower()
        if not slug:
            slug = "ultragoal"
        return f"{int(now.timestamp() * 1000)}-{slug[:48]}"

    def save_artifacts(
        self,
        ultragoal: Ultragoal,
        state_root: Path | str,
        plan_id: str = "",
    ) -> UltragoalArtifact:
        """Persist brief, goals, and ledger artifacts under the OMP state root."""
        root = Path(state_root)
        artifact_root = root / "ultragoal"
        if plan_id:
            artifact_root = artifact_root / "plans" / plan_id
        artifact_root.mkdir(parents=True, exist_ok=True)

        brief_path = artifact_root / "brief.md"
        goals_path = artifact_root / "goals.json"
        ledger_path = artifact_root / "ledger.jsonl"

        brief_path.write_text(
            f"# {ultragoal.name}\n\n{ultragoal.description}\n",
            encoding="utf-8",
        )
        goals_path.write_text(
            json.dumps(self._to_json(ultragoal), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        ledger_path.write_text(
            json.dumps(
                {
                    "event": "created",
                    "status": ultragoal.status.value,
                    "goal_count": len(ultragoal.goals),
                    "created_at": ultragoal.created_at.isoformat(),
                    "plan_id": plan_id,
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        return UltragoalArtifact(
            root=artifact_root,
            brief_path=brief_path,
            goals_path=goals_path,
            ledger_path=ledger_path,
            plan_id=plan_id,
        )

    def materialize_builtin_implementation(
        self,
        brief: str,
        project_root: Path | str,
    ) -> list[Path]:
        """Materialize a small built-in implementation for supported demo goals."""
        normalized = brief.lower()
        if "websocket" not in normalized and "web socket" not in normalized and "웹소켓" not in brief:
            raise ValueError("No built-in ultragoal executor is available for this brief")

        root = Path(project_root)
        client_path = root / "src" / "core" / "websocket_client.py"
        test_path = root / "tests" / "unit" / "core" / "test_websocket_client.py"
        client_path.parent.mkdir(parents=True, exist_ok=True)
        test_path.parent.mkdir(parents=True, exist_ok=True)
        client_path.write_text(WEBSOCKET_CLIENT_TEMPLATE, encoding="utf-8")
        test_path.write_text(WEBSOCKET_CLIENT_TEST_TEMPLATE, encoding="utf-8")
        return [client_path, test_path]

    def record_goal_status(
        self,
        artifact_root: Path | str,
        goal_title: str,
        status: GoalStatus,
        evidence_paths: list[Path] = None,
    ) -> None:
        """Update a goal status in goals.json and append a ledger event."""
        root = Path(artifact_root)
        goals_path = root / "goals.json"
        ledger_path = root / "ledger.jsonl"
        data = json.loads(goals_path.read_text(encoding="utf-8"))
        now = datetime.now().isoformat()
        for goal in data.get("goals", []):
            if goal.get("title") == goal_title:
                goal["status"] = status.value
                if status == GoalStatus.COMPLETED:
                    goal["completed_at"] = now
                    for checkpoint in goal.get("checkpoints", []):
                        checkpoint["completed"] = True
                        checkpoint["completed_at"] = now
                        checkpoint["verification_notes"] = "Implementation evidence recorded"
                break
        else:
            raise ValueError(f"Goal '{goal_title}' not found")

        goals_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        ledger_path.open("a", encoding="utf-8").write(
            json.dumps(
                {
                    "event": "goal_status_changed",
                    "goal": goal_title,
                    "status": status.value,
                    "evidence_paths": [str(path) for path in evidence_paths or []],
                    "recorded_at": now,
                },
                ensure_ascii=False,
            )
            + "\n"
        )
    
    def create_goal(
        self,
        title: str,
        description: str,
        priority: GoalPriority = GoalPriority.MEDIUM,
        criteria: List[str] = None,
        owner: str = ""
    ) -> Goal:
        """
        Create a goal for an ultragoal.
        
        Args:
            title: Goal title
            description: Goal description
            priority: Goal priority
            criteria: Acceptance criteria
            owner: Goal owner
            
        Returns:
            A new Goal
        """
        goal = Goal(
            title=title,
            description=description,
            priority=priority,
            owner=owner
        )
        
        if criteria:
            for criterion in criteria:
                goal.add_criterion(criterion)
        
        return goal
    
    def add_goal(
        self,
        ultragoal: Ultragoal,
        goal: Goal
    ) -> None:
        """
        Add a goal to an ultragoal.
        
        Args:
            ultragoal: The ultragoal
            goal: The goal to add
        """
        ultragoal.add_goal(goal)
    
    def create_checkpoint(
        self,
        name: str,
        description: str
    ) -> GoalCheckpoint:
        """
        Create a checkpoint for a goal.
        
        Args:
            name: Checkpoint name
            description: Checkpoint description
            
        Returns:
            A new GoalCheckpoint
        """
        return GoalCheckpoint(
            name=name,
            description=description
        )
    
    def add_checkpoint(
        self,
        goal: Goal,
        checkpoint: GoalCheckpoint
    ) -> None:
        """
        Add a checkpoint to a goal.
        
        Args:
            goal: The goal
            checkpoint: The checkpoint to add
        """
        goal.add_checkpoint(checkpoint)
    
    def start_goal(self, goal: Goal) -> None:
        """
        Start working on a goal.
        
        Args:
            goal: The goal to start
        """
        goal.start()
    
    def complete_checkpoint(
        self,
        checkpoint: GoalCheckpoint,
        notes: str = ""
    ) -> None:
        """
        Mark a checkpoint as complete.
        
        Args:
            checkpoint: The checkpoint
            notes: Verification notes
        """
        checkpoint.mark_complete(notes)
    
    def complete_goal(self, goal: Goal) -> None:
        """
        Mark a goal as complete.
        
        Args:
            goal: The goal to complete
        """
        goal.complete()
    
    def block_goal(self, goal: Goal) -> None:
        """
        Mark a goal as blocked.
        
        Args:
            goal: The goal to block
        """
        goal.block()
    
    def fail_goal(self, goal: Goal) -> None:
        """
        Mark a goal as failed.
        
        Args:
            goal: The goal that failed
        """
        goal.fail()
    
    def complete_ultragoal(self, ultragoal: Ultragoal) -> None:
        """
        Mark an ultragoal as complete.
        
        Args:
            ultragoal: The ultragoal to complete
        """
        ultragoal.status = GoalStatus.COMPLETED
        ultragoal.completed_at = __import__('datetime').datetime.now()
    
    def generate_report(self, ultragoal: Ultragoal) -> UltragoalReport:
        """
        Generate a progress report for an ultragoal.
        
        Args:
            ultragoal: The ultragoal
            
        Returns:
            An UltragoalReport
        """
        completed = len(ultragoal.get_completed_goals())
        in_progress = len(ultragoal.get_in_progress_goals())
        pending = len(ultragoal.get_pending_goals())
        blocked = len(ultragoal.get_blocked_goals())
        total = len(ultragoal.goals)
        
        completion_pct = ultragoal.completion_percentage()
        
        summary = f"Ultragoal '{ultragoal.name}': "
        summary += f"{completion_pct:.0f}% complete "
        summary += f"({completed}/{total} goals done)"
        
        if blocked > 0:
            summary += f", {blocked} blocked"
        
        return UltragoalReport(
            ultragoal=ultragoal,
            total_goals=total,
            completed_goals=completed,
            in_progress_goals=in_progress,
            pending_goals=pending,
            blocked_goals=blocked,
            completion_percentage=completion_pct,
            summary=summary
        )

    def _to_json(self, ultragoal: Ultragoal) -> dict:
        return {
            "name": ultragoal.name,
            "description": ultragoal.description,
            "status": ultragoal.status.value,
            "created_at": ultragoal.created_at.isoformat(),
            "completed_at": ultragoal.completed_at.isoformat() if ultragoal.completed_at else None,
            "metadata": ultragoal.metadata,
            "goals": [
                {
                    "title": goal.title,
                    "description": goal.description,
                    "status": goal.status.value,
                    "priority": goal.priority.value,
                    "acceptance_criteria": goal.acceptance_criteria,
                    "depends_on": goal.depends_on,
                    "owner": goal.owner,
                    "created_at": goal.created_at.isoformat(),
                    "started_at": goal.started_at.isoformat() if goal.started_at else None,
                    "completed_at": goal.completed_at.isoformat() if goal.completed_at else None,
                    "checkpoints": [
                        {
                            "name": checkpoint.name,
                            "description": checkpoint.description,
                            "completed": checkpoint.completed,
                            "completed_at": checkpoint.completed_at.isoformat()
                            if checkpoint.completed_at
                            else None,
                            "verification_notes": checkpoint.verification_notes,
                        }
                        for checkpoint in goal.checkpoints
                    ],
                }
                for goal in ultragoal.goals
            ],
        }


WEBSOCKET_CLIENT_TEMPLATE = '''"""Small stdlib WebSocket client for text messages."""

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
            f"GET {self.target.resource} HTTP/1.1\\r\\n"
            f"Host: {host_header}\\r\\n"
            "Upgrade: websocket\\r\\n"
            "Connection: Upgrade\\r\\n"
            f"Sec-WebSocket-Key: {key}\\r\\n"
            "Sec-WebSocket-Version: 13\\r\\n\\r\\n"
        )
        raw_socket.sendall(request.encode("ascii"))
        response = self._recv_until(raw_socket, b"\\r\\n\\r\\n")
        if b" 101 " not in response.split(b"\\r\\n", 1)[0]:
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
'''


WEBSOCKET_CLIENT_TEST_TEMPLATE = '''"""Tests for the stdlib WebSocket client."""

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
'''

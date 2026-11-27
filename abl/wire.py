"""Persistent JSON-over-TCP client for the AbletonMCP Remote Script (default 127.0.0.1:9877)."""

from __future__ import annotations

import json
import os
import socket
from typing import Any, Callable

DEFAULT_HOST = os.environ.get("ABLETON_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("ABLETON_PORT", "9877"))
DEFAULT_TIMEOUT = float(os.environ.get("ABL_TIMEOUT", "15"))
RECV_SIZE = 65536

NOT_RUNNING_MSG = "Live is not running or the AbletonMCP Remote Script is not loaded (nothing listening on {host}:{port})."
TIMEOUT_MSG = "Live did not answer in {timeout:g}s. A modal dialog may be open in Live; press Enter there and retry."
CLOSED_MSG = "Live closed the connection mid-reply. Is Live still running?"


class LiveError(Exception):
    """Base for everything that goes wrong talking to Live."""


class LiveNotRunning(LiveError):
    pass


class LiveTimeout(LiveError):
    pass


class LiveConnectionLost(LiveError):
    def __init__(self, message: str, partial: bool = False):
        super().__init__(message)
        self.partial = partial  # True when Live had started answering
        self.retryable = False  # set by the client: the socket was a reused one


class LiveCommandError(LiveError):
    """Live executed the command and answered with status=error."""


class LiveClient:
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        timeout: float = DEFAULT_TIMEOUT,
        connector: Callable[..., Any] = socket.create_connection,
    ):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._connector = connector
        self._sock: Any = None
        self._fresh = False  # True until the socket has completed one command

    # -- connection -----------------------------------------------------------
    def _ensure_connected(self) -> None:
        if self._sock is not None:
            return
        try:
            self._sock = self._connector((self.host, self.port), self.timeout)
        except (ConnectionRefusedError, OSError) as exc:
            raise LiveNotRunning(NOT_RUNNING_MSG.format(host=self.host, port=self.port)) from exc
        self._fresh = True

    def close(self) -> None:
        if self._sock is not None:
            try:
                self._sock.close()
            finally:
                self._sock = None

    # -- framing --------------------------------------------------------------
    def _receive(self) -> dict:
        chunks: list[bytes] = []
        while True:
            chunk = self._sock.recv(RECV_SIZE)
            if not chunk:
                raise LiveConnectionLost(CLOSED_MSG, partial=bool(chunks))
            chunks.append(chunk)
            if not chunk.rstrip().endswith(b"}"):
                continue
            try:
                return json.loads(b"".join(chunks).decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue

    def send(self, command_type: str, params: dict | None = None) -> Any:
        frame = json.dumps({"type": command_type, "params": params or {}}).encode("utf-8")
        try:
            reply = self._exchange(frame)
        except LiveConnectionLost as exc:
            # A socket that had already served a command and now closes before answering is
            # a stale one left over from a Live restart: reconnect once and resend.
            if exc.partial or not exc.retryable:
                raise
            reply = self._exchange(frame)
        if reply.get("status") == "error":
            raise LiveCommandError(reply.get("message", "unknown error from Live"))
        return reply.get("result", {})

    def _exchange(self, frame: bytes) -> dict:
        self._ensure_connected()
        was_fresh = self._fresh
        try:
            self._sock.settimeout(self.timeout)
            self._sock.sendall(frame)
            reply = self._receive()
        except TimeoutError as exc:
            self.close()
            raise LiveTimeout(TIMEOUT_MSG.format(timeout=self.timeout)) from exc
        except LiveConnectionLost as exc:
            self.close()
            exc.retryable = not was_fresh
            raise
        except OSError as exc:
            self.close()
            lost = LiveConnectionLost(f"Connection to Live lost ({exc}).")
            lost.retryable = not was_fresh
            raise lost from exc
        self._fresh = False
        return reply

    def batch(self, commands: list[dict]) -> Any:
        return self.send("batch", {"commands": commands})

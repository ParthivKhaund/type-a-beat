import json
import socket

import pytest

from abl.wire import LiveClient, LiveCommandError, LiveError, LiveNotRunning, LiveTimeout


class FakeSock:
    def __init__(self, replies: list[bytes]):
        self.replies = list(replies)
        self.sent = b""
        self.closed = False
        self.timeout = None

    def sendall(self, data: bytes):
        self.sent += data

    def recv(self, size: int) -> bytes:
        if not self.replies:
            return b""
        chunk = self.replies.pop(0)
        if isinstance(chunk, Exception):
            raise chunk
        return chunk

    def settimeout(self, value):
        self.timeout = value

    def close(self):
        self.closed = True


def make_client(*replies, socks=None):
    """Replies are consumed in order across reconnects, like a real Live would answer."""
    made = socks if socks is not None else []
    queue = list(replies)

    def connector(address, timeout):
        sock = FakeSock(queue)
        sock.replies = queue
        made.append(sock)
        return sock

    return LiveClient(connector=connector), made


def test_send_frames_a_json_command_and_returns_the_result():
    client, socks = make_client(json.dumps({"status": "success", "result": {"tempo": 120}}).encode())
    assert client.send("get_session_info") == {"tempo": 120}
    assert json.loads(socks[0].sent) == {"type": "get_session_info", "params": {}}


def test_send_passes_params_through():
    client, socks = make_client(b'{"status": "success", "result": {}}')
    client.send("set_tempo", {"tempo": 128})
    assert json.loads(socks[0].sent)["params"] == {"tempo": 128}


def test_reply_split_across_chunks_is_reassembled():
    payload = json.dumps({"status": "success", "result": {"name": "Drums é"}}).encode()
    client, _ = make_client(payload[:7], payload[7:20], payload[20:])
    assert client.send("get_track_info", {"track_index": 0}) == {"name": "Drums é"}


def test_error_status_raises_with_lives_message():
    client, _ = make_client(b'{"status": "error", "message": "Track index out of range"}')
    with pytest.raises(LiveCommandError, match="Track index out of range"):
        client.send("get_track_info", {"track_index": 99})


def test_connection_refused_is_reported_as_live_not_running():
    def connector(address, timeout):
        raise ConnectionRefusedError

    client = LiveClient(connector=connector)
    with pytest.raises(LiveNotRunning, match="not running|Remote Script"):
        client.send("get_session_info")


def test_timeout_mentions_the_modal_dialog_and_drops_the_socket():
    client, socks = make_client(socket.timeout(), b'{"status": "success", "result": {}}')
    with pytest.raises(LiveTimeout, match="modal"):
        client.send("get_session_info")
    assert socks[0].closed
    client.send("get_session_info")
    assert len(socks) == 2


def test_socket_is_reused_between_commands():
    client, socks = make_client(b'{"status": "success", "result": 1}', b'{"status": "success", "result": 2}')
    assert client.send("a") == 1
    assert client.send("b") == 2
    assert len(socks) == 1


def test_batch_wraps_commands_under_the_batch_type():
    client, socks = make_client(b'{"status": "success", "result": {"results": []}}')
    cmds = [{"type": "set_tempo", "params": {"tempo": 100}}, {"type": "start_playback", "params": {}}]
    client.batch(cmds)
    assert json.loads(socks[0].sent) == {"type": "batch", "params": {"commands": cmds}}


def test_peer_closing_mid_reply_raises_a_live_error():
    client, _ = make_client(b'{"status": "succ')
    with pytest.raises(LiveError, match="mid-reply|closed"):
        client.send("get_session_info")


def test_a_stale_socket_after_a_live_restart_reconnects_once_and_resends():
    client, socks = make_client(b'{"status": "success", "result": 1}', b"", b'{"status": "success", "result": 2}')
    assert client.send("get_session_info") == 1
    assert client.send("get_session_info") == 2
    assert len(socks) == 2
    assert json.loads(socks[1].sent) == {"type": "get_session_info", "params": {}}


def test_a_fresh_socket_that_closes_at_once_does_not_loop():
    client, socks = make_client(b"", b"", b"")
    with pytest.raises(LiveError):
        client.send("get_session_info")
    assert len(socks) <= 2

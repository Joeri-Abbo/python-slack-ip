import socket
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Patch config loading before importing main
with patch("builtins.open", MagicMock(return_value=MagicMock(
    __enter__=MagicMock(return_value=b"slack:\n  webhook: http://example.com\n"),
    __exit__=MagicMock(return_value=False),
    read=MagicMock(return_value=b"slack:\n  webhook: http://example.com\n"),
))):
    with patch("yaml.safe_load", return_value={"slack": {"webhook": "http://example.com"}}):
        import main


def test_extract_ip_returns_string():
    ip = main.extract_ip()
    assert isinstance(ip, str)
    parts = ip.split(".")
    assert len(parts) == 4


def test_extract_ip_fallback():
    with patch("socket.socket") as mock_socket:
        instance = mock_socket.return_value
        instance.connect.side_effect = Exception("Network unreachable")
        ip = main.extract_ip()
    assert ip == "127.0.0.1"


def test_send_to_slack_posts_json():
    with patch("main.requests.post") as mock_post:
        mock_post.return_value = MagicMock(status_code=200)
        main.send_to_slack("test message")
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args
        assert call_kwargs[1]["headers"] == {"Content-Type": "application/json"}
        import json
        body = json.loads(call_kwargs[1]["data"])
        assert body["text"] == "test message"

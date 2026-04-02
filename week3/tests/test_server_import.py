# for smoke testing that the server module imports successfully and the mcp variable is defined.

from __future__ import annotations

from week3.server import mcp


def test_server_imports_successfully() -> None:
    assert mcp is not None
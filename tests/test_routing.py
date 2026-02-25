from app.core.session_manager import route_text


def test_menu_route() -> None:
    payloads = route_text("27820000000", "Hi")
    assert payloads[0]["interactive"]["type"] == "list"


def test_global_commands() -> None:
    assert "paused" in route_text("2782", "PAUSE")[0]["text"]["body"].lower()

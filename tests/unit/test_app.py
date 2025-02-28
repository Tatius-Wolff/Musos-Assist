from fastapi.testclient import TestClient
from musos_assist import app

client = TestClient(app)


def test_read_simple_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"

    with open("musos_assist/static/index.html", "r", newline="\r\n") as f:
        f_str = f.read()

    assert response.content.decode() == f_str

import os
import tempfile

import pytest

from app import app, init_app, reset_database
from api.utils import gen_token, generate_joke


@pytest.fixture(scope="session")
def client():
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_app(app)
            reset_database()
        yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


def test_get_token(client):
    with app.app_context():
        token = gen_token()

    assert token is not None


def test_generate_joke():
    assert len(generate_joke()) != 0

import json
import os.path
from os import environ as env
from pathlib import Path

import pytest

from chordrec import create_app


@pytest.fixture(scope="session", autouse=True)
def setup_envs():
    env["TELEGRAM_TOKEN"] = "fake_token"
    env["TELEGRAM_CHAT_ID"] = "fake_chat_id"
    yield


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class AssertValue:
    def __init__(self, path_obj):
        self.path_obj = path_obj

    def __call__(self, obj, fixture_name):
        with open(os.path.join(self.path_obj, fixture_name + ".txt"), 'r') as f:
            fixture = json.load(f)

        assert obj == fixture


@pytest.fixture
def assert_value():
    return AssertValue(Path(__file__).parent / 'fixtures')

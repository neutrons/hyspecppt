"""pytest configuration"""

import os
from configparser import ConfigParser

import pytest
import qtpy  # noqa: F401

from hyspecppt import Hyspecppt


@pytest.fixture
def hyspec_app(qapp):  # noqa: ARG001
    """Create a Hyspecppt app"""
    app = Hyspecppt()
    app.show()
    return app


@pytest.fixture(scope="session")
def user_conf_file(tmp_path_factory, request):
    """Fixture to create a custom configuration file in tmp_path"""
    # custom configuration file
    config_data = request.param
    user_config = ConfigParser(allow_no_value=True)
    user_config.read_string(config_data)
    user_path = os.path.join(tmp_path_factory.mktemp("data"), "test_config.ini")
    with open(user_path, "w", encoding="utf8") as config_file:
        user_config.write(config_file)
    return user_path

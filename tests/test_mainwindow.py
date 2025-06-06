"""UI tests for the application"""

import subprocess

import pytest

from hyspecppt.hyspecpptmain import __version__


def test_appwindow(hyspec_app, qtbot):
    """Test that the application starts successfully"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    assert hyspec_app.windowTitle() == f"Hyspecppt - {__version__}"


def test_gui_version():
    """Test that argument parameter --version prints the version"""
    full_command = ["hyspecppt", "--version"]
    version_result = subprocess.run(full_command, capture_output=True, text=True)
    version_result = version_result.stdout.strip()
    assert version_result == __version__


def test_gui_v():
    """Test that argument parameter -v prints the version"""
    full_command = ["hyspecppt", "-v"]
    version_result = subprocess.run(full_command, capture_output=True, text=True)
    version_result = version_result.stdout.strip()
    assert version_result == __version__


def test_gui_invalid_parameter():
    """Test that invalid parameter prints usage"""
    full_command = ["hyspecppt", "-invalid"]
    invalid_result = subprocess.run(full_command, capture_output=True, text=True)
    invalid_result = invalid_result.stderr.strip()
    assert invalid_result.startswith("usage: hyspecppt [-h] [-v]") is True


@pytest.mark.parametrize(
    "user_conf_file",
    [
        """
        [global.other]
        help_url = https://test.url.com

        """
    ],
    indirect=True,
)
def test_mainwindow_help(monkeypatch, user_conf_file, hyspec_app):
    """Test the help function in the main window"""
    help_url = ""

    def fake_webbrowser(url):
        nonlocal help_url
        help_url = url

    monkeypatch.setattr("hyspecppt.configuration.CONFIG_PATH_FILE", user_conf_file)
    monkeypatch.setattr("webbrowser.open", fake_webbrowser)

    hyspec_app.main_window.handle_help()
    assert help_url == "https://test.url.com"

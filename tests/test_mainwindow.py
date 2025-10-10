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


def test_gui_full_version_param():
    """Test that argument parameter --version prints the version"""
    hyspecppt_command = ["hyspecppt", "--version"]
    conda_command = ["conda list | grep hyspecppt", ""]
    # get the version from command line
    hyspecppt_version = subprocess.run(hyspecppt_command, capture_output=True, text=True)
    hyspecppt_version_result = hyspecppt_version.stdout.strip()
    # get the version from the environment
    conda_version = subprocess.run(conda_command, shell=True, capture_output=True, text=True)
    conda_version_result = conda_version.stdout.strip().split()[-3]
    # they should match
    assert hyspecppt_version_result == conda_version_result


def test_gui_v_param():
    """Test that argument parameter -v prints the version"""
    hyspecppt_command = ["hyspecppt", "-v"]
    conda_command = ["conda list | grep hyspecppt", ""]
    # get the version from command line
    hyspecppt_version = subprocess.run(hyspecppt_command, capture_output=True, text=True)
    hyspecppt_version_result = hyspecppt_version.stdout.strip()
    # get the version from the environment
    conda_version = subprocess.run(conda_command, shell=True, capture_output=True, text=True)
    conda_version_result = conda_version.stdout.strip().split()[-3]
    # they should match
    assert hyspecppt_version_result == conda_version_result


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

"""UI tests for the application"""


# def test_appwindow(qtbot):
#     """Test that the application starts successfully"""
#     hyspecplanningtools = HyspecPlanningTool()
#     hyspecplanningtools.show()
#     qtbot.waitUntil(hyspecplanningtools.show, timeout=5000)
#     assert hyspecplanningtools.isVisible()
#     assert hyspecplanningtools.windowTitle() == f"HyspecPlanning Tools - {__version__}"
#     hyspecplanningtools.destroy()


# def test_gui_version():
#     """Test that argument parameter --version prints the version"""
#     full_command = ["hyspecplanningtools", "--version"]
#     version_result = subprocess.run(full_command, capture_output=True, text=True)
#     version_result = version_result.stdout.strip()
#     assert version_result == __version__


# def test_gui_v():
#     """Test that argument parameter -v prints the version"""
#     full_command = ["hyspecplanningtools", "-v"]
#     version_result = subprocess.run(full_command, capture_output=True, text=True)
#     version_result = version_result.stdout.strip()
#     assert version_result == __version__


# @pytest.mark.parametrize(
#     "user_conf_file",
#     [
#         """
#         [global.other]
#         help_url = https://test.url.com

#         """
#     ],
#     indirect=True,
# )
# def test_mainwindow_help(monkeypatch, user_conf_file):
#     """Test the help function in the main window"""

#     fake_webbrowser = Mock()
#     monkeypatch.setattr("hyspecplanningtools.configuration.CONFIG_PATH_FILE", user_conf_file)
#     monkeypatch.setattr("webbrowser.open", fake_webbrowser)

#     main_window = MainWindow()
#     main_window.handle_help()
#     fake_webbrowser.assert_called_once()

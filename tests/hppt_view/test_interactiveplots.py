import os
import tempfile

from hyspecppt.hppt.hppt_view import PlotWidget


def test_save_file(qtbot, hyspec_app):
    """Test save file functions for HyspecPPT. It saves a test.png file in temp directory"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    canvas = plotwidget.static_canvas
    with tempfile.TemporaryDirectory() as temp_dir:
        canvas.print_png(os.path.join(temp_dir, "test.png"))
        assert os.path.isfile(os.path.join(temp_dir, "test.png"))


def test_home_button(qtbot, hyspec_app):
    """Test UI component home button exists and is clickable and can be triggered"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    home = plotwidget.toolbar.actions()[0]

    def on_action_triggered():
        print("Action triggered!")
        assert True

    home.triggered.connect(on_action_triggered)
    home.trigger()
    assert home.isEnabled()
    assert home.isVisible()


def test_back_button(qtbot, hyspec_app):
    """Test UI component back button exists and is NOT clickable and can be triggered"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    back = plotwidget.toolbar.actions()[1]

    def on_action_triggered():
        print("Action triggered!")
        assert False

    back.triggered.connect(on_action_triggered)
    back.trigger()
    assert not back.isEnabled()
    assert back.isVisible()


def test_forward_button(qtbot, hyspec_app):
    """Test UI component forward button exists and is NOT clickable and can be triggered"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    forward = plotwidget.toolbar.actions()[2]

    def on_action_triggered():
        print("Action triggered!")
        assert False

    forward.triggered.connect(on_action_triggered)
    forward.trigger()
    assert not forward.isEnabled()
    assert forward.isVisible()


def test_zoom_button(qtbot, hyspec_app):
    """Test UI component zoom button exists and is clickable and can be triggered"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    zoom = plotwidget.toolbar.actions()[5]

    def on_action_triggered():
        print("Action triggered!")
        assert True

    zoom.triggered.connect(on_action_triggered)
    zoom.trigger()
    assert zoom.isEnabled()
    assert zoom.isVisible()


def test_pan_button(qtbot, hyspec_app):
    """Test UI component pan button exists and is clickable"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    pan = plotwidget.toolbar.actions()[4]

    def on_action_triggered():
        print("Action triggered!")
        assert True

    pan.triggered.connect(on_action_triggered)
    pan.trigger()
    assert pan.isEnabled()
    assert pan.isVisible()


def test_subplots_button(qtbot, hyspec_app):
    """Test UI component subplots button exists and is clickable"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    subplots = plotwidget.toolbar.actions()[6]
    assert subplots.isEnabled()
    # assert False


def test_axes_button(qtbot, hyspec_app):
    """Test UI component axes button exists and is clickable"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    axes = plotwidget.toolbar.actions()[7]
    assert axes.isEnabled()
    assert axes.isVisible()


def test_save_button(qtbot, hyspec_app):
    """Test UI component save button exists and is clickable"""
    hyspec_app.show()
    qtbot.waitUntil(hyspec_app.show, timeout=5000)
    assert hyspec_app.isVisible()
    plotwidget = PlotWidget()
    save = plotwidget.toolbar.actions()[9]
    assert save.isEnabled()
    assert save.isVisible()

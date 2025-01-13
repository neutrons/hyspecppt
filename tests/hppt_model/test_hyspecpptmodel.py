import numpy as np

from hyspecppt.hppt.experiment_settings import DEFAULT_EXPERIMENT, DEFAULT_LATTICE, PLOT_TYPES
from hyspecppt.hppt.hppt_model import HyspecPPTModel  # noqa: F401


def test_setdefaultvalues():
    """Test setting single crystal data function"""
    model = HyspecPPTModel()
    assert model.Ei == DEFAULT_EXPERIMENT["Ei"]
    assert model.S2 == DEFAULT_EXPERIMENT["S2"]
    assert model.alpha_p == DEFAULT_EXPERIMENT["alpha_p"]
    assert model.plot_type == DEFAULT_EXPERIMENT["plot_type"]


def test_set_and_get_singlecrystaldata():
    """Test setting and getting single crystal data function"""
    model = HyspecPPTModel()
    params = DEFAULT_LATTICE
    model.set_single_crystal_data(params)
    assert model.get_single_crystal_data()["a"] == params["a"]
    assert model.get_single_crystal_data()["b"] == params["b"]
    assert model.get_single_crystal_data()["c"] == params["c"]

    assert model.get_single_crystal_data()["alpha"] == params["alpha"]
    assert model.get_single_crystal_data()["beta"] == params["beta"]
    assert model.get_single_crystal_data()["gamma"] == params["gamma"]

    assert model.get_single_crystal_data()["h"] == params["h"]
    assert model.get_single_crystal_data()["k"] == params["k"]
    assert model.get_single_crystal_data()["l"] == params["l"]


def test_set_and_get_crosshairdata():
    """Test setting and getting crosshair data function"""
    model = HyspecPPTModel()
    current_experiment_type = "powder"
    model.set_crosshair_data(current_experiment_type=current_experiment_type, DeltaE=20.0, modQ=1.0)
    assert model.get_crosshair_data()["DeltaE"] == 20.0
    assert model.get_crosshair_data()["modQ"] == 1.0

    current_experiment_type = "single_crystal"
    model.set_single_crystal_data(DEFAULT_LATTICE)
    model.set_crosshair_data(current_experiment_type=current_experiment_type, DeltaE=30.0, modQ=1.0)
    assert model.get_crosshair_data()["DeltaE"] == 30.0
    assert model.get_crosshair_data()["modQ"] == 0.0
    model.cp.sc_parameters.h = 10
    model.cp.sc_parameters.l = 10
    model.cp.sc_parameters.k = 10
    assert np.isclose(model.get_crosshair_data()["modQ"], 108.827)  # modQ greater than maxQ
    assert model.cp.modQ == 0.0  # stored modQ is still 0.0


def test_set_and_get_experimentdata():
    """Test setting and getting experiment data function"""
    model = HyspecPPTModel()
    model.set_experiment_data(Ei=10.0, S2=35.0, alpha_p=45.0, plot_type=PLOT_TYPES[0])
    assert model.get_experiment_data()["Ei"] == 10.0
    assert model.get_experiment_data()["S2"] == 35.0
    assert model.get_experiment_data()["alpha_p"] == 45.0
    assert model.get_experiment_data()["plot_type"] == PLOT_TYPES[0]


def test_calculate_graph_data():
    """Test calculating different graph data"""
    pass

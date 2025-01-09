import hyspecppt.hppt.hppt_model as hppt_model
import numpy as np

def test_single_crystal_parameter_set_parameters():
    """Test SingleCrystalParameters set_parameters function"""
    scp = hppt_model.SingleCrystalParameters()
    sc_data = {"a":1.0, "b":1.0,"c":1.0, "alpha":90.0, "beta":90, "gamma":90, "h": 0, "k":0, "l":0}
    scp.set_parameters(sc_data)
    
    assert scp.a == 1.0
    assert scp.b == 1.0
    assert scp.c == 1.0
    assert scp.alpha == 90.0
    assert scp.beta == 90.0
    assert scp.gamma == 90.0
    assert scp.h == 0
    assert scp.k == 0
    assert scp.l == 0

def test_single_crystal_parameter_get_parameters():
    """Test SingleCrystalParameters get_parameters function"""
    scp = hppt_model.SingleCrystalParameters()
    sc_data = {"a":1.0, "b":1.0,"c":1.0, "alpha":90.0, "beta":90, "gamma":90, "h": 0, "k":0, "l":0}
    scp.set_parameters(sc_data)

    assert scp.get_parameters()["a"] == 1.0
    assert scp.get_parameters()["b"] == 1.0
    assert scp.get_parameters()["c"] == 1.0
    assert scp.get_parameters()["alpha"] == 90.0
    assert scp.get_parameters()["beta"] == 90.0
    assert scp.get_parameters()["gamma"] == 90.0
    assert scp.get_parameters()["h"] == 0
    assert scp.get_parameters()["k"] == 0
    assert scp.get_parameters()["l"] == 0

def test_single_crystal_parameter_calculate_modQ():
    """Test SingleCrystalParameters calculate_modQ function"""
    scp = hppt_model.SingleCrystalParameters()
    sc_data = {"a":1.0, "b":1.0,"c":1.0, "alpha":90.0, "beta":90, "gamma":90, "h": 0, "k":0, "l":0}
    scp.set_parameters(sc_data)
    assert scp.calculate_modQ() == 0.0

    sc_data["h"] = 1
    sc_data["k"] = 2
    sc_data["l"] = 3
    scp.set_parameters(sc_data)
    assert np.isclose(scp.calculate_modQ(), 23.5095267)

    sc_data["alpha"] = 60
    sc_data["beta"] = 60
    sc_data["gamma"] = 90
    scp.set_parameters(sc_data)
    assert np.isclose(scp.calculate_modQ(), 19.3660777)

    sc_data["a"] = 10
    sc_data["b"] = 10
    sc_data["c"] = 15.12312
    scp.set_parameters(sc_data)
    assert np.isclose(scp.calculate_modQ(), 1.469240)

def test_cross_hair_parameters_set_crosshair():
    """Test Crosshair set_crosshair function"""
    cp = hppt_model.CrosshairParameters()
    current_experiment_type = "single_crystal"
    DeltaE = 10.0
    modQ = 1.23
    cp.set_crosshair(current_experiment_type)
    assert cp.current_experiment_type == "single_crystal"

    cp.set_crosshair(current_experiment_type, DeltaE = DeltaE)
    assert cp.DeltaE == 10.0

    cp.set_crosshair(current_experiment_type, modQ = modQ)
    assert cp.DeltaE == 10.0
    assert cp.modQ == 1.23

def test_get_cross_hair_parameters_set_crosshair():
    """Test Crosshair get_crosshair function"""
    cp = hppt_model.CrosshairParameters()
    current_experiment_type = "single_crystal"
    DeltaE = 10.0
    modQ = 1.23

    cp.set_crosshair(current_experiment_type, DeltaE = DeltaE, modQ = modQ)
    cp.sc_parameters.set_parameters({"a":1.0, "b":1.0,"c":1.0, "alpha":90.0, "beta":90, "gamma":90, "h": 0, "k":0, "l":0})
    assert cp.get_crosshair()["DeltaE"] == 10.0
    assert cp.get_crosshair()["modQ"] == 0.0

    cp.set_crosshair("powder", DeltaE = DeltaE, modQ = modQ)
    assert cp.get_crosshair()["DeltaE"] == 10.0
    assert cp.get_crosshair()["modQ"] == 1.23
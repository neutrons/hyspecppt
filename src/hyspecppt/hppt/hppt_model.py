"""Model for the polarization planning tool"""
import numpy as np
import logging


logger = logging.getLogger("hyspecppt")

class SingleCrystalParameters:
    """Model for single crystal calculations"""
    a: float
    b: float
    c: float
    alpha: float
    beta: float
    gamma: float
    h: float
    k: float
    l: float

    def __init__(self) -> None:
        """Constructor"""
        return

    def set_parameters(self, params: dict[str, float]) -> None:
        """store single crystal parameters

        Args:
            params: dict - contains the following keys:
                a, b, c, alpha, beta, gamma, h, k, l

        """
        self.a = params["a"]
        self.b = params["b"]
        self.c = params["c"]
        self.alpha = params["alpha"]
        self.beta = params["beta"]
        self.gamma = params["gamma"]
        self.h = params["h"]
        self.k = params["k"]
        self.l = params["l"]

    def get_paramters(self) -> dict[str, float]:
        """returns all the parameters as a dictionary"""
        try:
            return dict(a=self.a, b=self.b, c=self.c, alpha=self.alpha, beta=self.beta, gamma=self.gamma, h=self.h, k=self.k, l=self.l)
        except AttributeError:
            logger.error("The parameters were not initialized")

    def calculate_modQ(self) -> float:
        """returns |Q| from lattice parameters and h, k, l"""
        try:
            ca = np.cos(np.radians(self.alpha))
            sa = np.sin(np.radians(self.alpha))
            cb = np.cos(np.radians(self.beta))
            sb = np.sin(np.radians(self.beta))
            cg = np.cos(np.radians(self.gamma))
            sg = np.sin(np.radians(self.gamma))
            vabg = np.sqrt(1 - ca**2 - cb**2 - cg**2 + 2 * ca * cb * cg)
            astar = sa / (self.a * vabg)
            bstar = sb / (self.b * vabg)
            cstar = sg / (self.c * vabg)
            cas = (cb * cg - ca) / (sb * sg)
            cbs = (cg * ca - cb) / (sg * sa)
            cgs = (ca * cb - cg) / (sa * sb)

            # B matrix
            B = np.array(
                [
                    [astar, bstar * cgs, cstar * cbs],
                    [0, bstar * np.sqrt(1 - cgs**2), -cstar * np.sqrt(1 - cbs**2) * ca],
                    [0, 0, 1.0 / self.c],
                ]
            )

            modQ = 2 * np.pi * np.linalg.norm(B.dot([self.h, self.k, self.l]))
            return modQ
        except AttributeError:
            logger.error("The parameters were not initialized")


class CrosshairParameters:
    """Model for the crosshair parameters"""
    modQ: float
    DeltaE: float
    current_experiment_type: str
    sc_parameters: SingleCrystalParameters

    def __init__(self):
        self.sc_parameters=SingleCrystalParameters()

    def store_data(self, *, current_experiment_type: str = None, DeltaE: float = None,
                    modQ: float = None, sc_parameters:dict[str, float] = None) -> None:
        """store crosshair parameters including in SC mode"""
        if current_experiment_type is not None:
            self.current_experiment_type = current_experiment_type
        if DeltaE is not None:
            self.DeltaE = DeltaE
        if modQ is not None:
            self.modQ = modQ
        if sc_parameters is not None:
            self.sc_parameters.set_parameters(sc_parameters)

    def get_crosshair(self) -> dict[str, float]:
        """get the crosshair"""
        if self.current_experiment_type == "crystal":
            self.modQ = self.sc_parameters.calculate_modQ()
        return dict(DeltaE=self.DeltaE, modQ=self.modQ)


class HyspecPPTModel:
    """Main model"""
    Ei: float = 0
    S2: float = 0
    alpha_p: float = 0
    plot_type: str = ""
    cp: CrosshairParameters

    def __init__(self):
        """Constructor"""
        self.cp = CrosshairParameters()

    def store_experiment_data(self, Ei: float, S2: float, alpha_p: float, plot_type: str) -> None:
        self.Ei = Ei
        self.S2 = S2
        self.alpha_p = alpha_p
        self.plot_type = plot_type

    def store_crosshair_data(self, *, current_experiment_type: str = None, DeltaE: float = None, modQ: float = None) -> None:
        self.cp.store_data(current_experiment_type=current_experiment_type, DeltaE=DeltaE, modQ=modQ)

    def store_single_crystal_data(self, params: dict[str, float]) -> None:
        self.cp.store_data(sc_parameters=params)

    def get_crosshair(self) -> dict[str, float]:
        return self.cp.get_crosshair()

    def calculate_graph_data(self):
        return [1,2,3]

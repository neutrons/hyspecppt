"""Model for the polarization planning tool"""

import logging

import numpy as np
from scipy.constants import e, hbar, m_n

from .experiment_settings import PLOT_TYPES

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
        """Store single crystal parameters

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
        """Returns all the parameters as a dictionary"""
        try:
            return dict(
                a=self.a,
                b=self.b,
                c=self.c,
                alpha=self.alpha,
                beta=self.beta,
                gamma=self.gamma,
                h=self.h,
                k=self.k,
                l=self.l,
            )
        except AttributeError:
            logger.error("The parameters were not initialized")

    def calculate_modQ(self) -> float:
        """Returns |Q| from lattice parameters and h, k, l"""
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
        self.sc_parameters = SingleCrystalParameters()

    def store_data(
        self,
        *,
        current_experiment_type: str = None,
        DeltaE: float = None,
        modQ: float = None,
        sc_parameters: dict[str, float] = None,
    ) -> None:
        """Store crosshair parameters including in SC mode"""
        if current_experiment_type is not None:
            self.current_experiment_type = current_experiment_type
        if DeltaE is not None:
            self.DeltaE = DeltaE
        if modQ is not None:
            self.modQ = modQ
        if sc_parameters is not None:
            self.sc_parameters.set_parameters(sc_parameters)

    def get_crosshair(self) -> dict[str, float]:
        """Get the crosshair"""
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

    def store_crosshair_data(
        self, *, current_experiment_type: str = None, DeltaE: float = None, modQ: float = None
    ) -> None:
        self.cp.store_data(current_experiment_type=current_experiment_type, DeltaE=DeltaE, modQ=modQ)

    def store_single_crystal_data(self, params: dict[str, float]) -> None:
        self.cp.store_data(sc_parameters=params)

    def get_crosshair(self) -> dict[str, float]:
        return self.cp.get_crosshair()

    def get_graph_data(self) -> list:
        return self.calculate_graph_data()

    def calculate_graph_data(self) -> list[float]:
        """Returns a list of [Q_low, Q_hi, E, Q2d, E2d, data of plot_types]"""
        try:
            SE2K = np.sqrt(2e-3 * e * m_n) * 1e-10 / hbar
            # def Ei, Emin = - Ei to create Qmin, Qmax to generate plot range
            if self.cp.DeltaE is not None and self.cp.DeltaE < -self.Ei:
                EMin = -self.Ei
            E = np.linspace(EMin, self.Ei * 0.9, 200)

            kfmin = np.sqrt(self.Ei - EMin) * SE2K
            ki = np.sqrt(self.Ei) * SE2K

            # S2= 60
            # Create Qmin and Qmax
            Qmax = np.sqrt(ki**2 + kfmin**2 - 2 * ki * kfmin * np.cos(np.radians(self.S2 + 30)))  # Q=ki or Q=
            Qmin = 0
            Q = np.linspace(Qmin, Qmax, 200)

            # Create 2D array
            E2d, Q2d = np.meshgrid(E, Q)

            Ef2d = self.Ei - E2d
            kf2d = np.sqrt(Ef2d) * SE2K

            Px = np.cos(np.radians(self.alpha_p))
            Pz = np.sin(np.radians(self.alpha_p))

            cos_theta = (ki**2 + kf2d**2 - Q2d**2) / (2 * ki * kf2d)
            cos_theta[cos_theta < np.cos(np.radians(self.S2 + 30))] = np.nan
            cos_theta[cos_theta > np.cos(np.radians(self.S2 - 30))] = np.nan  # cos(30)

            Qz = ki - kf2d * cos_theta

            if self.S2 >= 30:
                Qx = (-1) * kf2d * np.sqrt((1 - cos_theta**2))
            elif self.S2 <= -30:
                Qx = kf2d * np.sqrt((1 - cos_theta**2))

            cos_ang_PQ = (Qx * Px + Qz * Pz) / Q2d / np.sqrt(Px**2 + Pz**2)
            ang_PQ = np.degrees(np.arccos(cos_ang_PQ))

            kf = np.sqrt(self.Ei - E) * SE2K

            Q_low = np.sqrt(ki**2 + kf**2 - 2 * ki * kf * np.cos(np.radians(self.S2 - 30)))
            Q_hi = np.sqrt(ki**2 + kf**2 - 2 * ki * kf * np.cos(np.radians(self.S2 + 30)))

            if self.plot_type == PLOT_TYPES[0]:  # alpha
                return [Q_low, Q_hi, E, Q2d, E2d, ang_PQ]

            if self.plot_type == PLOT_TYPES[1]:  # cos^2(alpha)
                return [Q_low, Q_hi, E, Q2d, E2d, np.cos(np.radians(ang_PQ)) ** 2]

            if self.plot_type == PLOT_TYPES[2]:  # "(cos^2(a)+1)/2"
                return [Q_low, Q_hi, E, Q2d, E2d, (np.cos(np.radians(ang_PQ)) ** 2 + 1) / 2]
        except AttributeError:
            logger.error("The parameters were not initialized")

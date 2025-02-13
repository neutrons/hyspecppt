"""Model for the polarization planning tool"""

import logging

import numpy as np
from scipy.constants import e, hbar, m_n

from .experiment_settings import (
    DEFAULT_CROSSHAIR,
    DEFAULT_EXPERIMENT,
    DEFAULT_LATTICE,
    DEFAULT_MODE,
    MAX_MODQ,
    N_POINTS,
    PLOT_TYPES,
    TANK_HALF_WIDTH,
)

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
        self.set_parameters(DEFAULT_LATTICE)

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

    def get_parameters(self) -> dict[str, float]:
        """Returns all the parameters as a dictionary"""
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

    def calculate_modQ(self) -> float:
        """Returns |Q| from lattice parameters and h, k, l"""
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
        cas = (cb * cg - ca) / (sb * sg)  # noqa: F841
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


class CrosshairParameters:
    """Model for the crosshair parameters"""

    modQ: float
    DeltaE: float
    current_experiment_type: str
    sc_parameters: SingleCrystalParameters

    def __init__(self) -> None:
        """Constructor"""
        self.set_crosshair(**DEFAULT_MODE, **DEFAULT_CROSSHAIR)
        self.sc_parameters = SingleCrystalParameters()

    def set_crosshair(self, current_experiment_type: str, DeltaE: float = None, modQ: float = None) -> None:
        """Store crosshair parameters including in SC mode"""
        if current_experiment_type is not None:
            self.current_experiment_type = current_experiment_type
        if DeltaE is not None:
            self.DeltaE = DeltaE
        if modQ is not None:
            self.modQ = modQ

    def get_crosshair(self) -> dict[str, float]:
        """Get the crosshair"""
        if self.current_experiment_type == "single_crystal":
            modQ = self.sc_parameters.calculate_modQ()
            # update the valid value
            if modQ < MAX_MODQ:
                self.modQ = modQ
            return dict(DeltaE=self.DeltaE, modQ=modQ)
        return dict(DeltaE=self.DeltaE, modQ=self.modQ)

    def get_experiment_type(self) -> str:
        """Return experiment type"""
        return self.current_experiment_type


class HyspecPPTModel:
    """Main model"""

    Ei: float
    S2: float
    Emin: float
    alpha_p: float
    plot_type: str
    cp: CrosshairParameters

    def __init__(self):
        """Constructor"""
        self.set_experiment_data(**DEFAULT_EXPERIMENT)
        self.cp = CrosshairParameters()

    def set_single_crystal_data(self, params: dict[str, float]) -> None:
        self.cp.sc_parameters.set_parameters(params)

    def get_single_crystal_data(self) -> dict[str, float]:
        return self.cp.sc_parameters.get_parameters()

    def set_crosshair_data(self, current_experiment_type: str, DeltaE: float = None, modQ: float = None) -> None:
        self.cp.set_crosshair(current_experiment_type=current_experiment_type, DeltaE=DeltaE, modQ=modQ)

    def get_crosshair_data(self) -> dict[str, float]:
        return self.cp.get_crosshair()

    def set_experiment_data(self, Ei: float, S2: float, alpha_p: float, plot_type: str) -> None:
        self.Ei = Ei
        self.S2 = S2
        self.alpha_p = alpha_p
        self.plot_type = plot_type

    def get_experiment_data(self) -> dict[str, float]:
        data = dict(Ei=self.Ei, S2=self.S2, alpha_p=self.alpha_p, plot_type=self.plot_type)
        return data

    def check_plot_update(self, deltaE) -> bool:
        """Returns bool to indicate whether the Emin is different and indicate replotting"""
        # calculate the new Emin
        if deltaE is not None and deltaE <= -self.Ei:
            Emin = 1.2 * deltaE
        else:
            Emin = -self.Ei
        # check if it is the same
        return self.Emin != Emin

    def get_ang_Q_beam(self) -> float:
        """Returns the angle between Q and the beam"""
        SE2K = np.sqrt(2e-3 * e * m_n) * 1e-10 / hbar
        crosshair_data = self.get_crosshair_data()
        deltaE = crosshair_data["DeltaE"]
        modQ = crosshair_data["modQ"]
        ki = np.sqrt(self.Ei) * SE2K
        kf = np.sqrt(self.Ei - deltaE) * SE2K
        cos_theta = (ki**2 + kf**2 - modQ**2) / (2 * ki * kf)
        with np.errstate(
            invalid="ignore"
        ):  # ignore the state when users put a non-zero deltaE while modQ is still at 0
            return np.degrees(np.arccos(cos_theta)) if self.S2 < 0 else -np.degrees(np.arccos(cos_theta))

    def calculate_graph_data(self) -> dict[str, np.array]:
        """Returns a dictionary of arrays [Q_low, Q_hi, E, Q2d, E2d, data of plot_types]"""
        # constant to transform from energy in meV to momentum in Angstrom^-1
        SE2K = np.sqrt(2e-3 * e * m_n) * 1e-10 / hbar

        # adjust minimum energy
        if self.cp.DeltaE is not None and self.cp.DeltaE <= -self.Ei:
            self.Emin = 1.2 * self.cp.DeltaE
        else:
            self.Emin = -self.Ei

        E = np.linspace(self.Emin, self.Ei * 0.9, N_POINTS)

        # Calculate lines for the edges of the tank
        ki = np.sqrt(self.Ei) * SE2K
        kf = np.sqrt(self.Ei - E) * SE2K
        Q_low = np.sqrt(ki**2 + kf**2 - 2 * ki * kf * np.cos(np.radians(np.abs(self.S2) - TANK_HALF_WIDTH)))
        Q_hi = np.sqrt(ki**2 + kf**2 - 2 * ki * kf * np.cos(np.radians(np.abs(self.S2) + TANK_HALF_WIDTH)))

        # Create 2D array
        Q = np.linspace(0, np.max(Q_hi), N_POINTS)
        E2d, Q2d = np.meshgrid(E, Q)
        Ef2d = self.Ei - E2d
        kf2d = np.sqrt(Ef2d) * SE2K

        # Calculate the angle between Q and z axis. Set to NAN values outside the detector range
        cos_theta = (ki**2 + kf2d**2 - Q2d**2) / (2 * ki * kf2d)
        cos_theta[cos_theta < np.cos(np.radians(np.abs(self.S2) + TANK_HALF_WIDTH))] = np.nan
        cos_theta[cos_theta > np.cos(np.radians(np.abs(self.S2) - TANK_HALF_WIDTH))] = np.nan

        # Calculate Qz
        Qz = ki - kf2d * cos_theta

        # Calculate Qx. Note that is in the opposite direction as detector position
        if self.S2 >= TANK_HALF_WIDTH:
            Qx = (-1) * kf2d * np.sqrt((1 - cos_theta**2))
        elif self.S2 <= -TANK_HALF_WIDTH:
            Qx = kf2d * np.sqrt((1 - cos_theta**2))

        # Transform polarization angle in the lab frame to vector
        Px = np.sin(np.radians(self.alpha_p))
        Pz = np.cos(np.radians(self.alpha_p))

        # Calculate angle between polarization vector and momentum transfer
        cos_ang_PQ = (Qx * Px + Qz * Pz) / Q2d

        # Select return value for intensity
        if self.plot_type == PLOT_TYPES[0]:  # alpha
            ang_PQ = np.arccos(cos_ang_PQ)
            intensity = np.degrees(ang_PQ)
        elif self.plot_type == PLOT_TYPES[1]:  # cos^2(alpha)
            intensity = cos_ang_PQ**2
        elif self.plot_type == PLOT_TYPES[2]:  # "(cos^2(a)+1)/2"
            intensity = (cos_ang_PQ**2 + 1) / 2

        return dict(Q_low=Q_low, Q_hi=Q_hi, E=E, Q2d=Q2d, E2d=E2d, intensity=intensity, plot_type=self.plot_type)

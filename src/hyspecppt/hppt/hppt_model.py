"""Model for the polarization planning tool"""

import logging
from typing import Tuple

import numpy as np

logger = logging.getLogger("hyspecppt")


class SingleCrystalModel:
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
        self.a, self.b, self.c, self.alpha, self.beta, self.gamma, self.h, self.k, self.l = params.values()

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

    def calculate_modq(self) -> float:
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
    deltaE: float
    current_experiment_type: str
    sc_parameters: SingleCrystalModel

    def __init__(self):
        pass

    def store_data(
        self,
        *,
        current_experiment_type: str = None,
        delta_e: float = None,
        mod_q: float = None,
        sc_parameters: dict[str, float] = None,
    ) -> None:
        """Store crosshair parameters including in SC mode"""
        self.current_experiment_type = current_experiment_type
        if delta_e is not None:
            self.deltaE = delta_e
        if mod_q is not None:
            self.modQ = mod_q
        if sc_parameters is not None:
            self.sc_parameters.set_parameters(sc_parameters)
            self.modQ = self.sc_parameters.calculate_modq()

    def get_crosshair(self) -> Tuple[float, float]:
        """Get the crosshair"""
        return self.deltaE, self.modQ


class HyspecPPTModel:
    """Main model"""

    Ei: float
    S2: float
    alpha_p: float
    plot_type: str

    def __init__(self):
        """Constructor"""
        return

    def store_data(
        self,
        incident_energy_e: float,
        detector_tank_angle_s: float,
        polarization_direction_angle_p: float,
        plot_type: str,
    ) -> None:
        Ei = incident_energy_e
        S2 = detector_tank_angle_s

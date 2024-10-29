import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import e, hbar, m_n


class model_polarization(object):
    def __init__(self):
        self.S2 = 30.0
        self.Ei = 20.0
        self.Q = None
        self.DeltaE = None
        self.Emin = -self.Ei
        self.B = None

    def Bmatrix(self, a, b, c, alpha, beta, gamma):
        ca = np.cos(np.radians(alpha))
        sa = np.sin(np.radians(alpha))
        cb = np.cos(np.radians(beta))
        sb = np.sin(np.radians(beta))
        cg = np.cos(np.radians(gamma))
        sg = np.sin(np.radians(gamma))
        vabg = np.sqrt(1 - ca**2 - cb**2 - cg**2 + 2 * ca * cb * cg)
        astar = sa / (a * vabg)
        bstar = sb / (b * vabg)
        cstar = sg / (c * vabg)
        cas = (cb * cg - ca) / (sb * sg)
        cbs = (cg * ca - cb) / (sg * sa)
        cgs = (ca * cb - cg) / (sa * sb)
        self.B = np.array(
            [
                [astar, bstar * cgs, cstar * cbs],
                [0, bstar * np.sqrt(1 - cgs**2), -cstar * np.sqrt(1 - cbs**2) * ca],
                [0, 0, 1.0 / c],
            ]
        )

    def modQ_from_HKL(self, h, k, l):
        if self.B:
            self.Q = 2 * np.pi * np.linalg.norm(self.B.dot([h, k, l]))

    def set_energy(self, newEi, newDeltaE=None):
        self.Ei = newEi
        self.DeltaE = newDeltaE
        if newDeltaE is not None and newDeltaE < -self.Ei:
            self.Emin = newDeltaE
        else:
            self.Emin = -self.Ei
        self.update()

    def set_S2(self, newS2):
        self.S2 = newS2

    def q_at_angle(self, angle):
        SE2K = np.sqrt(2e-3 * e * m_n) * 1e-10 / hbar
        dE = np.linspace(self.Emin, self.Ei * 0.99, 200)
        ki = np.sqrt(self.Ei) * SE2K
        kf = np.sqrt(self.Ei - dE) * SE2K
        return np.sqrt(ki**2 + kf**2 - 2 * ki * kf * np.cos(np.radians(angle))), dE

    def q_min_max(self):
        max_angle = abs(self.S2) + 30.0
        min_angle = np.max([0, abs(self.S2) - 30.0])
        return self.q_at_angle(min_angle), self.q_at_angle(max_angle)

    def update(self):
        return self.q_min_max(), self.DeltaE, self.Q


class plot_polarization(object):
    model = model_polarization()

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.qmin_line = self.ax.plot([0, 0], [0, 0])[0]
        self.qmax_line = self.ax.plot([0, 0], [0, 0])[0]
        self.qline = self.ax.axvline(x=0)
        self.eline = self.ax.axhline(y=0)
        self.ax.set_xlabel(r"$|Q| (\AA^{-1})$")
        self.ax.set_ylabel("DeltaE (meV)")
        self.update_figure()
        self.fig.show()

    def update_figure(self):
        (qmin_line_data, qmax_line_data), ecursor, qcursor = self.model.update()
        self.qmin_line.set_data(qmin_line_data)
        self.qmax_line.set_data(qmax_line_data)
        if ecursor is not None:
            self.eline.set_data([0, 1], [ecursor, ecursor])
        if qcursor is not None:
            self.qline.set_data([qcursor, qcursor], [0, 1])
        self.ax.relim()
        self.ax.autoscale()
        self.fig.canvas.draw()

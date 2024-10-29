"""This is a script that use the package as a module."""

#!/usr/bin/env python
import matplotlib.pyplot as plt
from polarization import plot_polarization

# show figure
p1 = plot_polarization()
input("Press Enter to continue...")

p2 = plot_polarization()
# clear the plot
plt.close(p2.fig)
p2.model.set_energy(40, 10)
p2.model.set_S2(-55)
p2.model.Q = 3.4
p2.update_figure()


# show updated figure
p = plot_polarization()
input("Press Enter to exit...")

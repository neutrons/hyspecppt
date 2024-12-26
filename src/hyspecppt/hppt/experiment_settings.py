"""Definition of constants and default parameters"""

# unicode
alpha = "\u03b1"
beta = "\u03b2"
gamma = "\u03b3"
square = "\u00b2"
subscript_s = "\u209b"

# defined plot types
PLOT_TYPES = [
    alpha + subscript_s,
    "cos" + alpha + subscript_s + square,
    "(1+cos" + alpha + subscript_s + square + ")/2",
]

# default parameters
DEFAULT_LATTICE = dict(a=1, b=1, c=1, alpha=90, beta=90, gamma=90, h=0, k=0, l=0)
DEFAULT_EXPERIMENT = dict(Ei=20, S2=30, alpha_p=0, plot_type=PLOT_TYPES[1])
DEFAULT_CROSSHAIR = dict(DeltaE=0, modQ=0)

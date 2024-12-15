alpha = "\u03B1"
beta = "\u03B2"
gamma = "\u03B3"
square = "\u00B2"
subscript_s = "\u209B"

PLOT_TYPES = [alpha+subscript_s,
              "cos"+alpha+subscript_s+square,
              "(1+cos"+alpha+subscript_s+square+")/2"]

DEFAULT_LATTICE = dict(a=1, b=1, c=1, alpha=90, beta=90, gamma=90, h=0, k=0, l=0)
DEFAULT_EXPERIMENT = dict(Ei=20, s2=30, alpha_p=0, plot_type=PLOT_TYPES[1])
DEFAULT_CROSSHAIR = dict(DeltaE=0, modQ=0)

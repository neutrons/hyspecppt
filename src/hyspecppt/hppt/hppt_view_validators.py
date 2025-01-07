import copy
from qtpy.QtCore import QObject
from qtpy.QtGui import QDoubleValidator, QValidator


class AbsValidator(QDoubleValidator):
    """Absolute value validator"""

    def __init__(self, parent: QObject, bottom: float, top: float, decimals: int = -1) -> None:
        """Constructor for the absolute value validator. All the parameters
           are the same as for QDoubleValidator, but the valid value is between a
           positive bottom and top, or between -top and -bottom

        Args:
            parent (QObject): Optional parent
            bottom (float): the minimum positive value (set to 0 if not positive)
            top (float): the highest top value (set to infinity if not greater than bottom)
            decimals (int): the number of digits after the decimal point.

        """
        super().__init__(parent=parent, bottom=bottom, top=top, decimals=decimals)

    def validate(self, inp: str, pos: int) -> tuple[QValidator.State, str, int]:
        """Override for validate method

        Args:
            inp (str): the input string
            pos (int): cursor position

        """
        original_str = copy.copy(inp)
        original_pos = pos
        if inp == "-":
            return QValidator.Intermediate
        try:
            inp = str(abs(float(inp)))
        except ValueError:
            pass
        x = super().validate(inp, pos)
        # do not "fix" the input
        return x[0], original_str, original_pos

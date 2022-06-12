import pathlib

HERE = pathlib.Path(__file__).parent
__version__ = (HERE / "VERSION").read_text().strip()


from shapley_values.shapley import *
from shapley_values.x_shapley import *
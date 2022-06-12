import pathlib

HERE = pathlib.Path(__file__).parent
__version__ = (HERE / "VERSION").read_text().strip()


from shapley import shapley
from x_shapley import x_shapley
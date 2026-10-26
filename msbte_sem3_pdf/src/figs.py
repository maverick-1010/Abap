"""Import every figure module so that they register themselves in FIGS."""
import importlib
from figreg import FIGS  # noqa: F401

for _m in ("figs_te1", "figs_te2", "figs_som", "figs_pd1", "figs_pd2", "figs_pd3", "figs_pd4"):
    try:
        importlib.import_module(_m)
    except ModuleNotFoundError as e:
        if e.name != _m:
            raise

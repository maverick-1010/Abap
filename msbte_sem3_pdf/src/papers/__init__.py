import importlib
from collections import OrderedDict

REQUESTED = OrderedDict([
    ("SOM", ("Strength of Materials", "313308")),
    ("FMM", ("Fluid Mechanics & Machinery", "313309")),
    ("TE", ("Thermal Engineering", "313310")),
    ("PD", ("Production Drawing", "313311")),
])

EXTRA_NOTE = ("Only part of the requested set was received: 4 of the 12 papers (Thermal Engineering W24 and S25, Production Drawing W24 and S25). "
              "The Strength of Materials file supplied is <b>Summer 2023, I-scheme (paper code 22306)</b>, not one of the three sessions you listed, "
              "so it is included as a clearly labelled extra paper. No Fluid Mechanics paper was received. Missing papers are listed on the next page and are not guessed.")

CONCEPT_TITLES = {}
REVISION = {}

for _m in ("te_w24", "te_s25", "som_s23", "pd_w24", "pd_s25", "backmatter"):
    try:
        importlib.import_module(f"papers.{_m}")
    except ModuleNotFoundError as e:
        if e.name != f"papers.{_m}":
            raise

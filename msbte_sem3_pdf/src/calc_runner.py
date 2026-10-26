import importlib
import json
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import common  # noqa: F401
import calcfw

for mod in ("te", "som", "pd"):
    try:
        importlib.import_module(f"calcs.{mod}")
    except ModuleNotFoundError as e:
        if e.name != f"calcs.{mod}":
            raise
res = calcfw.run_all()
for cid, d in res.items():
    ans = "; ".join(f"{a['name']} = {a['value']} {a['unit']}".strip() for a in d["answers"])
    chk = ", ".join("PASS" if k["passed"] else "FAIL" for k in d["checks"])
    print(f"{cid}: {ans}   [{chk}]")
print(len(res), "calculations run")

"""Reporte agregado funcional, sin endpoint de predicción individual."""
import argparse
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def report(group="smoker,bmi_group", smoker="all"):
    allowed = {"smoker", "smoker,bmi_group", "smoker,age_group", "smoker,region", "smoker,children_group"}
    if group not in allowed:
        raise ValueError(f"Dimensiones permitidas: {sorted(allowed)}")
    frame = pd.read_csv(ROOT / "results/group_costs.csv")
    frame = frame.loc[frame.group_dimensions == group].copy()
    if smoker != "all":
        frame = frame.loc[frame.smoker == smoker]
    frame = frame.loc[frame.n >= 5]
    return frame[group.split(",") + ["n", "charges_mean", "expected_mean", "small_group"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", default="smoker,bmi_group")
    parser.add_argument("--smoker", choices=["all", "no", "yes"], default="all")
    parser.add_argument("--output", type=Path, help="CSV opcional del reporte agregado")
    args = parser.parse_args()
    result = report(args.group, args.smoker)
    print(result.to_string(index=False, float_format=lambda n: f"{n:,.2f}"))
    print("\nUSD anuales. Asociaciones observadas; estimación agregada exploratoria. n<20 requiere cautela.")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()

"""Ejecutar desde la raíz: python -m src.analysis.

El modelo describe asociaciones y costos medios por grupo. No está autorizado
para tarificación individual ni permite inferir efectos causales.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from datetime import datetime
from importlib.metadata import version
from pathlib import Path
from zoneinfo import ZoneInfo

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit, StratifiedGroupKFold
from statsmodels.stats.diagnostic import het_breuschpagan

SEED = 42
ROOT = Path(__file__).resolve().parents[1]
COLUMNS = ["age", "sex", "bmi", "children", "smoker", "region", "charges"]
FORMULAS = {
    "M1_aditivo": "log_charges ~ age + C(sex) + bmi_c + children + C(smoker) + C(region)",
    "M2_interaccion": "log_charges ~ age + C(sex) + bmi_c * C(smoker) + children + C(region)",
}
COLORS = ["#186F75", "#D17A45", "#496783", "#73737E"]


def dump_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")


def validate_data(df):
    """Rechaza entradas incompatibles. Nunca elimina filas de forma silenciosa."""
    if list(df.columns) != COLUMNS:
        raise ValueError(f"Columnas esperadas (en orden): {COLUMNS}")
    if df.empty or df.isna().any().any():
        raise ValueError("La base está vacía o contiene valores nulos")
    for col in ["age", "bmi", "children", "charges"]:
        if not pd.api.types.is_numeric_dtype(df[col]) or not np.isfinite(df[col]).all():
            raise ValueError(f"{col} debe ser numérica y finita")
    if not df["age"].between(0, 120).all() or not (df["age"] % 1 == 0).all():
        raise ValueError("Edad fuera de dominio")
    if not df["bmi"].between(10, 100).all():
        raise ValueError("IMC fuera del dominio de validación")
    if not df["children"].between(0, 20).all() or not (df["children"] % 1 == 0).all():
        raise ValueError("Número de hijos fuera de dominio")
    if not (df["charges"] > 0).all():
        raise ValueError("charges debe ser positiva para aplicar logaritmo")
    for col, allowed in {"sex": {"female", "male"}, "smoker": {"no", "yes"},
                         "region": {"northeast", "northwest", "southeast", "southwest"}}.items():
        if not set(df[col]).issubset(allowed):
            raise ValueError(f"Categorías no reconocidas en {col}")
    return True


def prepare(df):
    validate_data(df)
    out = df.copy()
    out["row_id"] = np.arange(len(out))
    # Incluir todas las columnas de origen mantiene juntas copias exactas.
    out["duplicate_group"] = pd.util.hash_pandas_object(df[COLUMNS], index=False).astype(str)
    out["log_charges"] = np.log(out["charges"])
    out["bmi_c"] = out["bmi"] - 30.0
    out["bmi_group"] = np.where(out["bmi"] >= 30, "IMC >= 30", "IMC < 30")
    out["age_group"] = pd.cut(out["age"], [-1, 29, 44, 120], labels=["18-29", "30-44", "45-64"]).astype(str)
    out["children_group"] = np.where(out["children"] >= 3, "3 o más", out["children"].astype(int).astype(str))
    return out


def build_splits(df):
    splitter = GroupShuffleSplit(n_splits=1, test_size=.20, random_state=SEED)
    train_idx, test_idx = next(splitter.split(df, groups=df["duplicate_group"]))
    train, test = df.iloc[train_idx].copy(), df.iloc[test_idx].copy()
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    folds = list(cv.split(train, train["smoker"], train["duplicate_group"]))
    assert not set(train["duplicate_group"]) & set(test["duplicate_group"])
    for fit_idx, val_idx in folds:
        assert not set(train.iloc[fit_idx]["duplicate_group"]) & set(train.iloc[val_idx]["duplicate_group"])
    return train, test, folds


def fit_model(frame, name):
    fitted = smf.ols(FORMULAS[name], data=frame).fit(cov_type="HC3")
    # La media del costo original no equivale a exp(media log). Duan por
    # tabaquismo admite distribuciones de error diferentes entre esos grupos.
    residual_exp = pd.Series(np.exp(fitted.resid), index=frame.index)
    factors = residual_exp.groupby(frame["smoker"]).mean().to_dict()
    factors["global"] = float(residual_exp.mean())
    return {"model": fitted, "smearing": factors, "name": name}


def predict_cost(bundle, frame):
    log_pred = np.asarray(bundle["model"].predict(frame))
    factors = frame["smoker"].map(bundle["smearing"]).fillna(bundle["smearing"]["global"]).to_numpy()
    return np.exp(log_pred) * factors


def scores(y, pred, log_pred=None):
    result = {"mae_usd": float(mean_absolute_error(y, pred)),
              "rmse_usd": float(np.sqrt(mean_squared_error(y, pred))),
              "r2_usd": float(r2_score(y, pred)),
              "bias_usd": float(np.mean(np.asarray(pred) - np.asarray(y)))}
    if log_pred is not None:
        result["r2_log"] = float(r2_score(np.log(y), log_pred))
    return result


def aggregate(frame, group_columns, expected=None):
    tmp = frame.copy()
    if expected is not None:
        tmp["expected"] = expected
    result = tmp.groupby(group_columns, observed=True, dropna=False).agg(
        n=("charges", "size"), charges_sum=("charges", "sum"),
        charges_mean=("charges", "mean"), charges_median=("charges", "median"),
        charges_std=("charges", "std"))
    if expected is not None:
        result["expected_sum"] = tmp.groupby(group_columns, observed=True)["expected"].sum()
        result["expected_mean"] = result["expected_sum"] / result["n"]
    result["se_mean"] = result["charges_std"] / np.sqrt(result["n"])
    result["ci95_low"] = (result["charges_mean"] - 1.96 * result["se_mean"]).clip(lower=0)
    result["ci95_high"] = result["charges_mean"] + 1.96 * result["se_mean"]
    result["small_group"] = result["n"] < 20
    return result.reset_index()


def contrasts(bundle):
    fit = bundle["model"]
    params = fit.params
    names = list(params.index)
    rows = []
    def add(label, terms):
        v = np.array([terms.get(n, 0.) for n in names])
        beta = float(v @ params)
        se = float(np.sqrt(v @ fit.cov_params() @ v))
        z = beta / se
        lo, hi = beta - 1.96 * se, beta + 1.96 * se
        rows.append({"comparison": label, "log_effect": beta, "robust_se_hc3": se,
                     "percent_change": 100 * np.expm1(beta), "ci95_percent_low": 100 * np.expm1(lo),
                     "ci95_percent_high": 100 * np.expm1(hi), "p_value_hc3": float(2 * st.norm.sf(abs(z)))})
    add("Edad: +1 año", {"age": 1})
    add("Hijos: +1", {"children": 1})
    add("Sexo: male frente a female", {"C(sex)[T.male]": 1})
    add("IMC: +1 en no fumadores", {"bmi_c": 1})
    add("IMC: +1 en fumadores", {"bmi_c": 1, "bmi_c:C(smoker)[T.yes]": 1})
    for bmi in [20, 25, 30, 35, 40]:
        add(f"Fumador frente a no fumador con IMC {bmi}",
            {"C(smoker)[T.yes]": 1, "bmi_c:C(smoker)[T.yes]": bmi - 30})
    for region in ["northwest", "southeast", "southwest"]:
        add(f"Región {region} frente a northeast", {f"C(region)[T.{region}]": 1})
    return pd.DataFrame(rows)


def figures(frame, selected, comparison, out):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "figure.facecolor": "white", "axes.labelcolor": "#22333B"})
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].hist(frame.charges, bins=35, color=COLORS[0], alpha=.9)
    axes[0].axvline(frame.charges.mean(), color=COLORS[1], label=f"Media {frame.charges.mean():,.0f}")
    axes[0].axvline(frame.charges.median(), color=COLORS[2], linestyle="--", label=f"Mediana {frame.charges.median():,.0f}")
    axes[0].set(xlabel="Costo anual observado (USD)", ylabel="Afiliados", title="Distribución asimétrica del costo")
    axes[0].legend(fontsize=9)
    for smoker, color, label in [("no", COLORS[0], "No fumadores"), ("yes", COLORS[1], "Fumadores")]:
        sub = frame[frame.smoker == smoker]
        axes[1].scatter(sub.bmi, sub.charges, c=color, s=12, alpha=.45, label=label)
    axes[1].set(xlabel="IMC", ylabel="Costo anual observado (USD)", title="La relación con IMC varía por tabaquismo")
    axes[1].legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(out / "01_eda_costos.png", dpi=180)
    plt.close(fig)

    fit = selected["model"]
    resid = np.asarray(fit.resid)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].scatter(fit.fittedvalues, resid, s=10, alpha=.45, c=COLORS[0])
    axes[0].axhline(0, c=COLORS[1], lw=1)
    axes[0].set(xlabel="Valor ajustado log(costo)", ylabel="Residuo log", title="Residuos frente a valores ajustados")
    st.probplot(resid, dist="norm", plot=axes[1])
    axes[1].set(title="Gráfico Q-Q de residuos", xlabel="Cuantiles teóricos", ylabel="Residuos ordenados")
    fig.tight_layout()
    fig.savefig(out / "02_diagnosticos.png", dpi=180)
    plt.close(fig)

    costs = aggregate(frame, ["smoker", "bmi_group"])
    fig, ax = plt.subplots(figsize=(8, 4.4))
    labels = [("Fumadores" if r.smoker == "yes" else "No fumadores") + "\n" + r.bmi_group for r in costs.itertuples()]
    bars = ax.bar(labels, costs.charges_mean, color=[COLORS[1] if s == "yes" else COLORS[0] for s in costs.smoker])
    for bar, row in zip(bars, costs.itertuples()):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+600, f"{row.charges_mean:,.0f}\nn={row.n}", ha="center", fontsize=10)
    ax.set(ylabel="Media observada anual (USD)", title="Segmentos para presupuesto y prevención", ylim=(0, costs.charges_mean.max()*1.22))
    fig.tight_layout()
    fig.savefig(out / "03_costos_grupo.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    chart_labels = comparison["model"].replace({"Baseline_media": "Media global", "M1_aditivo": "M1 aditivo", "M2_interaccion": "M2 interacción"})
    ax.bar(chart_labels, comparison["cv_mae_usd"], color=COLORS[:len(comparison)])
    for idx, row in comparison.iterrows():
        ax.text(idx, row.cv_mae_usd+100, f"{row.cv_mae_usd:,.0f}", ha="center")
    ax.set(ylabel="MAE en USD, menor es mejor", title="Validación cruzada de 5 particiones en entrenamiento")
    fig.tight_layout()
    fig.savefig(out / "04_comparacion_modelos.png", dpi=180)
    plt.close(fig)


def run(data_path=None, output_root=ROOT):
    started = time.perf_counter()
    output_root = Path(output_root)
    data_path = Path(data_path or ROOT / "data/raw/insurance.csv")
    for folder in ["data/processed", "models", "results/figures", "results/logs"]:
        (output_root / folder).mkdir(parents=True, exist_ok=True)
    out = output_root / "results"
    raw = pd.read_csv(data_path)
    df = prepare(raw)
    df.to_csv(output_root / "data/processed/insurance_validated.csv", index=False)
    train, test, folds = build_splits(df)
    split_manifest = df[["row_id", "duplicate_group", "smoker"]].copy()
    split_manifest["split"] = np.where(split_manifest.row_id.isin(train.row_id), "train", "holdout")
    split_manifest["cv_validation_fold"] = pd.Series([pd.NA]*len(df), dtype="Int64")
    fold_results, oof_records, comparison = [], [], []
    for fold, (_, val_idx) in enumerate(folds, 1):
        split_manifest.loc[train.iloc[val_idx].row_id, "cv_validation_fold"] = fold
    split_manifest.to_csv(out / "split_manifest.csv", index=False)
    fits = {}
    for name in ["Baseline_media", *FORMULAS]:
        records = []
        for fold, (fit_idx, val_idx) in enumerate(folds, 1):
            fit_frame, val = train.iloc[fit_idx], train.iloc[val_idx]
            if name == "Baseline_media":
                pred = np.repeat(fit_frame.charges.mean(), len(val))
                log_pred = np.repeat(fit_frame.log_charges.mean(), len(val))
            else:
                bundle = fit_model(fit_frame, name)
                pred = predict_cost(bundle, val)
                log_pred = bundle["model"].predict(val)
            fold_results.append({"model": name, "fold": fold, "n_train": len(fit_frame), "n_validation": len(val),
                                 **scores(val.charges, pred, log_pred)})
            for rid, truth, est, lp in zip(val.row_id, val.charges, pred, log_pred):
                record = {"model": name, "fold": fold, "row_id": int(rid), "observed": float(truth), "estimated": float(est), "estimated_log": float(lp)}
                records.append(record)
                oof_records.append(record)
        oof = pd.DataFrame(records)
        score = scores(oof.observed, oof.estimated, oof.estimated_log)
        if name in FORMULAS:
            fits[name] = fit_model(train, name)
            aic = float(fits[name]["model"].aic)
        else:
            aic = None
        comp = {"model": name, "aic_train_log": aic, **{"cv_" + key: value for key, value in score.items()}}
        comparison.append(comp)
    comparison = pd.DataFrame(comparison)
    chosen = comparison[comparison.model.isin(FORMULAS)].sort_values("cv_mae_usd").iloc[0].model
    selected = fits[chosen]
    prediction = predict_cost(selected, test)
    test_score = scores(test.charges, prediction, selected["model"].predict(test))
    baseline_test = scores(test.charges, np.repeat(train.charges.mean(), len(test)))
    holdout_records = test[["row_id", "smoker", "bmi_group", "age_group", "region", "charges"]].copy()
    holdout_records["estimated"] = prediction
    holdout_records["error"] = prediction - test.charges
    holdout_records.to_csv(out / "holdout_predictions.csv", index=False)
    pd.DataFrame(fold_results).to_csv(out / "cv_folds.csv", index=False)
    pd.DataFrame(oof_records).to_csv(out / "cv_predictions.csv", index=False)
    comparison.to_csv(out / "model_comparison.csv", index=False)
    # Persistimos el modelo entrenado sin incorporar el holdout.
    joblib.dump(selected, output_root / "models/factors_model.joblib")
    model = selected["model"]
    table = pd.DataFrame({"term": model.params.index, "coefficient_log": model.params.values,
                          "robust_se_hc3": model.bse.values, "p_value_hc3": model.pvalues.values,
                          "ci95_log_low": model.conf_int()[0].values, "ci95_log_high": model.conf_int()[1].values})
    table.to_csv(out / "coefficients.csv", index=False)
    effects = contrasts(selected)
    effects.to_csv(out / "effects.csv", index=False)
    bp_lm, bp_p, bp_f, bp_fp = het_breuschpagan(model.resid, model.model.exog)
    jb = st.jarque_bera(model.resid)
    influence = model.get_influence()
    cooks = influence.cooks_distance[0]
    diagnostics = {"sample": "entrenamiento", "n": len(train),
                   "breusch_pagan": {"lm": float(bp_lm), "p_value": float(bp_p)},
                   "jarque_bera": {"statistic": float(jb.statistic), "p_value": float(jb.pvalue)},
                   "p_value_note": "Un p-valor calculado como 0.0 indica subdesbordamiento numérico, no probabilidad exactamente cero.",
                   "condition_number": float(model.condition_number),
                   "max_cooks_distance": float(cooks.max()), "n_cooks_above_4_over_n": int((cooks > 4/len(train)).sum()),
                   "interpretation": "Revisar p-valores y gráficos. Se utilizan errores estándar HC3. La normalidad/varianza constante pueden fallar. La independencia entre afiliados no puede verificarse sin identificadores. Asociación observacional, sin causalidad."}
    dump_json(out / "residual_diagnostics.json", diagnostics)
    expected = predict_cost(selected, df)
    group_outputs = []
    for cols in [["smoker"], ["smoker", "bmi_group"], ["smoker", "age_group"], ["smoker", "region"], ["smoker", "children_group"]]:
        agg = aggregate(df, cols, expected)
        agg["group_dimensions"] = ",".join(cols)
        group_outputs.append(agg)
    groups = pd.concat(group_outputs, ignore_index=True)
    groups.to_csv(out / "group_costs.csv", index=False)
    held_groups = aggregate(holdout_records, ["smoker"], prediction)
    held_groups["relative_budget_error"] = (held_groups.expected_sum - held_groups.charges_sum) / held_groups.charges_sum
    held_groups.to_csv(out / "holdout_group_validation.csv", index=False)
    costs = raw.charges.sort_values(ascending=False)
    top_n = int(np.ceil(.10*len(raw)))
    quality = {"rows_raw": len(raw), "rows_validated": len(df), "columns_raw": len(raw.columns),
               "missing_values": int(raw.isna().sum().sum()), "duplicate_excess_rows": int(raw.duplicated().sum()),
               "duplicate_policy": "Conservar 1338 registros de referencia (E2); mantener copias exactas en el mismo split/fold.",
               "duplicate_group_overlap_train_holdout": 0, "negative_or_zero_charges": int((raw.charges <= 0).sum()),
               "sha256_input": hashlib.sha256(data_path.read_bytes()).hexdigest(),
               "ranges": {c: {"min": float(raw[c].min()), "max": float(raw[c].max())} for c in ["age", "bmi", "children", "charges"]}}
    dump_json(out / "data_quality.json", quality)
    raw.describe(include="all").to_csv(out / "descriptive_statistics.csv")
    summary = {"n": len(df), "mean_cost_usd": float(df.charges.mean()), "median_cost_usd": float(df.charges.median()),
               "total_cost_usd": float(df.charges.sum()), "smokers_n": int((df.smoker == "yes").sum()),
               "smokers_share": float((df.smoker == "yes").mean()),
               "smokers_cost_share": float(df.loc[df.smoker == "yes", "charges"].sum()/df.charges.sum()),
               "top_10pct_n": top_n, "top_10pct_cost_share": float(costs.head(top_n).sum()/costs.sum()),
               "cost_over_20000_share": float((df.charges > 20000).mean())}
    metrics = {"seed": SEED, "selection_rule": "Menor MAE USD OOF en CV de 5 folds de entrenamiento; AIC log como evidencia complementaria.",
               "selected_model": chosen, "formulas": FORMULAS, "n_train": len(train), "n_holdout": len(test),
               "group_split": "Copias exactas nunca se separan. GroupShuffleSplit 20%; CV StratifiedGroupKFold por smoker.",
               "model_comparison": comparison.where(comparison.notna(), None).astype(object).where(pd.notna(comparison), None).to_dict("records"),
               "holdout_selected": test_score, "holdout_baseline": baseline_test,
               "mae_reduction_vs_baseline_holdout": float(1-test_score["mae_usd"]/baseline_test["mae_usd"]),
               "smearing_train": {k: float(v) for k, v in selected["smearing"].items()}, "summary": summary,
               "planned_mae_reference_usd": 4824., "cv_mae_meets_reference": bool(comparison.loc[comparison.model == chosen, "cv_mae_usd"].iloc[0] <= 4824),
               "elapsed_seconds": time.perf_counter()-started,
               "executed_at_santiago": datetime.now(ZoneInfo("America/Santiago")).isoformat(),
               "python": platform.python_version(),
               "versions": {p: version(p) for p in ["pandas", "numpy", "scipy", "scikit-learn", "statsmodels", "matplotlib", "joblib"]}}
    dump_json(out / "metrics.json", metrics)
    dashboard = {"metadata": {"source": "insurance.csv, referencia pública Kaggle", "unit": "USD por año", "model": chosen,
                              "min_n": 5, "small_group_warning_n": 20,
                              "expected_definition": "Estimación media con modelo log y smearing por tabaquismo entrenado sin holdout. Ajuste descriptivo al conjunto, no validación externa.",
                              "warning": "Asociaciones observacionales. No usar para tarificación individual. Muestra pública sin representatividad acreditada."},
                 "summary": summary, "filters": {"smoker": ["all", "no", "yes"]}, "comparisons": {}}
    for smoker in ["all", "no", "yes"]:
        mask = np.ones(len(df), dtype=bool) if smoker == "all" else (df.smoker == smoker).to_numpy()
        sub, estimates = df.loc[mask], expected[mask]
        dashboard["comparisons"][smoker] = {}
        for label, column in {"bmi": "bmi_group", "age": "age_group", "region": "region", "children": "children_group"}.items():
            agg = aggregate(sub, [column], estimates).rename(columns={column: "group"})
            agg = agg.loc[agg.n >= 5, ["group", "n", "charges_sum", "expected_sum", "charges_mean", "expected_mean", "small_group"]]
            dashboard["comparisons"][smoker][label] = agg.to_dict("records")
    dump_json(out / "dashboard_groups.json", dashboard)
    figures(df, selected, comparison, out / "figures")
    dump_json(out / "logs/execution.json", {"event": "pipeline_completed", "timestamp": metrics["executed_at_santiago"],
                                           "input_sha256": quality["sha256_input"], "selected_model": chosen,
                                           "artifacts": ["metrics.json", "model_comparison.csv", "effects.csv", "group_costs.csv", "residual_diagnostics.json", "dashboard_groups.json"],
                                           "note": "Registro de ejecución de esta sesión, no evidencia de semanas previas."})
    return metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "data/raw/insurance.csv")
    args = parser.parse_args()
    metrics = run(args.data)
    print(json.dumps({key: metrics[key] for key in ["selected_model", "n_train", "n_holdout", "holdout_selected", "mae_reduction_vs_baseline_holdout"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

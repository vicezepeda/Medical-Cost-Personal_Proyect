"""Reentrena el simulador EP6 con la partición y el control de calidad existentes."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.analysis import (
    FORMULAS, ROOT, SEED, build_splits, dump_json, fit_model, predict_cost, prepare, scores,
)
from src.predictor import FEATURES, estimate

NUMERIC = ["age", "bmi", "children"]
CATEGORICAL = ["sex", "smoker", "region"]
LINEAR = "Lineal_USD"
BASELINE = "Media_entrenamiento"
TARGET_MAE = 4824.0


def make_pipeline():
    return Pipeline([
        ("preprocessor", ColumnTransformer([
            ("numeric", StandardScaler(), NUMERIC),
            ("categorical", OneHotEncoder(drop="first", handle_unknown="error"), CATEGORICAL),
        ])),
        ("regression", LinearRegression()),
    ])


def evaluate_cv(train, folds):
    records = []
    for name in [BASELINE, LINEAR, *FORMULAS]:
        oof = np.empty(len(train))
        for fit_indices, validation_indices in folds:
            fit = train.iloc[fit_indices]
            validation = train.iloc[validation_indices]
            if name == BASELINE:
                prediction = fit.charges.mean()
            elif name == LINEAR:
                pipeline = make_pipeline().fit(fit[FEATURES], fit.charges)
                prediction = estimate(pipeline, validation)
            else:
                prediction = predict_cost(fit_model(fit, name), validation)
            oof[validation_indices] = prediction
        records.append({"model": name, **scores(train.charges, oof)})
    return records


def train_model(data_path=ROOT / "data/raw/insurance.csv", output_root=ROOT):
    """Ajusta el producto lineal y registra comparaciones en la escala original."""
    raw = pd.read_csv(data_path)
    data = prepare(raw)
    train, test, folds = build_splits(data)
    comparison = evaluate_cv(train, folds)
    linear_cv = next(row["mae_usd"] for row in comparison if row["model"] == LINEAR)

    pipeline = make_pipeline().fit(train[FEATURES], train.charges)
    prediction = estimate(pipeline, test)
    baseline = np.full(len(test), train.charges.mean())
    holdout = scores(test.charges, prediction)
    baseline_holdout = scores(test.charges, baseline)
    groups = []
    for feature in CATEGORICAL:
        for category in sorted(test[feature].unique()):
            mask = test[feature] == category
            groups.append({
                "variable": feature, "group": category, "n": int(mask.sum()),
                **scores(test.loc[mask, "charges"], prediction[mask]),
            })

    def negative_served_mae(estimator, inputs, target):
        return -float(np.abs(np.asarray(target) - estimate(estimator, inputs)).mean())

    importance = permutation_importance(
        pipeline, test[FEATURES], test.charges, scoring=negative_served_mae,
        n_repeats=20, random_state=SEED,
    )
    metrics = {
        "model": LINEAR, "seed": SEED, "n_rows": len(data), "n_train": len(train),
        "n_test": len(test), "missing_cells": int(raw.isna().sum().sum()),
        "exact_duplicates": int(raw.duplicated().sum()), "cv": comparison,
        "mae_reference_usd": TARGET_MAE, "cv_linear_mae_usd": linear_cv,
        "holdout": holdout, "holdout_baseline": baseline_holdout,
        "holdout_mae_reduction": 1 - holdout["mae_usd"] / baseline_holdout["mae_usd"],
        "holdout_group_metrics": groups,
        "holdout_permutation_importance": [
            {"feature": feature, "mean_mae_increase_usd": float(mean), "sd_usd": float(sd)}
            for feature, mean, sd in zip(FEATURES, importance.importances_mean, importance.importances_std)
        ],
        "holdout_baseline_mean_usd": float(baseline[0]),
        "holdout_underestimation_baseline_usd": float(np.maximum(test.charges - baseline, 0).mean()),
        "holdout_underestimation_model_usd": float(np.maximum(test.charges - prediction, 0).mean()),
        "holdout_predictions_clipped": int((pipeline.predict(test[FEATURES]) < 0).sum()),
    }
    output_root = Path(output_root)
    for folder in ("models", "results"):
        (output_root / folder).mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, output_root / "models/medicalcost.joblib", compress=3)
    dump_json(output_root / "results/medicalcost_metrics.json", metrics)
    print(f"Modelo guardado. MAE CV: USD {linear_cv:,.2f}. MAE prueba: USD {holdout['mae_usd']:,.2f}.")
    return metrics


if __name__ == "__main__":
    train_model()

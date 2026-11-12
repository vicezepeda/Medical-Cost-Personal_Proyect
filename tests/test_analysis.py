"""Controles sobre integridad, ausencia de fuga y resultados del entregable."""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

from src.analysis import aggregate, build_splits, predict_cost, prepare, validate_data
from src.cli import report

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def frame():
    return prepare(pd.read_csv(ROOT / "data/raw/insurance.csv"))


def test_preserves_reference_and_keeps_duplicate_together(frame):
    assert len(frame) == 1338
    assert frame.duplicate_group.nunique() == 1337
    train, test, folds = build_splits(frame)
    assert not set(train.duplicate_group) & set(test.duplicate_group)
    assert len(train) + len(test) == len(frame)
    validation_rows = []
    for fit_idx, val_idx in folds:
        assert not set(train.iloc[fit_idx].duplicate_group) & set(train.iloc[val_idx].duplicate_group)
        validation_rows.extend(train.iloc[val_idx].row_id.tolist())
    assert sorted(validation_rows) == sorted(train.row_id.tolist())


def test_invalid_target_and_unrecognized_category_rejected():
    raw = pd.read_csv(ROOT / "data/raw/insurance.csv")
    invalid = raw.copy()
    invalid.loc[0, "charges"] = 0
    with pytest.raises(ValueError, match="positiva"):
        validate_data(invalid)
    invalid = raw.copy()
    invalid.loc[0, "smoker"] = "maybe"
    with pytest.raises(ValueError, match="Categorías"):
        validate_data(invalid)


def test_aggregate_reconciles_total_and_weighted_mean(frame):
    groups = aggregate(frame, ["smoker", "bmi_group"])
    assert groups.n.sum() == len(frame)
    assert groups.charges_sum.sum() == pytest.approx(frame.charges.sum())
    assert np.average(groups.charges_mean, weights=groups.n) == pytest.approx(frame.charges.mean())


def test_artifacts_match_oof_and_exclude_holdout(frame):
    metrics = json.loads((ROOT / "results/metrics.json").read_text(encoding="utf-8"))
    manifest = pd.read_csv(ROOT / "results/split_manifest.csv")
    predictions = pd.read_csv(ROOT / "results/cv_predictions.csv")
    held = set(manifest.loc[manifest.split == "holdout", "row_id"])
    assert not held & set(predictions.row_id)
    selected = predictions[predictions.model == metrics["selected_model"]]
    independently_computed_mae = (selected.observed-selected.estimated).abs().mean()
    declared = next(r["cv_mae_usd"] for r in metrics["model_comparison"] if r["model"] == metrics["selected_model"])
    assert independently_computed_mae == pytest.approx(declared)


def test_cli_and_dashboard_only_publish_sufficient_groups():
    assert (report().n >= 5).all()
    with pytest.raises(ValueError):
        report("row_id")
    data = json.loads((ROOT / "results/dashboard_groups.json").read_text(encoding="utf-8"))
    for tables in data["comparisons"].values():
        for rows in tables.values():
            assert all(row["n"] >= 5 for row in rows)


def test_persisted_model_reproduces_reserved_predictions(frame):
    model = joblib.load(ROOT / "models/factors_model.joblib")
    held = pd.read_csv(ROOT / "results/holdout_predictions.csv")
    reloaded = predict_cost(model, frame.loc[frame.row_id.isin(held.row_id)])
    assert np.allclose(reloaded, held.estimated, rtol=1e-10)

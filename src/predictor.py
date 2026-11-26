"""Contrato de datos e inferencia compartido por FastAPI y Streamlit."""
from pathlib import Path
from typing import Literal

import joblib
import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field

FEATURES = ["age", "sex", "bmi", "children", "smoker", "region"]
MODEL_PATH = Path(__file__).resolve().parents[1] / "models/medicalcost.joblib"


class Profile(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    age: int = Field(ge=18, le=64)
    sex: Literal["female", "male"]
    bmi: float = Field(ge=15.96, le=53.13, allow_inf_nan=False)
    children: int = Field(ge=0, le=5)
    smoker: Literal["yes", "no"]
    region: Literal["northeast", "northwest", "southeast", "southwest"]


def load_model():
    return joblib.load(MODEL_PATH)


def estimate(model, frame):
    return np.maximum(model.predict(frame[FEATURES]), 0.0)


def predict_profile(model, profile):
    return round(float(estimate(model, pd.DataFrame([profile.model_dump()]))[0]), 2)

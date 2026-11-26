"""Ejecutar desde la raíz: uvicorn api:app --reload."""
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, Request
from pydantic import BaseModel

from src.predictor import Profile, load_model, predict_profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    yield


app = FastAPI(title="MedicalCost Predictor", version="1.0.0", lifespan=lifespan)


class Health(BaseModel):
    status: Literal["ok"]


class Prediction(BaseModel):
    predicted_charges: float


@app.get("/health", response_model=Health)
def health():
    return Health(status="ok")


@app.post("/predict", response_model=Prediction)
def predict(profile: Profile, request: Request):
    return Prediction(predicted_charges=predict_profile(request.app.state.model, profile))

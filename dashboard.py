"""Ejecutar desde la raíz: streamlit run dashboard.py."""
import json
import os

import altair as alt
import httpx
import pandas as pd
import streamlit as st

from src.analysis import ROOT
from src.predictor import Profile, load_model, predict_profile

REGIONS = {
    "northeast": "Noreste", "northwest": "Noroeste",
    "southeast": "Sureste", "southwest": "Suroeste",
}
LABELS = {"age": "Edad", "sex": "Sexo", "bmi": "IMC", "children": "Hijos",
          "smoker": "Tabaquismo", "region": "Región"}


@st.cache_data
def read_data():
    data = pd.read_csv(ROOT / "data/raw/insurance.csv")
    metrics = json.loads((ROOT / "results/medicalcost_metrics.json").read_text(encoding="utf-8"))
    return data, metrics


@st.cache_resource
def get_model():
    return load_model()


def show_analysis(data, metrics):
    chart_data = data.assign(
        tabaquismo=data.smoker.map({"yes": "Fumador", "no": "No fumador"})
    )
    st.subheader("Distribución de cargos por tabaquismo")
    st.altair_chart(
        alt.Chart(chart_data).mark_bar(opacity=0.65, binSpacing=0).encode(
            x=alt.X("charges:Q", bin=alt.Bin(step=2500), title="Cargos observados (USD)"),
            y=alt.Y("count():Q", title="Registros", stack=None),
            color=alt.Color("tabaquismo:N", title=None, scale=alt.Scale(
                domain=["No fumador", "Fumador"], range=["#07968d", "#d36734"]
            )),
            tooltip=[alt.Tooltip("count():Q", title="Registros")],
        ),
        width="stretch",
    )
    st.subheader("Importancia de las variables en la prueba")
    importance = pd.DataFrame(metrics["holdout_permutation_importance"])
    importance["variable"] = importance.feature.map(LABELS)
    st.altair_chart(
        alt.Chart(importance).mark_bar(color="#07968d").encode(
            x=alt.X("mean_mae_increase_usd:Q", title="Cambio promedio del MAE (USD)"),
            y=alt.Y("variable:N", title=None, sort="-x"),
            tooltip=[alt.Tooltip("variable:N"), alt.Tooltip("mean_mae_increase_usd:Q", format=".2f")],
        ),
        width="stretch",
    )
    st.caption("Variación del error al permutar cada variable. La medida depende de esta muestra y del modelo.")


def show_simulator():
    st.subheader("Simulador de cargos")
    cols = st.columns(3)
    age = cols[0].slider("Edad", 18, 64, 30)
    bmi = cols[1].number_input("IMC", 15.96, 53.13, 25.0, step=0.01)
    children = cols[2].slider("Número de hijos", 0, 5, 0)
    sex = cols[0].selectbox("Sexo", ["male", "female"], format_func={"male": "Masculino", "female": "Femenino"}.get)
    smoker = cols[1].selectbox("Fumador", ["no", "yes"], format_func={"no": "No", "yes": "Sí"}.get)
    region = cols[2].selectbox("Región", list(REGIONS), format_func=REGIONS.get)
    profile = Profile(age=age, sex=sex, bmi=bmi, children=children, smoker=smoker, region=region)

    mode = st.radio("Origen de la predicción", ["Modelo local", "API REST"], horizontal=True)
    if mode == "Modelo local":
        st.metric("Cargo estimado", f"USD {predict_profile(get_model(), profile):,.2f}")
    else:
        api_url = os.getenv("MEDICALCOST_API_URL", "http://127.0.0.1:8000").rstrip("/")
        if st.button("Consultar API", type="primary"):
            try:
                response = httpx.post(f"{api_url}/predict", json=profile.model_dump(), timeout=5.0)
                response.raise_for_status()
                prediction = float(response.json()["predicted_charges"])
            except (httpx.HTTPError, ValueError, KeyError, TypeError):
                st.error("No se pudo consultar la API. Comprueba que esté iniciada o selecciona el modelo local.")
            else:
                st.metric("Cargo estimado", f"USD {prediction:,.2f}", help="Resultado devuelto por POST /predict.")
    st.caption("Prototipo académico. Los cargos se expresan en USD y las estimaciones requieren validación con una cartera real.")


def main():
    st.set_page_config(page_title="MedicalCost Predictor", page_icon="📊", layout="wide")
    try:
        data, metrics = read_data()
        get_model()
    except FileNotFoundError:
        st.error("Falta el modelo o sus resultados. Ejecuta python train.py desde la raíz del repositorio.")
        st.stop()

    st.title("MedicalCost Predictor")
    st.caption(f"Regresión lineal · Evaluación en {metrics['n_test']} observaciones de prueba")
    holdout = metrics["holdout"]
    cols = st.columns(3)
    cols[0].metric("RMSE de prueba", f"USD {holdout['rmse_usd']:,.0f}")
    cols[1].metric("MAE de prueba", f"USD {holdout['mae_usd']:,.0f}")
    cols[2].metric("R² de prueba", f"{holdout['r2_usd']:.3f}")
    simulator, analysis, plan = st.tabs(["Simulador", "Análisis de datos", "Plan y ejecución"])
    with simulator:
        show_simulator()
    with analysis:
        show_analysis(data, metrics)
    with plan:
        planned = metrics["mae_reference_usd"]
        real = metrics["cv_linear_mae_usd"]
        st.subheader("Referencia de MAE en validación cruzada")
        st.table(pd.DataFrame([{
            "Meta máxima (USD)": f"{planned:,.2f}",
            "MAE obtenido (USD)": f"{real:,.2f}",
            "Brecha (USD)": f"{real - planned:+,.2f}",
            "Resultado": "Cumple" if real <= planned else "Pendiente de mejora",
        }]))
        st.caption("Referencia conservada del plan EP4. El MAE de prueba se reporta por separado.")
        st.link_button("Ver hitos y tareas en Linear", "https://linear.app/duocuc2026/project/medicalcost-predictor-ep6-b503ee94e0e0")


if __name__ == "__main__":
    main()

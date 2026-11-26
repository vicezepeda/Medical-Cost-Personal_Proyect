# MedicalCost Predictor · extensión EP6

Prototipo académico de predicción de cargos en USD. Reutiliza el CSV, el
perfilado y las particiones del estudio anterior y conserva su dashboard
descriptivo. El nuevo simulador usa una regresión lineal con preprocesamiento
empaquetado. El [tablero Linear](https://linear.app/duocuc2026/project/medicalcost-predictor-ep6-b503ee94e0e0)
registra hitos y responsables.

Desde la raíz del repositorio, con Python 3.12:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python train.py
python -m pytest -q
```

En terminales independientes con el mismo entorno activado:

```bash
uvicorn api:app --reload
streamlit run dashboard.py
```

- [Simulador y análisis](http://127.0.0.1:8501). El modelo local recalcula al
  cambiar una entrada. Para una demostración HTTP, selecciona **API REST**
  y pulsa **Consultar API**. La variable `MEDICALCOST_API_URL` permite cambiar
  la URL base desde el entorno de Streamlit.
- [Swagger UI](http://127.0.0.1:8000/docs) y [salud](http://127.0.0.1:8000/health).
  Ambos enlaces locales requieren iniciar el servicio correspondiente.
- [Informe ejecutivo](../entregables/MedicalCost_Predictor_Informe_EP6.pdf),
  [presentación](../entregables/MedicalCost_Predictor_Defensa_EP6.pptx) y
  [guion cronometrado](MedicalCost_Predictor_Defensa.md).
- [Resultados experimentales](../results/medicalcost_metrics.json),
  [supuestos económicos](../gestion/medicalcost_roi.csv) y
  [seguimiento por hito](../gestion/MedicalCost_Predictor_Seguimiento.md).

```bash
curl -sS http://127.0.0.1:8000/health
curl -sS http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"age":30,"sex":"male","bmi":25.0,"children":0,"smoker":"no","region":"northeast"}'
```

La respuesta de predicción contiene `predicted_charges` en USD. El contrato
usa los rangos observados en el CSV (edad 18–64, IMC 15,96–53,13, hijos 0–5)
y rechaza entradas fuera del dominio con HTTP 422. La unidad económica
reportada es el cargo del dataset. La proyección anual del informe es un
escenario hipotético. Para repetir el entrenamiento, usa el CSV versionado
y el mismo entorno de dependencias.

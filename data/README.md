# Datos de referencia

- Fuente declarada por el usuario: [Medical Cost Personal Datasets, Miri Choi](https://www.kaggle.com/datasets/mirichoi0218/insurance).
- Archivo de entrada: `raw/insurance.csv`, copia local proporcionada por el estudiante. Se conserva sin modificar y su SHA-256 está en `../results/data_quality.json`.
- Base validada y variables derivadas: `processed/insurance_validated.csv`.
- Diccionario, dominios, unidades y decisiones de limpieza: `../docs/diccionario_datos.md`.

1.338 observaciones del conjunto público de referencia. No corresponde a datos de una aseguradora real ni permite identificar el período de observación. Los costos se presentan en USD y el horizonte anual sigue el supuesto del plan EP4. No se imputan nulos ni se eliminan extremos; no hay nulos y se preserva el duplicado auditado. No se usa esta base para tarificación individual.

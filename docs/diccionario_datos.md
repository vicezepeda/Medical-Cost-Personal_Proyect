# Diccionario y control de la base E2

Fuente: Miri Choi, **Medical Cost Personal Datasets**, [Kaggle](https://www.kaggle.com/datasets/mirichoi0218/insurance). Se utiliza la copia `insurance.csv` proporcionada por el estudiante, sin atribuir una descarga nueva a esta ejecución. El SHA-256 de esa copia se registra en `results/data_quality.json`.

La base contiene **1.338 registros y 7 columnas**, sin nulos. Son observaciones del conjunto público de referencia, no una cartera real proporcionada por una aseguradora chilena. El CSV no incluye fecha, identificadores de paciente, diagnóstico, plan ni medicamentos. El plan EP4 interpreta `charges` como costo anual en USD; la periodicidad no se puede verificar dentro del archivo y debe confirmarse para un uso real.

| Variable original | Tipo leído | Significado | Dominio observado | Uso |
|---|---|---|---|---|
| `age` | entero | Edad del beneficiario principal | 18–64 años | Factor continuo |
| `sex` | texto categórico | Sexo registrado en el conjunto | `female`, `male` | Factor, referencia `female` |
| `bmi` | decimal | Índice de masa corporal | 15,96–53,13 kg/m² | Factor continuo centrado en 30 |
| `children` | entero | Hijos o dependientes cubiertos | 0–5 | Factor continuo y segmentación |
| `smoker` | texto categórico | Tabaquismo registrado | `no`, `yes` | Factor e interacción con IMC |
| `region` | texto categórico | Región de residencia de Estados Unidos | `northeast`, `northwest`, `southeast`, `southwest` | Factor, referencia `northeast` |
| `charges` | decimal | Costos médicos facturados | 1.121,8739–63.770,42801 USD | Variable respuesta positiva |

## Variables derivadas reproducibles

| Variable | Regla | Finalidad |
|---|---|---|
| `row_id` | Posición original entre 0 y 1.337 | Trazabilidad técnica; no identifica una persona |
| `duplicate_group` | Hash de las siete variables de origen, sin índice | Mantener copias exactas en un mismo split y fold |
| `log_charges` | Logaritmo natural de `charges` | Respuesta de los modelos M1 y M2 |
| `bmi_c` | `bmi - 30` | Interpretar el efecto de tabaquismo a IMC 30 |
| `bmi_group` | `bmi < 30` o `bmi >= 30` | Segmentación del plan |
| `age_group` | 18–29, 30–44, 45–64 | Segmentación descriptiva dentro del rango observado |
| `children_group` | 0, 1, 2, 3 o más | Comparación agregada |

## Decisiones de calidad

- Se conserva **una fila duplicada adicional** para respetar el criterio E2 de 1.338 registros. El archivo tiene 1.337 filas únicas. Las copias exactas nunca se reparten entre entrenamiento, validación ni holdout. No se inventa un identificador de afiliado para resolver si son personas distintas.
- El programa rechaza columnas inesperadas, nulos, valores no finitos, categorías desconocidas y costos no positivos. Valida dominios amplios plausibles y no transforma casos costosos en errores de captura sin evidencia.
- Se conservan valores extremos. Los diagnósticos de residuos e influencia se publican, junto con la advertencia sobre su efecto en RMSE y estimación de medias.
- `data/raw/insurance.csv` es inmutable. `data/processed/insurance_validated.csv` conserva las siete columnas y añade las derivadas.
- No existen identificadores directos en el archivo proporcionado. Esto no constituye una certificación de anonimización o cumplimiento legal. Para datos reales de salud se requiere revisión institucional y control de acceso. El dashboard sólo publica agregados con `n >= 5`; `n < 20` se marca como grupo pequeño.

La distribución de sexo y tabaquismo describe lo registrado por esta fuente. No acredita representatividad ni equivale a una evaluación clínica.

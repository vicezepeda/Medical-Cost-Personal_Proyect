# Factores asociados a los costos médicos

Implementación del plan EP4 para **EP5 y EP6**, asignatura SCY1102 Gestión de Proyectos de Datos.

**Estudiante:** Vicente Gabriel Zepeda Rojas. **Docente:** Jorge Alberto Moscoso Santander.

El proyecto estudia asociaciones entre edad, sexo, IMC, hijos, tabaquismo y región con `charges`. Compara dos regresiones de `log(charges)` y entrega estimaciones de costos por grupos. La unidad USD y el horizonte anual siguen el supuesto del plan EP4; el CSV no incluye fechas ni unidad temporal. La muestra pública de referencia no acredita representatividad de una cartera real. El producto no ofrece cotizaciones individuales ni estima ahorros causales.

## Entregas

| Entrega | Archivo |
|---|---|
| EP5, informe de implementación y control | [Informe PDF](entregables/EP5_Informe_Implementacion.pdf) |
| EP6, presentación ejecutiva | [PPTX editable](entregables/EP6_Presentacion.pptx) y [PDF](entregables/EP6_Presentacion.pdf) |
| Exposición de 10 minutos y preparación de defensa | [Guion y preguntas](docs/EP6_guion_y_defensa.md) |
| Evidencia técnica ejecutada | [Notebook](notebooks/01_implementacion.ipynb) |
| Seguimiento real de esta ejecución | [GitHub Issues](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues) y [tablero de corte](gestion/tablero.md) |
| Trazabilidad de pautas y plan | [Matriz de cumplimiento](docs/matriz_cumplimiento.md) |
| Propuesta de evaluación del programa | [Piloto](docs/propuesta_piloto.md) |

## Reproducir el análisis

Python 3.12. Desde la raíz del repositorio:

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.analysis
python -m pytest -q
python dashboard/app.py
```

Abrir `http://127.0.0.1:8501/`. El dashboard permite filtrar tabaquismo y comparar IMC, edad, región e hijos. Muestra sólo agregados y tamaños de muestra. Para usarlo sin servidor, ejecutar `python dashboard/app.py --export` y abrir [dashboard/index.html](dashboard/index.html) descargado localmente. GitHub muestra el código HTML y no lo ejecuta en su visor de archivos.

El notebook incluye salidas de una ejecución real. Las versiones, particiones, semilla 42 y registros de ejecución se conservan junto a los resultados. La selección usa validación cruzada dentro del entrenamiento; la reserva final queda separada. Las filas idénticas permanecen en la misma partición para evitar contaminación.

La prueba opcional de interfaz está en `tests/dashboard_browser.mjs`. Con Node.js instalado, ejecutar `npm install --no-save --package-lock=false playwright@1.62.1` y `npx playwright install chromium`. Mantener el dashboard iniciado y ejecutar en otra terminal `node tests/dashboard_browser.mjs` desde la raíz. Esta prueba verifica las 12 combinaciones, conteos, medias ponderadas, carga local y vista móvil emulada.

La [ejecución de GitHub Actions](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/actions/runs/43133074760) completó la instalación limpia, reprodujo el análisis, aprobó las seis pruebas sobre los artefactos recién generados y exportó el dashboard en Ubuntu. El [registro de esa comprobación](evidence/github_actions.json) incluye el resultado y el artefacto de la ejecución. Las métricas de Windows y Linux coinciden hasta diferencias numéricas de punto flotante.

## Dónde revisar la evidencia

- `data/`: fuente recibida y base preparada, sin sustituir el archivo original.
- `src/`, `tests/`, `models/`: implementación, pruebas y modelo de factores.
- `results/`: control de calidad, comparación M1/M2, diagnósticos, asociaciones y costos grupales.
- `dashboard/`: aplicación Python y vista interactiva local.
- `evidence/`: pruebas, capturas y comprobaciones de esta entrega.
- `gestion/`: plan frente a ejecución, reportes de corte, riesgos, decisiones y acciones correctivas.
- `docs/referencias/`: plan y pautas proporcionadas por el estudiante.

## Estado y límites

Las evidencias corresponden a esta ejecución del **11 de noviembre de 2026, America/Santiago**. No representan un seguimiento realizado durante las doce semanas del plan. Las semanas S2/S4/S7/S9/S12 se conservan como línea base relativa porque no se proporcionó una fecha de inicio confirmada. Las 200 horas y USD 2.519 del plan son estimaciones. No hay partes de horas ni costos reales para calcular desviaciones de gasto, CPI o SPI.

La firma del acta, la validación de representatividad con la aseguradora, la defensa oral y la aprobación del patrocinador requieren evidencia externa y permanecen abiertas. Los entregables documentales no acreditan esas aprobaciones.

El modelo describe asociaciones observacionales. La heterocedasticidad y la falta de normalidad limitan la inferencia clásica. Los errores robustos HC3 no corrigen el diseño de la muestra ni convierten una asociación en causalidad. Las medias ajustadas del dashboard corresponden al modelo entrenado sin la reserva y aplicado de forma descriptiva a la base de referencia; su validación fuera de muestra se consulta por separado en el informe y los resultados.

## Fuentes

- Miri Choi, [Medical Cost Personal Datasets](https://www.kaggle.com/datasets/mirichoi0218/insurance), archivo `insurance.csv` suministrado por el estudiante.
- [Plan EP4](docs/referencias/Plan_EP4.pdf), [pauta EP5](docs/referencias/Pauta_EP5.pdf) y [pauta EP6](docs/referencias/Pauta_EP6.pdf).
- [Statsmodels: errores robustos](https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.OLSResults.get_robustcov_results.html).
- [Scikit-learn: validación cruzada y particiones por grupos](https://scikit-learn.org/stable/modules/cross_validation.html).

El desarrollo y la preparación documental recibieron asistencia de IA. El estudiante debe revisar los resultados, reproducir el proyecto y explicar las decisiones en la defensa.

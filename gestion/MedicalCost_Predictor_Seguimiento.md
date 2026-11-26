# Seguimiento de MedicalCost Predictor · EP6

Corte técnico del 25 de noviembre de 2026, hora de Santiago. Las fechas objetivo
del 26 al 29 de noviembre son estimaciones de planificación del prototipo. La
fecha de exposición la fija el curso. El líder del proyecto es el responsable registrado
en los 13 issues. Los puntos representan esfuerzo relativo.

[Tablero Linear](https://linear.app/duocuc2026/project/medicalcost-predictor-ep6-b503ee94e0e0)

## M1 · Datos y preparación · objetivo 26 de noviembre

- **Plan.** Perfilar el CSV, validar dominios y preservar duplicados, preparar split y CV.
- **Ejecución.** 3 de 3 tareas técnicas verificadas. Hay 1.338 filas, cero celdas nulas, una copia exacta y particiones de 1.069 y 269 filas.
- **Desviación y acción.** La copia exacta se conservó para reproducir el estudio previo. Se agruparon las dos filas tanto en el corte como en los pliegues para evitar que la copia cruzara conjuntos. Se reutilizó el perfilado existente y se adelantó el cierre técnico.
- **Evidencia.** [Calidad de datos](../results/data_quality.json), [split](../results/split_manifest.csv), [DUO-5](https://linear.app/duocuc2026/issue/DUO-5/cargar-y-perfilar-el-dataset), [DUO-7](https://linear.app/duocuc2026/issue/DUO-7/validar-categorias-y-controlar-duplicados), [DUO-15](https://linear.app/duocuc2026/issue/DUO-15/preparar-particion-8020-y-cv).

## M2 · Modelo y evaluación · objetivo 27 de noviembre

- **Plan.** Empaquetar una regresión, evaluar en USD y revisar diferencias por grupo. Meta de MAE CV ≤ USD 4.824, heredada del plan EP4.
- **Ejecución.** 3 de 3 tareas técnicas verificadas. MAE CV USD 4.232,88, USD 591,12 bajo la meta. En prueba el MAE fue USD 4.119,82, RMSE USD 5.883,55 y R² 0,737.
- **Desviación y acción.** El modelo previo de interacción en log-cargos obtenía un MAE CV de USD 5.039,52. Se incorporó regresión directa, que tuvo el menor MAE CV en la comparación. Entre fumadores el error sigue siendo mayor. La siguiente validación debe medir calibración y error por grupo en cartera representativa.
- **Evidencia.** [Entrenamiento](../train.py), [resultados](../results/medicalcost_metrics.json), [DUO-6](https://linear.app/duocuc2026/issue/DUO-6/entrenar-regresion-lineal-y-empaquetar-pipeline), [DUO-12](https://linear.app/duocuc2026/issue/DUO-12/comparar-modelos-y-evaluar-mae-rmse-y-r), [DUO-14](https://linear.app/duocuc2026/issue/DUO-14/revisar-error-por-grupo-y-alcance-del-modelo).

## M3 · API y dashboard · objetivo 28 de noviembre

- **Plan.** Implementar el contrato HTTP, construir el simulador y verificar paridad local y HTTP.
- **Ejecución.** 3 de 3 tareas técnicas verificadas. FastAPI devuelve 200 para salud y predicción y 422 para edad fuera de rango. Las 16 pruebas automatizadas pasaron. Se verificaron recálculo, gráfica, tabla de control y consulta API en Chromium. Ambos modos devuelven USD 4.335,51 para el perfil de demostración.
- **Decisión de alcance.** La demo se ejecuta localmente, tal como permite el encargo. Los enlaces de código, el contrato Swagger, la captura y la prueba HTTP permiten reproducirla.
- **Evidencia.** [API](../api.py), [dashboard](../dashboard.py), [demo](../evidence/medicalcost_demo.json), [captura](../evidence/medicalcost_simulador.jpg), [DUO-11](https://linear.app/duocuc2026/issue/DUO-11/definir-esquema-pydantic-e-implementar-api), [DUO-8](https://linear.app/duocuc2026/issue/DUO-8/implementar-dashboard-y-simulador-streamlit), [DUO-9](https://linear.app/duocuc2026/issue/DUO-9/verificar-api-y-simulador).

## M4 · Documentación y presentación · objetivo técnico 29 de noviembre

- **Plan.** Preparar informe, presentación de 10 minutos, trazabilidad y exposición.
- **Ejecución.** Informe ejecutivo, 10 diapositivas editables, guion de 10:00 y fuentes de resultados. La defensa oral y las preguntas quedan abiertas en DUO-13.
- **Desviación y acción.** La iniciativa «Transformación analítica para la tarificación de seguros» quedó documentada en la descripción del proyecto. El conector no ofrece la operación y el navegador compartido no se inicializó. La relación nativa se puede incorporar al tablero cuando esté disponible. El tablero registra proyecto, hitos e issues.
- **Evidencia.** [Informe](../entregables/MedicalCost_Predictor_Informe_EP6.pdf), [PPTX](../entregables/MedicalCost_Predictor_Defensa_EP6.pptx), [guion](../docs/MedicalCost_Predictor_Defensa.md), [supuestos ROI](medicalcost_roi.csv), [DUO-10](https://linear.app/duocuc2026/issue/DUO-10/redactar-informe-ejecutivo-y-escenarios-roi), [DUO-16](https://linear.app/duocuc2026/issue/DUO-16/preparar-presentacion-y-guion-de-10-minutos), [DUO-17](https://linear.app/duocuc2026/issue/DUO-17/verificar-coherencia-planejecucion-y-publicar-entrega), [DUO-13](https://linear.app/duocuc2026/issue/DUO-13/realizar-exposicion-y-responder-preguntas).

# Bitácora de implementación

Esta bitácora registra actividades reales de la sesión del **11/11/2026 (America/Santiago)**. No acredita trabajo de semanas anteriores ni horas invertidas. El repositorio conserva las fechas reales de publicación de sus commits e Issues.

| Registro | Fecha local | Actividad comprobable | Evidencia | Resultado al registrar |
|---|---|---|---|---|
| B01 | 11/11/2026 | Revisión de pautas EP5/EP6 y antecedentes EP1/EP2/EP4 | [Matriz](../docs/matriz_cumplimiento.md) | Identificados requisitos, alcance, criterios y limitaciones |
| B02 | 11/11/2026 22:00 | Apertura de cinco Issues E1–E5 | [Issues](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues) | Tareas iniciales creadas con estados de ejecución y pendientes externos |
| B03 | 11/11/2026 | Registro de planificado frente a ejecutado | [Plan y ejecución](plan_vs_ejecucion.csv) | Línea base de semanas relativas; fecha real y evidencia pendientes por tarea |
| B04 | 11/11/2026 | Registro de desviaciones y riesgos | [Desviaciones](desviaciones.csv), [riesgos](riesgos.csv) | Cambios justificados y acciones identificadas |
| B05 | 11/11/2026 | Revisión del supuesto financiero del piloto | [Propuesta](../docs/propuesta_piloto.md) | Aclarada reducción condicionada frente a reducción media |
| B06 | 11/11/2026 22:04:33 | Ejecución del pipeline de calidad y modelado | [Métricas](../results/metrics.json), [calidad](../results/data_quality.json) | 1.338 filas, cero nulos, un duplicado agrupado, M1/M2 evaluados |
| B07 | 11/11/2026 | Revisión de desviación del KPI y errores por grupo | [Reporte R1](reportes_estado.md), [validación grupal](../results/holdout_group_validation.csv) | MAE CV +4,47% sobre referencia; uso operativo pendiente de mejora y validación |
| B08 | 11/11/2026 22:06:12 | Prueba de dashboard en Chromium local y móvil emulado | [Validación](../evidence/dashboard_validation.json), [captura escritorio](../evidence/dashboard_desktop.png), [captura móvil](../evidence/dashboard_mobile.png) | 12 combinaciones correctas, cero errores JS, máximo 622,2 ms en cinco cargas, sin desborde móvil |
| B09 | 11/11/2026 22:09:22 | Ejecución final del notebook y actualización de resultados | [Notebook](../notebooks/01_implementacion.ipynb), [métricas finales](../results/metrics.json) | Nueve celdas de código ejecutadas sin errores; resultados numéricos conservados |
| B10 | 11/11/2026 | Pruebas técnicas y demostración CLI | [Pytest](../results/logs/pytest.txt), [CLI](../results/logs/cli_demo.txt) | Seis pruebas aprobadas en 3,90 s y salida agregada reproducible |
| B11 | 11/11/2026 | Publicación técnica en GitHub | [Commit técnico](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/commit/48503c55c7a9edd2d27028d42f90c14ff946970a) | Evidencia técnica publicada; Issues 2 y 4 cerrados técnicamente, 1 y 3 abiertos con pendientes |
| B12 | 11/11/2026 | Revisión documental EP5 y EP6 | [Informe](../entregables/EP5_Informe_Implementacion.pdf), [PPTX](../entregables/EP6_Presentacion.pptx), [validación EP6](../evidence/EP6_validation.json) | Informe de ocho páginas revisado; PPTX de 12 diapositivas y PDF de 12 páginas; guion de 600 s y 19 preguntas |

**B13. 11/11/2026 22:16:54 America/Santiago.** Publicación documental verificada en commit `0dad7369ed68b02f7aa202128a121904f0376b04`: 69 archivos, tres entregables con blobs remotos idénticos a los locales. [Registro](../evidence/publicacion_verificada.json).

**B14. 11/11/2026.** GitHub Actions [43133074760](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/actions/runs/43133074760) concluyó correctamente en Ubuntu: pipeline reproducido y seis pruebas sobre los resultados nuevos aprobadas en 1,56 s. Se adjuntan [log](../evidence/github_actions_resultado.txt) y [snapshot de Issues](../evidence/github_issues.json).

## Criterio de actualización

Cada cierre de tarea requiere una salida verificable y su enlace. Las tareas con firmas, validación de representatividad o exposición oral permanecen abiertas hasta contar con evidencia de la persona responsable. El estado de una Issue representa su alcance explícito; la implementación técnica de E3 no cierra el KPI de desempeño, su aceptación operativa ni la aprobación externa G3.

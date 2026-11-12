# Matriz de cumplimiento EP5 y EP6

Revisión de requisitos: 11 de noviembre de 2026. Esta matriz vincula las pautas con los artefactos de la entrega. El estado de pruebas y publicación se registra en [reportes de estado](../gestion/reportes_estado.md); un enlace por sí solo no acredita una aprobación externa.

## Alcance de la evaluación

El pedido del estudiante es completar EP5 y EP6 y publicar las evidencias en GitHub. Las pautas EP5 y EP6 definen implementación, monitoreo y control. EP1/EP2 y el plan EP4 se usan como antecedentes; no son una orden para fabricar evaluaciones previas, reuniones, firmas, gastos ni actividades históricas.

| ID | Fuente y requisito | Evidencia | Verificación requerida / límite |
|---|---|---|---|
| EP5-T1 | EP5, apartado 1.1. Uso de Python, notebooks y/o scripts | [Pipeline](../src/analysis.py), [notebook](../notebooks/01_implementacion.ipynb) | Ejecutar desde los datos originales y conservar salidas reproducibles |
| EP5-T2 | EP5, 1.1. Al menos un entregable funcional | [Modelo/pipeline](../src/analysis.py), [dashboard](../dashboard/app.py) | Demostración con entrada/salida y controles efectivos |
| EP5-T3 | EP5, 1.1. Avances técnicos y resultados parciales | [Bitácora](../gestion/bitacora.md), `results/` | Solo ejecuciones realmente realizadas, con fecha y enlace |
| EP5-G1 | EP5, 1.2. Herramienta de gestión | [Issues](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues), [tablero](../gestion/tablero.md) | Enlaces activos; tareas identificadas, estado y evidencia |
| EP5-G2 | EP5, 1.2. Planificado frente a ejecutado | [Registro de tareas](../gestion/plan_vs_ejecucion.csv) | Comparar alcance; no afirmar puntualidad sin calendario verificable |
| EP5-G3 | EP5, 1.2. Reportes de estado | [Reportes de estado](../gestion/reportes_estado.md) | Estado, evidencia, problemas, decisión y siguiente acción |
| EP5-G4 | EP5, 1.2. Desviaciones y correctivas | [Desviaciones](../gestion/desviaciones.csv), [riesgos](../gestion/riesgos.csv) | Explicar causa, impacto, decisión, responsable y estado |
| EP5-F1 | EP5, aspectos formales. Informe de 5–8 páginas | [Informe EP5](../entregables/EP5_Informe_Implementacion.pdf) | Ocho páginas; revisión visual de las ocho páginas realizada |
| EP5-F2 | EP5, aspectos formales. Evidencias y enlaces | [README](../README.md), informe y esta matriz | Enlaces a repositorio, tablero y notebook verificables |
| EP5-F3 | EP5, aspectos formales. Claridad y trazabilidad | Esta matriz y seguimiento contra EP4 | Distinguir línea base, cambio y resultado |
| EP6-P1 | EP6, presentación. Evidencia técnica | [PPTX EP6](../entregables/EP6_Presentacion.pptx), pipeline y dashboard | Mostrar archivos y resultados obtenidos |
| EP6-P2 | EP6, presentación. Uso de herramientas de gestión | PPTX, [Issues](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues), [tablero](../gestion/tablero.md) | Abrir tarea y su evidencia, mostrar estados y correctiva |
| EP6-P3 | EP6, presentación. Estado del proyecto | PPTX y [reporte](../gestion/reportes_estado.md) | Producto técnico y validaciones externas separados |
| EP6-P4 | EP6, presentación. Desviaciones respecto al plan | PPTX y [desviaciones](../gestion/desviaciones.csv) | Justificación técnica y de gestión fundamentada |
| EP6-P5 | EP6, presentación. Defensa del cumplimiento | Trazabilidad E1–E5 y [guion](EP6_guion_y_defensa.md) | No afirmar aprobación externa ni exposición ya realizadas |
| EP6-F1 | EP6, modalidad. Presentación ejecutiva de 10 min | [PPTX](../entregables/EP6_Presentacion.pptx), [PDF](../entregables/EP6_Presentacion.pdf), [guion](EP6_guion_y_defensa.md) | 12 diapositivas y 600 s previstos; ensayo y exposición pendientes del estudiante |
| EP6-F2 | EP6, formal. PPT/Canva o similar, claridad visual | [PPTX editable](../entregables/EP6_Presentacion.pptx), [validación](../evidence/EP6_validation.json) | 12 diapositivas revisadas visualmente, tablas/gráfico editables, sin hallazgos geométricos; no abierto en PowerPoint nativo |
| EP6-R1 | Rúbrica EP6. Defensa técnica y de gestión, 40% | PPTX y [guion/decisiones](EP6_guion_y_defensa.md) | El estudiante debe comprender y defender las decisiones |
| EP6-R2 | Rúbrica EP6. Cumplimiento trazable, 30% | Informe, tablero, tareas y desviaciones | Evidencia enlazada y coherente con planificado/ejecutado |
| EP6-R3 | Rúbrica EP6. Preguntas con dominio, 30% | [Guía de preguntas y respuestas](EP6_guion_y_defensa.md) | La ronda real de preguntas depende del estudiante |

La rúbrica EP5 asigna 50% a implementación y 50% a gestión. No se asigna una nota ni un porcentaje de logro a la entrega: la evaluación corresponde al docente.

## Continuidad con el plan EP4

| Línea base | Compromiso | Evidencia / criterio de cierre |
|---|---|---|
| RF1 Must | Identificar factores asociados al costo | [Descriptivos](../results/descriptive_statistics.csv) y [coeficientes ajustados](../results/coefficients.csv) |
| RF2 Must | Cuantificar cambios porcentuales manteniendo otros factores constantes | [Efectos](../results/effects.csv), [coeficientes](../results/coefficients.csv) e interacción explicada |
| RF3 Must | Estimar costo esperado por grupo | [Costos grupales](../results/group_costs.csv) con smearing; [validación de reserva](../results/holdout_group_validation.csv) muestra calibración pendiente para uso operativo |
| RF4 Must | Segmentar prevención por tabaquismo, IMC, edad y región | [Dashboard](../dashboard/app.py), [grupos](../results/dashboard_groups.json), tamaños y límites |
| RF5 Should | Dashboard con filtros/comparaciones | 12 combinaciones verificadas en [evidencia](../evidence/dashboard_validation.json) |
| RF6 Could | Alertar desviación de gasto frente a presupuesto | **Diferido**: no hay ingreso de gasto real ni alertas operativas. La validación de reserva no sustituye este requerimiento |
| RNF1 Must | Privacidad de datos sensibles | Fuente pública, ausencia de identificadores directos y límites de uso |
| RNF2 Should | Semilla 42 y código documentado | [Métricas/versiones](../results/metrics.json), [hash y calidad](../results/data_quality.json), [particiones](../results/split_manifest.csv), [seis pruebas aprobadas](../results/logs/pytest.txt), notebook ejecutado |
| RNF3 Must | Interpretabilidad y asociaciones | Efectos porcentuales comprensibles; no inferencia causal |
| RNF4 Could | Uso móvil | [Móvil emulado](../evidence/dashboard_mobile.png), 390×844 sin desborde en [prueba local](../evidence/dashboard_validation.json); teléfono físico no probado |
| E1 / G1 S2 | Acta y requerimientos aprobados por patrocinador | **Pendiente externo**: no hay firma o aprobación en los insumos |
| E2 / G2 S4 | 1.338 filas, cero nulos del modelo, diccionario y EDA | [Calidad](../results/data_quality.json), [diccionario](diccionario_datos.md); un duplicado conservado, agrupado y documentado |
| E3 / G3 S7 | M1/M2, AIC, CV5, p-valores, residuos y costos grupales | Implementación/evaluación técnica completa; KPI MAE CV no cumple, calibración y aprobación del patrocinador **pendientes** |
| E4 / G4 S9 | Filtros, carga <3 s, computador y móvil | [Prueba](../evidence/dashboard_validation.json): 12 combinaciones, máximo 622,2 ms en cinco cargas locales, móvil emulado sin desborde |
| E5 / G5 S12 | Informe, PPT 10 min y propuesta de piloto aprobados | Artefactos entregables; aprobación y presentación real **pendientes externas** |
| Recursos | 200 h y USD 2.519 estimados | Línea base de planificación. Horas y gastos reales no disponibles |
| Cronograma | 12 semanas relativas | No hay fecha de inicio corroborada; no calcular atraso/puntualidad como hechos |
| Herramientas | Python, Colab, Trello y Canva | GitHub como gestión implica cambio documentado, autorizado por pedido del usuario |

## Lectura de inconsistencias de las pautas

- Los títulos identifican EP5/EP6, pero sus tablas generales todavía mencionan EP3. Se aplican los apartados específicos y las rúbricas de EP5/EP6.
- Los encabezados indican ponderaciones de 10% y 30%, mientras sus tablas internas usan distribuciones distintas. Esa contradicción administrativa no altera los requisitos técnicos; no se inventa una ponderación final.
- EP6 conserva “semana X/XX” en el calendario. No se dispone de vencimiento oficial.
- Las pautas alternan encargo grupal y presentación individual/por equipo. El plan EP4 establece a Vicente Gabriel Zepeda Rojas como único integrante.
- EP1/EP2 fijan 4–6 páginas y 8–10 diapositivas para otra evaluación. EP5/EP6 fijan 5–8 páginas y 10 minutos, sin número de diapositivas. Se priorizan estas últimas.

## Fuentes documentales revisadas

1. EP5_Instrucciones y Pauta ENCARGO_Estudiante.pdf, pp. internas 1–4.
2. EP6_Instrucciones y Pauta PRES_Estudiante.pdf, pp. internas 1–5.
3. Plan_Proyecto_EP4_Factores_Costo_Aseguradora-4 (1).pdf, pp. 1–7.
4. EP1_Instrucciones y Pauta_ENCARGO_Estudiante.pdf, pp. internas 1–5.
5. EP2_Instrucciones y Pauta_PRES_Estudiante.pdf, pp. internas 1–5.

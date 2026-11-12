# Reportes de estado de implementación

Proyecto: factores asociados al costo anual de atención médica. Responsable: Vicente Gabriel Zepeda Rojas. Fuente de planificación: EP4 entregado el 14/10/2026. Repositorio: [Medical-Cost-Personal_Proyect](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect).

Los cortes siguientes pertenecen a la sesión real de implementación del **11 de noviembre de 2026, America/Santiago**. No representan semanas históricas reconstruidas. Las semanas S1–S12 corresponden a la línea base relativa, sin fecha de inicio corroborada.

## R0. Apertura y revisión de insumos

Fecha: 11/11/2026. Apertura de Issues registrada a las 22:00 America/Santiago (12/11/2026 01:00 UTC).

**Estado:** línea base y requisitos revisados; ejecución técnica en curso.

Se revisaron pautas EP5/EP6, pautas antecedentes EP1/EP2 y plan EP4. Se conservaron autor, docente, alcance asociativo, RF1–RF4 Must, CRISP-DM y comparación M1/M2. Se abrieron cinco Issues para E1–E5 y se inició el registro de seguimiento en GitHub. La implementación usa el CSV suministrado; los resultados aún requieren ejecución y verificación.

| Entregable | Criterio del plan | Estado al corte R0 | Próxima acción |
|---|---|---|---|
| E1 | Acta y requerimientos validados | Plan disponible; firma y representatividad pendientes | Mantener [Issue 1](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/1) abierto |
| E2 | 1.338 filas, cero nulos, diccionario y EDA | En ejecución | Ejecutar controles, documentar duplicados y guardar evidencia |
| E3 | M1/M2, AIC, CV5, p-valores, residuos y grupos | En ejecución | Ejecutar pipeline con semilla 42 y control de fuga |
| E4 | Dashboard con filtros, carga <3 s, móvil | En ejecución | Probar funcionalidad, rendimiento y vista móvil |
| E5 | Informe, PPT 10 min y piloto aprobados | En preparación; aceptación externa pendiente | Crear artefactos y mantener pendiente la exposición real |

**Desviaciones y decisiones:** D01 centraliza gestión en GitHub por pedido del estudiante; D04 y D07 preservan las limitaciones de aprobaciones y calendario; D05 marca como ND costos/horas reales; D06 aclara el punto de equilibrio del piloto. [Registro completo](desviaciones.csv).

**Problemas abiertos:** no hay firma de patrocinador, fecha de inicio corroborada ni registros de horas/gastos. No hay evidencia de presentación realizada. Esos faltantes no se sustituyen por documentación creada en esta sesión.

## R1. Verificación técnica

Primera ejecución del pipeline: **11/11/2026 22:04:33 America/Santiago**. La ejecución final del notebook actualizó las salidas el **11/11/2026 a las 22:09:22 America/Santiago**, según [`results/metrics.json`](../results/metrics.json), conservando los mismos resultados numéricos. Este corte acredita la ejecución del análisis y las pruebas complementarias descritas abajo.

**Datos verificados:** 1.338 filas y siete variables originales, cero nulos, una fila duplicada adicional conservada. Las réplicas se mantienen en la misma partición. Hay 1.069 filas de entrenamiento y 269 de reserva; el solapamiento de grupos duplicados entre ambas es cero. [Calidad](../results/data_quality.json) y [particiones](../results/split_manifest.csv).

| Modelo | AIC en entrenamiento, escala log | MAE CV5, USD | RMSE CV5, USD | R² CV5, USD |
|---|---:|---:|---:|---:|
| Media de entrenamiento | No aplica | 9.208,71 | 12.265,60 | -0,0014 |
| M1 aditivo | 1.321,61 | 5.099,15 | 9.252,18 | 0,4302 |
| M2 con interacción | 1.257,88 | 5.039,52 | 9.757,56 | 0,3663 |

Se selecciona M2 por el menor MAE en validación cruzada, con AIC como apoyo. M1 tiene mejor RMSE y R² en USD; la elección no implica superioridad en todas las métricas. El modelo de reserva se evalúa después de esa decisión: MAE USD 4.505,95, RMSE USD 8.414,67 y R² en USD 0,4616. El MAE mejora un 49,4% frente a la media de entrenamiento en la misma reserva. [Comparación](../results/model_comparison.csv).

**Desviación de desempeño:** la referencia EP4 de MAE CV ≤USD 4.824 **no se cumple**: USD 5.039,52 es USD 215,52 mayor, un 4,47%. El resultado de reserva más favorable no sustituye ese KPI de validación cruzada. La línea base no aporta código ni particiones originales para reconciliar exactamente su cifra.

**Límites detectados:** Breusch–Pagan `p=1,08e-10` y Jarque–Bera con p numéricamente cero evidencian heterocedasticidad y falta de normalidad residual. Se usa inferencia HC3 y smearing por tabaquismo calculado dentro de cada entrenamiento. Esas medidas no eliminan todos los problemas de especificación. En reserva, el costo esperado agregado supera al observado en 15,21% para fumadores y 3,64% para no fumadores; el prototipo requiere recalibración y validación externa antes de presupuestar una cartera real. [Diagnósticos](../results/residual_diagnostics.json) y [validación grupal](../results/holdout_group_validation.csv).

**Decisión de control:** conservar el alcance de análisis de factores y presupuesto exploratorio por grupo; no habilitar decisiones operativas o individuales. La aprobación de interpretación por patrocinador sigue pendiente.

**Dashboard verificado el 11/11/2026 a las 22:06:12 America/Santiago** (12/11/2026 01:06:12 UTC). Se comprobaron 12 combinaciones de tabaquismo y dimensión de comparación: conteos y medias ponderadas correctos en todos los casos, sin errores JavaScript. En Chromium local, cinco cargas tuvieron máximo **622,2 ms**, inferior al criterio de tres segundos. La vista móvil emulada de 390×844 px no tuvo desborde horizontal. Estas pruebas acreditan ese entorno local; no equivalen a un teléfono físico ni a rendimiento en producción. [Registro](../evidence/dashboard_validation.json), [escritorio](../evidence/dashboard_desktop.png) y [móvil](../evidence/dashboard_mobile.png).

**Pruebas técnicas finales:** seis pruebas aprobadas en 3,90 s, con verificación de fuga de duplicados, rechazo de entradas inválidas, conciliación de grupos, MAE OOF independiente, tamaños mínimos de grupo y reproducción de la reserva por el modelo serializado. [Salida pytest](../results/logs/pytest.txt). El [notebook](../notebooks/01_implementacion.ipynb) conserva nueve celdas de código ejecutadas, sin errores; la [demo CLI](../results/logs/cli_demo.txt) publica una salida agregada real.

**Pendiente al cerrar R1:** revisión final de informe/presentación y publicación verificable. El cierre técnico no modifica las aprobaciones externas ni el incumplimiento del KPI de referencia.

## R2. Preparación de entrega

Fecha: **11/11/2026, America/Santiago**. **Cierre documental y publicación verificados a las 22:16:54.**

El [informe EP5](../entregables/EP5_Informe_Implementacion.pdf) tiene **ocho páginas**, dentro del requisito de cinco a ocho, y sus ocho páginas se revisaron visualmente. Se comprobó la cobertura de implementación, monitoreo, tareas frente al plan, reportes, desviaciones, correctivas y enlaces. El contenido distingue medias geométricas, medias aritméticas y asociaciones observacionales.

La [presentación EP6 editable](../entregables/EP6_Presentacion.pptx) tiene **12 diapositivas** y la [versión PDF](../entregables/EP6_Presentacion.pdf), 12 páginas. El [guion y defensa](../docs/EP6_guion_y_defensa.md) distribuye **600 segundos** y prepara 19 preguntas. La revisión visual y de integridad se documenta en [`evidence/EP6_validation.json`](../evidence/EP6_validation.json); no se abrió PowerPoint nativo. Se conservaron tablas y gráfico editables en PPTX.

**Publicación técnica acreditada:** [commit 48503c55c7a9edd2d27028d42f90c14ff946970a](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/commit/48503c55c7a9edd2d27028d42f90c14ff946970a), seguido por [2ac7e4b827dc9ed79adb589cb35d8259ad8ac431](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/commit/2ac7e4b827dc9ed79adb589cb35d8259ad8ac431). El [run de GitHub Actions 43133074760](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/actions/runs/43133074760) terminó correctamente: instalación limpia en Ubuntu, pipeline reproducido, seis pruebas aprobadas en 1,56 s sobre salidas recién generadas y exportación del dashboard. [Registro](../evidence/github_actions.json) y [extracto de log](../evidence/github_actions_resultado.txt). La documentación final se publicó en [commit 0dad7369ed68b02f7aa202128a121904f0376b04](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/commit/0dad7369ed68b02f7aa202128a121904f0376b04). Se consultó el árbol remoto y se comprobaron 69 archivos y la igualdad de los blobs locales y remotos del informe, PPTX y PDF de la presentación. [Verificación de publicación](../evidence/publicacion_verificada.json).

**Estado de tareas:** Issues [#2](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/2) y [#4](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/4) cerrados por criterios técnicos verificados. [#3](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/3) permanece abierto por KPI MAE, calibración y aceptación. [#1](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/1) mantiene firma/representatividad pendientes. [#5](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/5) conserva únicamente actuación oral y aprobación pendientes; los documentos y evidencias están publicados.

**Restricciones remanentes:** RF6 Could está diferido, sin ingreso de gasto real ni alertas operativas. No se pueden verificar plazo, horas o costos reales. El estudiante debe ensayar y realizar la exposición y responder las preguntas; los archivos no acreditan esa actuación ni la aprobación del patrocinador. G1, la aceptación externa de G3 y G5 permanecen abiertos.

## Indicadores de control disponibles

| Indicador | Línea base EP4 | Valor real disponible | Lectura al corte R0 |
|---|---:|---|---|
| Horas del análisis | 200 h | ND | No hay partes de horas reales |
| Personal estimado | USD 2.290 | ND | Estimación de planificación, sin ejecución financiera acreditada |
| Contingencia estimada | USD 229 | ND | 10% del personal estimado |
| Presupuesto total estimado | USD 2.519 | ND | No es gasto real |
| Desviación de costo | Meta ±10% | ND | Requiere costo real comparable |
| Desviación de horas | Meta ≤5% | ND | Requiere horas reales por rol |
| Hitos oportunos | Meta 100% | ND | Falta calendario de inicio y fechas de aceptación |
| SPI / CPI | No definidos en EP4 | ND | Faltan valor planificado, ganado y costo real |
| MAE CV5 del modelo | Referencia USD 4.824 | USD 5.039,52 | No cumple; +USD 215,52 y +4,47% |
| Participación del top 10% | Referencia 31,8% | 31,98% | Se toman 134 de 1.338 filas; diferencia +0,18 puntos porcentuales |
| Resultado del piloto | Reducción propuesta ≥4,9% | No medido | Piloto fuera de la implementación actual |

ND significa **no disponible**. No se interpreta como cero, cumplimiento o incumplimiento. El avance se informa por criterios verificables de entregables, sin simular métricas de valor ganado. Los valores técnicos de esta tabla se actualizan al corte R1; las métricas financieras siguen sin datos reales.

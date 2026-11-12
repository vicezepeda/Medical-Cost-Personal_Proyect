# Tablero de seguimiento

Herramienta de gestión: GitHub Issues, con un registro versionado de plan, ejecución, desviaciones y reportes. Las columnas de este documento son vistas de trabajo sobre las mismas cinco tareas; no simulan un tablero histórico de Trello ni un GitHub Project que no se haya creado.

[Abrir Issues del proyecto](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues)

## Verificado técnicamente

| Issue | Entregable | Criterio de salida | Evidencia esperada |
|---|---|---|---|
| [#2](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/2) | E2. Base validada y EDA | 1.338 filas, cero nulos y un duplicado conservado y agrupado | `results/data_quality.json`, `results/descriptive_statistics.csv`, `docs/diccionario_datos.md`, notebook ejecutado |
| [#3](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/3) | E3. Modelos evaluados | M1/M2, AIC, CV5, inferencia, residuos y grupos ejecutados | `src/analysis.py`, `results/`; MAE CV +4,47% sobre referencia y calibración operativa pendientes |
| [#4](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/4) | E4. Dashboard | 12 combinaciones correctas, máximo 622,2 ms, móvil emulado sin desborde | `dashboard/app.py`, `evidence/dashboard_validation.json`, capturas |

## Documentación verificada y publicación final

| Issue | Entregable | Criterio de salida | Evidencia esperada |
|---|---|---|---|
| [#5](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/5) | E5. Informe, presentación y piloto | Informe de 8 páginas revisado, PPTX de 12 diapositivas, PDF de 12 páginas, guion de 600 s y propuesta | `entregables/`, `docs/EP6_guion_y_defensa.md`, `docs/propuesta_piloto.md`; documentos publicados, defensa y aprobación pendientes |

## Pendiente de validación externa

| Issue / compuerta | Faltante | Responsable de aceptación |
|---|---|---|
| [#1](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/1), G1 | Acta firmada, objetivos aprobados y representatividad | Patrocinador |
| [#3](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/3), G3 | Validación de interpretación en una cartera real | Patrocinador |
| [#5](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues/5), G5 | Aprobación, exposición y ronda de preguntas | Patrocinador y estudiante |

## Reglas de seguimiento

- Cada Issue enlaza el artefacto que permite revisar su resultado.
- `gestion/plan_vs_ejecucion.csv` compara el alcance previsto con lo ejecutado y probado.
- `gestion/desviaciones.csv` registra causa, impacto, correctiva y estado.
- `gestion/reportes_estado.md` conserva cortes reales de esta sesión.
- Se marca completo técnico solo después de una prueba real. Las aprobaciones externas se mantienen abiertas.
- Las semanas S1–S12 son la línea base relativa. No se infiere atraso, puntualidad ni horas reales.

Última revisión: **R2 del 11/11/2026**. Issues #2 y #4 cerrados por criterios técnicos; #3 abierto por KPI, calibración y aceptación; #1 abierto por firma/representatividad; #5 abierto por exposición y aprobación. Documentos y evidencias publicados, con reproducción aprobada en Actions. RF6 Could permanece diferido.

Publicación documental verificada el 11/11/2026 a las 22:16:54 America/Santiago, commit `0dad7369ed68b02f7aa202128a121904f0376b04`. Los tres entregables coinciden con los blobs remotos. CI aprobado: pipeline y seis pruebas en Ubuntu. [Publicación](../evidence/publicacion_verificada.json), [CI](../evidence/github_actions.json) y [estado de Issues](../evidence/github_issues.json). E5 conserva pendiente la defensa y aprobación; E3 conserva desempeño, calibración y aceptación.

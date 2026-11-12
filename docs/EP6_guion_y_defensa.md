# EP6: guion de exposición y preparación de la defensa

**Autor:** Vicente Gabriel Zepeda Rojas. **Asignatura:** SCY1102 Gestión de Proyectos de Datos. **Docente:** Jorge Alberto Moscoso Santander. **Corte documental:** 11/11/2026, America/Santiago.

La presentación tiene 12 diapositivas y un tiempo objetivo de **10 minutos**. Las notas del PPT amplían cada argumento y citan la evidencia. Este guion prepara la exposición; no acredita que la presentación, las preguntas o la aprobación del patrocinador ya ocurrieron.

## Distribución del tiempo

| Lámina | Tiempo | Acumulado | Argumento y evidencia a mostrar |
|---|---:|---:|---|
| 1. Portada | 25 s | 0:25 | Identificar proyecto, autor y corte de la implementación. |
| 2. Objetivo y alcance | 45 s | 1:10 | Presupuesto por grupos y orientación de prevención. Distinguir asociaciones observacionales de causalidad. |
| 3. Calidad de la base | 40 s | 1:50 | 1.338 filas, cero nulos y un duplicado exacto conservado. Mostrar el control de calidad. |
| 4. Validación | 55 s | 2:45 | Semilla 42, cinco particiones dentro de entrenamiento y prueba final separada. Agrupar réplicas para impedir fuga. |
| 5. Comparación M1/M2 | 75 s | 4:00 | Explicar qué cambia con la interacción, cómo se selecciona y en qué escala se expresa cada métrica. |
| 6. Costos por grupos | 55 s | 4:55 | Comparar costo medio por tabaquismo e IMC. Aclarar que las medias son descriptivas y no ahorros potenciales garantizados. |
| 7. Interpretación y supuestos | 50 s | 5:45 | Efectos ajustados, p-valores robustos y diagnóstico de residuos. Explicar los límites que afectan la conclusión. |
| 8. Demostración técnica | 60 s | 6:45 | Cambiar filtros del dashboard y mostrar una salida real del notebook o CLI agregado. |
| 9. Demostración de gestión | 50 s | 7:35 | Abrir una tarea del tablero y su evidencia. Relacionar criterio del plan con estado verificado. |
| 10. Desviaciones | 65 s | 8:40 | Justificar cambios de herramientas, tratamiento del duplicado y referencias preliminares. Explicar las acciones correctivas. |
| 11. Cumplimiento del plan | 55 s | 9:35 | Separar entregables técnicos de las compuertas que requieren patrocinador o exposición real. |
| 12. Cierre | 25 s | 10:00 | Resumir la contribución y la siguiente decisión necesaria: validación de representatividad e interpretación. |

## Preparación de la demostración

1. Seguir el procedimiento de instalación del [README](../README.md). Abrir el dashboard local en `http://127.0.0.1:8501/` y comprobar que carga antes de presentar. Mantener abierta la versión estática `dashboard/index.html` como respaldo.
2. Abrir en otra pestaña el [notebook ejecutado](../notebooks/01_implementacion.ipynb), la [comparación de modelos](../results/model_comparison.csv) y el [tablero de gestión](../gestion/tablero.md).
3. Preparar la terminal en la raíz del repositorio. El comando `python -m src.cli --group smoker,bmi_group` entrega un reporte agregado. No ingresar características de una persona para intentar predecir su costo.
4. Abrir una [tarea de GitHub](https://github.com/vicezepeda/Medical-Cost-Personal_Proyect/issues) y el [plan frente a ejecución](../gestion/plan_vs_ejecucion.csv). Mostrar requisito, responsable, estado, criterio de aceptación y evidencia vinculada.
5. Durante la demo técnica: filtrar fumadores, comparar IMC y observar el tamaño de los grupos. Volver a todos y cambiar región. Explicar que los filtros actualizan descripciones de la muestra, sin convertirlas en efectos causales.
6. Si la conexión falla, usar los archivos locales, la versión estática y las capturas en `evidence/`. Explicar qué evidencia se está mostrando. No fingir una ejecución en vivo si se usa una captura.

## Preguntas para la defensa

**¿Qué problema resuelve el entregable?**

Permite examinar factores asociados al costo facturado y estimar valores de referencia por grupo. Entrega una base documentada, código reproducible, modelos comparados, costos agrupados y un dashboard. La utilidad propuesta es presupuestaria y exploratoria. Una aplicación en una aseguradora exige validar primero la cartera y sus objetivos.

**¿Por qué se modela el logaritmo del costo?**

La distribución de `charges` es asimétrica. En esta muestra la media es US$13.270 y la mediana US$9.382. El logaritmo facilita expresar asociaciones relativas y reduce la influencia de la escala de costos altos. No garantiza por sí mismo normalidad de residuos ni varianza constante; por eso el código revisa los supuestos.

**¿Cómo se interpreta M2?**

M2 permite que la asociación entre IMC y log(costo) difiera según tabaquismo. El IMC se centra en 30. Por eso el coeficiente principal de tabaquismo se interpreta en IMC=30 y el coeficiente de interacción modifica la pendiente del IMC en fumadores. Un cambio porcentual para un coeficiente simple se obtiene con `100 × (exp(beta) − 1)`. Con interacción, se debe usar la combinación de coeficientes que corresponde al perfil o contraste.

**¿Una asociación significativa prueba que dejar de fumar reduce el costo?**

No. La base es observacional y carece de diagnósticos, tratamientos, tipo de cobertura y seguimiento temporal. Un p-valor no elimina confusión ni sesgo de selección. La reducción del costo por intervención debe evaluarse en un piloto con diseño y grupo de comparación apropiados.

**¿Qué significan AIC, CV y prueba final?**

El AIC compara ajuste y complejidad sobre la misma muestra y la misma variable respuesta. La validación cruzada evalúa cada modelo en particiones que no usa para ajustarlo. La prueba final se reserva de la selección para obtener una evaluación adicional. Un AIC más bajo no equivale a un porcentaje de precisión, y R² debe leerse en la escala indicada.

**¿Por qué las cifras difieren de la presentación EP4?**

EP4 contiene referencias preliminares sin código ni particiones entregadas que permitan reproducirlas exactamente. La implementación registra fórmula, semilla, agrupación, separación y retransformación. Las diferencias deben atribuirse a procedimientos verificables, sin afirmar que las cifras preliminares eran resultados de esta ejecución. Revisar `gestion/desviaciones.csv`, D03 y D08.

**¿Se cumple el KPI MAE de validación cruzada de US$4.824?**

No. M2 obtiene MAE CV de US$5.039,52, que supera la referencia en US$215,52, un 4,47%. El MAE de la prueba final es US$4.505,95, pero esa métrica no reemplaza el criterio de CV comprometido. Se comunica el incumplimiento y se deja pendiente la mejora y aceptación de negocio.

**¿Por qué elegir M2 si su RMSE es peor?**

La regla primaria declarada es menor MAE en USD sobre predicciones fuera de partición. M2 reduce MAE 1,17% frente a M1 y reduce AIC en 63,73 puntos. Sin embargo, su RMSE CV sube de US$9.252,18 a US$9.757,56 y su R² USD baja. Eso muestra un intercambio: M2 mejora el error absoluto típico, pero penaliza más algunos errores grandes. La selección no demuestra superioridad bajo todas las pérdidas ni resuelve la aceptación presupuestaria.

**¿Puede usarse ya como presupuesto operativo de una aseguradora?**

No con esta evidencia. En la prueba final el presupuesto agregado del grupo fumador sobreestima 15,21%, por encima de la tolerancia de ±10% del plan. En no fumadores el error es +3,64%. Además, la representatividad y la aceptación del cliente siguen pendientes. Corresponde recalibrar, revisar la especificación y validar con datos de cartera antes de un uso real. HC3 corrige la estimación de incertidumbre bajo ciertas condiciones; no elimina ese error de presupuesto.

**¿Por qué se conserva el duplicado?**

E2 exige conservar las 1.338 filas de referencia. La copia exacta se identifica en el control de calidad. Su grupo se mantiene en una única partición para que no exista una copia en entrenamiento y otra en validación o prueba. La decisión conserva trazabilidad y controla el riesgo de fuga. No se puede asegurar que la réplica represente o no una persona distinta sin información de origen.

**¿Cómo se pasa de log(costo) a costo medio?**

Exponenciar la predicción del logaritmo no estima directamente la media aritmética del costo. El código aplica una corrección de retransformación por residuos, denominada smearing, estimada solo con los datos usados para ajustar cada modelo. Se calcula por tabaquismo para admitir diferencias entre esos grupos. La corrección mejora la coherencia del cálculo, pero no elimina todos los errores del modelo.

**¿Cómo se abordan los residuos y los p-valores?**

La implementación revisa heterocedasticidad, forma de la distribución residual e influencia. Reporta errores estándar robustos HC3. Estos protegen parcialmente la inferencia frente a heterocedasticidad, sin corregir una especificación equivocada, dependencia entre observaciones o variables omitidas. Las limitaciones se mantienen visibles al interpretar resultados.

**¿Por qué se muestra el número de registros de cada grupo?**

Una media de un grupo pequeño puede ser inestable. Mostrar `n`, costo medio y dispersión ayuda a interpretar cuánto respaldo descriptivo tiene el segmento. Si se crean muchas combinaciones de filtros, los grupos pueden quedar pequeños y no deben presentarse como presupuestos fiables sin revisión.

**¿Por qué GitHub reemplaza herramientas del plan?**

El usuario solicita publicar toda la evidencia en GitHub. Issues y archivos versionados concentran tareas, estados y vínculos al código. El cambio se registra como desviación de herramienta, con justificación y trazabilidad. El uso actual de GitHub no acredita un uso histórico de Trello ni reuniones anteriores.

**¿Se cumplió el plazo de doce semanas?**

No se puede verificar porque no se aportó fecha de inicio corroborada ni una bitácora de ejecución semanal. El seguimiento conserva las semanas relativas de la línea base y la fecha real de las evidencias creadas en este corte. La semana real permanece ND cuando no hay respaldo.

**¿Se cumplió el presupuesto?**

El plan estima 200 horas y US$2.519 para el análisis. No existen partes de horas ni gastos reales aportados. Por ello no se afirma ahorro, sobrecosto o cumplimiento financiero, ni se calculan indicadores que requieran esos datos. El registro inicia la trazabilidad actual sin reconstruir consumos históricos.

**¿Qué falta para cerrar las compuertas?**

E1 requiere acta firmada y validación de objetivos. G3 requiere interpretación validada por el patrocinador. E5 requiere aprobación y exposición efectiva. La existencia del notebook, PPT o informe acredita trabajo técnico y documental, pero no sustituye esas actuaciones externas. Consultar la matriz de cumplimiento y las tareas pendientes.

**¿Se ejecutó el piloto preventivo?**

Se presenta una propuesta. No hay intervención ni ahorro observado. El presupuesto propuesto es US$97.100 para 250 participantes, US$388,4 por persona. La meta de cesación de 25% es un supuesto. La propuesta distingue la reducción entre quienes dejan de fumar de la reducción promedio sobre todos los participantes; los umbrales y condiciones se explican en `docs/propuesta_piloto.md`.

**¿La publicación del CSV acredita cumplimiento legal?**

Se trabaja con la fuente pública de referencia, sin identificadores directos incorporados. Esto no acredita una auditoría legal ni autoriza publicar una cartera real de salud. Antes de usar datos del cliente corresponde definir autorización, acceso y tratamiento apropiados. El alcance académico y las limitaciones de representatividad quedan declarados.

## Evidencia para responder

| Pregunta | Evidencia principal |
|---|---|
| Calidad y duplicados | `results/data_quality.json`, `src/analysis.py`, diccionario de datos |
| Modelos, validación y coeficientes | `results/model_comparison.csv`, `results/metrics.json`, `results/effects.csv` |
| Supuestos | `results/residual_diagnostics.json`, gráficos de diagnóstico |
| Costos por grupos | `results/group_costs.csv`, `src/cli.py`, dashboard |
| Estado y acciones correctivas | `gestion/plan_vs_ejecucion.csv`, `gestion/reportes_estado.md`, `gestion/desviaciones.csv` |
| Cumplimiento | `docs/matriz_cumplimiento.md`, Issues E1–E5 |
| Piloto y presupuesto | `docs/propuesta_piloto.md`, plan EP4 de referencia |

## Ensayo final del estudiante

Realizar un ensayo cronometrado con el dashboard y las pestañas preparadas. Ajustar la explicación a diez minutos sin omitir limitaciones o sustituir la defensa por lectura de las diapositivas. Practicar explicar una fórmula, una desviación y una tarea pendiente con su evidencia. Confirmar con el docente el calendario, la modalidad y las ponderaciones contradictorias de la plantilla si inciden en la entrega.

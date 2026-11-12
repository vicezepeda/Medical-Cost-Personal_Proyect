# Propuesta de piloto preventivo

**Estado: propuesta académica, sin implementación ni resultados medidos.** Responsable del proyecto: Vicente Gabriel Zepeda Rojas. La propuesta da continuidad a E5 del plan EP4. La aseguradora, su patrocinador y el equipo clínico deberán validar presupuesto, factibilidad y condiciones de participación antes de ejecutar.

## Objetivo y población

Evaluar si un programa voluntario de cesación tabáquica puede mejorar los resultados de salud y reducir el costo anual medio del grupo participante. El plan considera 250 participantes y seis meses de coordinación clínica. Los datos públicos describen asociaciones entre tabaquismo y costos; no estiman el efecto causal de dejar de fumar ni garantizan ahorros.

La selección deberá evitar exclusiones discriminatorias. El programa no se usará para negar atención, cobertura o fijar primas individuales. La participación, consentimiento y seguimiento clínico requieren validación de las instancias responsables.

## Presupuesto de referencia del EP4

| Concepto | Cálculo del plan | USD |
|---|---|---:|
| Coordinación clínica | 6 meses × 1.500 | 9.000 |
| Participación | 250 × 317 | 79.250 |
| Base | 9.000 + 79.250 | 88.250 |
| Contingencia del plan | Ajuste informado por EP4 | 8.850 |
| Total | 88.250 + 8.850 | 97.100 |
| Costo por participante | 97.100 / 250 | 388,40 |

La contingencia de USD 8.850 equivale al 10,0283% de la base; el 10% exacto sería USD 8.825 y el total USD 97.075. Se conserva el presupuesto declarado como supuesto de la línea base, sin presentarlo como gasto ejecutado. La aprobación del patrocinador está pendiente.

El presupuesto del piloto es independiente del análisis de datos (200 h y USD 2.519 estimados en EP4). Ninguno de esos montos representa gasto real acreditado.

## Aclaración del punto de equilibrio

Supuestos de referencia del plan: costo anual inicial por fumador `C = USD 32.050`, proporción que deja de fumar `q = 25%` y costo del programa por participante `p = USD 388,40`.

Si solamente quienes dejan de fumar redujeran su costo en una fracción `r`, el ahorro medio por participante sería `q × C × r`. El punto de equilibrio exige:

`r = p / (q × C) = 388,40 / (0,25 × 32.050) = 4,8474%`.

Ese porcentaje representa la reducción necesaria **entre quienes dejan de fumar** bajo los supuestos del ejercicio. El umbral de reducción media para el conjunto de participantes es:

`p / C = 388,40 / 32.050 = 1,2119%`.

El EP4 aproxima el costo a USD 390 y obtiene 4,9%. Con USD 390, los valores son 4,87% condicionado y 1,22% medio. Se aclara esa diferencia para evitar llamar 4,9% a una reducción media de todos los participantes.

| Cesación supuesta `q` | Reducción condicionada necesaria `r` | Reducción media necesaria |
|---:|---:|---:|
| 10% | 12,12% | 1,21% |
| 25% | 4,85% | 1,21% |
| 40% | 3,03% | 1,21% |

Esta aritmética evalúa escenarios presupuestarios. No incorpora cambios de composición, costos clínicos posteriores, tiempo hasta el efecto, adherencia o inflación. Las cifras del modelo observacional no deben sustituir una evaluación del programa.

## Diseño de evaluación propuesto

Antes de iniciar se definirán criterios de participación, medición de cesación, costo observado y horizonte de seguimiento. Un grupo de comparación adecuado y un protocolo previamente establecido permitirán distinguir mejor el cambio del programa de otras diferencias entre participantes. La factibilidad de asignación y el análisis clínico requieren decisión de las instancias responsables.

Se recomienda medir costo total y medio por participante durante un periodo comparable, retención, cesación y eventos relevantes. Se reportarán tamaños de grupo, intervalos de incertidumbre y diferencias iniciales. Los indicadores de salud no se reducirán al ahorro monetario.

| Indicador propuesto | Definición | Evidencia necesaria |
|---|---|---|
| Participación y retención | Personas que ingresan y completan seguimiento | Registro de participación autorizado |
| Cesación | Proporción que cumple criterio clínico previamente definido | Medición validada por equipo clínico |
| Costo del programa | Gasto real / participantes elegibles definidos | Comprobantes y regla de denominador |
| Cambio del costo anual | Diferencia en costos comparables entre periodos y grupos | Datos reales, comparador y ajuste documentado |
| Punto de equilibrio | Ahorro atribuible frente a gasto real | Evaluación del efecto con incertidumbre |

## Decisión de continuidad

No se amplía el programa solo por una asociación del dataset. Se necesita aprobación, un protocolo clínico y ético, presupuesto actualizado y resultados reales que permitan valorar beneficios y costos. La meta del plan funciona como hipótesis de planificación; su cumplimiento no puede marcarse con los datos públicos actuales.

Fuente: *Plan de Proyecto de Ciencia de Datos, Evaluación Parcial N°4*, Vicente Gabriel Zepeda Rojas, 14/10/2026, secciones 2.3, 4.3, 4.4 y 4.5. Cálculos de sensibilidad elaborados para esta entrega.

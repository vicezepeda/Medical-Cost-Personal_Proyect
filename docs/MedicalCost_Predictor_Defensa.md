# Defensa de MedicalCost Predictor · EP6
Equipo MedicalCost Predictor · SCY1102

[Presentación editable](../entregables/MedicalCost_Predictor_Defensa_EP6.pptx) · [Guía de ejecución](MedicalCost_Predictor_Ejecucion.md) · [Proyecto en Linear](https://linear.app/duocuc2026/project/medicalcost-predictor-ep6-b503ee94e0e0)

Abre el dashboard y Swagger antes de presentar. Deja el simulador con el perfil inicial y el tablero en la lista de hitos. Si falla la conexión, usa la captura de la diapositiva 8 y el JSON de evidencia. Los bloques suman 10:00 e incluyen pausas y las acciones en pantalla. La exposición efectiva se registra en DUO-13.

## 1 · 0:00–0:45 · MedicalCost Predictor

Si una organización usa el cargo promedio como referencia, ¿cuánta precisión gana al incorporar edad, IMC y otros atributos del perfil? MedicalCost Predictor es un prototipo que estima ese cargo y permite consultarlo desde un simulador o por HTTP. En esta presentación mostraré cómo seguimos CRISP-DM, cuánto bajó el error frente a la media y en qué grupos sigue siendo mayor. Cerraré con la evidencia de los hitos y dos escenarios económicos para evaluar un posible piloto.

## 2 · 0:45–1:45 · Cuánto perdemos con una prima uniforme

Supongamos una cartera de mil pólizas. En un segmento de 250, el costo esperado supera en 400 dólares la prima uniforme. La brecha bruta anual del segmento sería de cien mil dólares. El margen neto dependería también de los otros segmentos, los gastos y las renovaciones. Una prima promedio puede cubrir la cartera en agregado y, aun así, dejar mal representados algunos grupos. En el conjunto público, usar una media única tiene un MAE cercano a nueve mil dólares en prueba. Esa cifra mide incertidumbre predictiva y la brecha de cien mil pertenece al escenario hipotético. Para pasar del error al dinero hay que observar primas y costos de una cartera real.

## 3 · 1:45–2:45 · Objetivo y metodología CRISP-DM

El objetivo de esta extensión EP6 es estimar un cargo en dólares a partir de seis atributos y demostrar el resultado en local. Seguimos CRISP-DM, la metodología adoptada en el plan EP4. Primero definimos el problema de negocio. Después perfilamos el dataset y preparamos las variables y las particiones. En modelado entrenamos los candidatos y en evaluación comparamos sus errores en dólares. El despliegue de la demo consiste en la API y el dashboard. EP4 descartó la cascada porque los resultados de una fase pueden exigir volver a una anterior. Eso ocurrió al revisar el error del modelo logarítmico y volver a modelar.

## 4 · 2:45–3:35 · Quién gana y qué debe validar

Suscripción es el beneficiario directo porque puede estudiar la diferencia entre perfiles. A los asegurados les interesa que la estimación sea comprensible y previsible. Finanzas puede respaldar el piloto si confirma el margen retenido y el tiempo liberado. TI y Datos necesitan que dos canales compartan el mismo contrato y la misma versión del modelo. Cumplimiento debe revisar el uso de variables como sexo, región y tabaquismo y exigir control humano. En un piloto, cada área debe acordar un criterio verificable. Una reducción global del error por sí sola no resuelve las diferencias entre grupos.

## 5 · 3:35–4:35 · Datos y preparación

Usamos 1.338 filas del dataset público Medical Cost Personal. La base tiene cero nulos y un duplicado exacto. Conservamos ambas copias y las agrupamos para que no crucen particiones. Quedaron 1.069 filas para entrenar y 269 para probar. Dentro de entrenamiento hicimos validación cruzada de cinco pliegues agrupados y estratificados por tabaquismo, con semilla 42. Las numéricas se escalan y las categóricas se codifican con one-hot. Cada preprocesador se ajusta con los datos de su pliegue. El horizonte de los cargos no está confirmado, por eso la anualización del negocio aparece solo como supuesto.

## 6 · 4:35–5:55 · Modelo y resultados

La media es la línea base. El estudio previo comparó dos regresiones sobre log-cargos. La que incluía la interacción entre IMC y tabaquismo obtuvo un MAE de validación cruzada de 5.040 dólares, sobre la referencia de 4.824. Volvimos al modelado y probamos una regresión directa en dólares con las mismas particiones. La elegimos por su menor MAE de validación cruzada, de 4.233. En el conjunto de prueba obtuvo un MAE de 4.120, un RMSE de 5.884 y un R² de 0,737. El MAE bajó 53,7 % frente a la media. [Señala el recuadro por tabaquismo.] El MAE fue de 8.610 entre fumadores y de 2.913 entre no fumadores. Esta diferencia requiere validación con una cartera real antes de aplicar el resultado a decisiones individuales.

## 7 · 5:55–6:45 · Arquitectura

El entrenamiento lee el CSV y guarda un solo objeto con el preprocesador y la regresión. Pydantic valida las categorías y los rangos. FastAPI carga el objeto una vez al arrancar y lo reutiliza para cada consulta. El dashboard puede servir una predicción local o llamar al endpoint. Ambos mecanismos usan las mismas reglas para formar las entradas y redondear la salida. El JSON de resultados conserva la evidencia de validación y alimenta las tarjetas y el control de la meta.

## 8 · 6:45–8:05 · Demostración

Comienzo con 30 años e IMC 25, cero hijos, no fumador y región noreste. En modo local el cargo estimado es de 4.335,51 dólares. [Cambia el IMC de 25 a 30 y muestra el recálculo. Devuelve el IMC a 25.] Selecciono API REST y pulso Consultar API. El valor coincide con el local. [Abre Swagger o muestra el JSON de la diapositiva.] El endpoint de salud devuelve ok. Si ingreso edad 17, la API responde 422. [Muestra la pestaña Análisis si queda tiempo.] Aquí se puede revisar la distribución por tabaquismo y el efecto sobre el error al permutar cada variable. La pestaña de plan registra la brecha respecto al MAE objetivo.

## 9 · 8:05–9:05 · Hitos y criterios de cierre

Linear registra cuatro hitos y trece tareas. Para cerrar datos, verificamos el perfilado y la partición agrupada. Para el modelo, comparamos candidatos, comprobamos la meta de error y reportamos diferencias por grupo. Para la demo, verificamos el contrato de la API y la paridad con el simulador. [Muestra la tabla.] El hito de entrega tiene tres tareas cerradas y la defensa oral sigue abierta en DUO-13. Las compuertas originales de EP4 también pedían aprobación del patrocinador en G1, G3 y G5. Esas aprobaciones siguen pendientes.

## 10 · 9:05–10:00 · ROI y decisión

Con un costo de 15.000 dólares en el primer año, el escenario conservador estima 16.000 de beneficio bruto y un ROI de 6,7 %. El optimista estima 38.000 y un ROI de 153,3 %. Ambos suman una recuperación parcial de la brecha, el margen de renovaciones adicionales y el tiempo operativo liberado. Son proyecciones sujetas a esos supuestos. La propuesta es un piloto en paralelo con una cartera representativa. Ahí se medirían la calibración por grupo, el ahorro y la retención antes de decidir un uso en primas. [Cierra en 10:00.]

## Preguntas de defensa

| Pregunta | Respuesta |
|---|---|
| ¿Por qué regresión lineal directa? | Obtuvo el menor MAE CV en USD con el mismo protocolo. El pipeline ofrece inferencia rápida, inspección y una línea base ampliable. |
| ¿Qué evita la fuga de datos? | Las copias exactas se agrupan. Los transformadores se ajustan solo con cada entrenamiento. El holdout no interviene en esa selección. |
| ¿Por qué RMSE y MAE son distintos? | MAE promedia magnitudes. RMSE eleva al cuadrado antes de promediar y acentúa errores grandes. Ambos se calculan en USD. |
| ¿Qué significa R² = 0,737? | La suma de errores cuadrados es menor que la de una estimación constante centrada en la media de la prueba. R² mide ajuste global bajo esta muestra. |
| ¿Un error mayor en fumadores demuestra discriminación? | Indica una diferencia de desempeño que debe investigarse con muestras representativas, calibración, intervalos e impactos en decisiones. |
| ¿Cómo se interpreta el ROI? | Es una proyección de año 1 con costos explícitos. La diferencia de MAE no se convierte directamente en ahorros. |
| ¿Cómo aseguran la paridad del simulador? | Ambos modos comparten esquema e inferencia. Se verificó un perfil a través de HTTP y del navegador y se probaron respuestas inválidas. |
| ¿Qué falta para producción? | Validación temporal con cartera real, mitigación de diferencias por grupo, monitoreo, controles operativos y aprobación formal. |
| ¿Cuál fue la desviación de gestión? | El modelo previo quedó sobre la referencia de MAE CV. Se evaluó regresión directa con las mismas particiones. El seguimiento conserva el resultado y el control pendiente de subgrupos. |
| ¿Qué metodología se usó y por qué se descartó cascada? | EP4 adoptó CRISP-DM porque permite volver a una fase anterior. El paso de evaluación a modelado se ve al probar la regresión directa tras detectar que el modelo logarítmico superaba la referencia de MAE CV. |
| ¿Qué acredita un hito técnico cerrado en Linear? | Acredita que se revisaron las tareas y las evidencias de EP6. El plan EP4 también exige aprobaciones del patrocinador para G1, G3 y G5, cuya constancia sigue pendiente. |

[Plan EP4, secciones 2.4 y 3.2](referencias/Plan_EP4.pdf) · [Estado de las compuertas EP4](../gestion/reportes_estado.md) · [Criterios y evidencias por hito EP6](../gestion/MedicalCost_Predictor_Seguimiento.md)

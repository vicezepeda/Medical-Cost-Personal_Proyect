# Defensa de MedicalCost Predictor · EP6
Equipo MedicalCost Predictor · SCY1102

[Presentación editable](../entregables/MedicalCost_Predictor_Defensa_EP6.pptx) · [Guía de ejecución](MedicalCost_Predictor_Ejecucion.md) · [Proyecto en Linear](https://linear.app/duocuc2026/project/medicalcost-predictor-ep6-b503ee94e0e0)

Abre el dashboard y Swagger antes de presentar. Deja el simulador con el perfil inicial y el tablero en la lista de hitos. Si falla la conexión, usa la captura de la diapositiva 8 y el JSON de evidencia. Los bloques suman 10:00 e incluyen pausas y las acciones en pantalla. La exposición efectiva se registra en DUO-13.

## 1 · 0:00–0:50 · MedicalCost Predictor

Partimos de una pregunta concreta. Si una organización utiliza un único cargo promedio como referencia, ¿cuánta precisión gana al incorporar edad, IMC y otros atributos disponibles? Implementamos un prototipo que estima ese cargo, conserva el proceso de entrenamiento y permite que el mismo perfil se consulte desde una interfaz o por HTTP. La comparación principal es contra la media de entrenamiento. Voy a mostrar la reducción del error, dónde sigue fallando el modelo y qué tendría que medirse antes de justificar una inversión. Cierro con la evidencia del plan y dos escenarios económicos.

## 2 · 0:50–1:55 · Cuánto perdemos con una prima uniforme

Supongamos una cartera de mil pólizas. En un segmento de 250, el costo esperado supera en 400 dólares la prima uniforme. La brecha bruta anual del segmento sería de cien mil dólares. El margen neto dependería también de los otros segmentos, los gastos y las renovaciones. Una prima promedio puede cubrir la cartera en agregado y, aun así, dejar mal representados algunos grupos. En el conjunto público, usar una media única tiene un MAE cercano a nueve mil dólares en prueba. Esa cifra mide incertidumbre predictiva y la brecha de cien mil pertenece al escenario hipotético. Para pasar del error al dinero hay que observar primas y costos de una cartera real.

## 3 · 1:55–2:40 · Objetivo y alcance

El objetivo es entregar una estimación repetible y defendible, con seis entradas y una salida en dólares. Lo acotamos a exploración, entrenamiento, API, dashboard y documentación de decisiones. Cualquier persona con el repositorio y Python puede repetir el flujo. La demostración usa una API local. Producción, integración transaccional y nuevos datos quedaron fuera del alcance. Eso permite evaluar la decisión técnica sin confundir una demostración funcional con un sistema aprobado para decidir primas.

## 4 · 2:40–3:35 · Quién gana y qué debe validar

Suscripción es el beneficiario directo porque puede estudiar la diferencia entre perfiles. A los asegurados les interesa que la estimación sea comprensible y previsible. Finanzas puede respaldar el piloto si confirma el margen retenido y el tiempo liberado. TI y Datos necesitan que dos canales compartan el mismo contrato y la misma versión del modelo. Cumplimiento debe revisar el uso de variables como sexo, región y tabaquismo y exigir control humano. En un piloto, cada área debe acordar un criterio verificable. Una reducción global del error por sí sola no resuelve las diferencias entre grupos.

## 5 · 3:35–4:35 · Datos y preparación

Usamos 1.338 filas del dataset público Medical Cost Personal. La base tiene cero nulos y un duplicado exacto. Conservamos ambas copias y las agrupamos para que no crucen particiones. Quedaron 1.069 filas para entrenar y 269 para probar. Dentro de entrenamiento hicimos validación cruzada de cinco pliegues agrupados y estratificados por tabaquismo, con semilla 42. Las numéricas se escalan y las categóricas se codifican con one-hot. Cada preprocesador se ajusta con los datos de su pliegue. El horizonte de los cargos no está confirmado, por eso la anualización del negocio aparece solo como supuesto.

## 6 · 4:35–5:55 · Modelo y resultados

La media es la línea base. El proyecto previo estudió dos regresiones sobre log-cargos, una aditiva y otra con interacción entre IMC y tabaquismo. Entrenamos además una regresión directa en USD, con salida acotada a cero. La elegimos por el menor MAE fuera de pliegue, 4.233 dólares, frente a la referencia de 4.824. En prueba obtuvo un MAE de 4.120, RMSE de 5.884 y R² de 0,737. Eso reduce el MAE un 53,7 % frente a la media. El RMSE penaliza más los errores grandes. La debilidad aparece al segmentar. El MAE en fumadores es cercano a 8.610, versus 2.913 en no fumadores. Por eso el resultado agregado es insuficiente para justificar una decisión individual. [Pausa para mostrar las dos columnas de errores.]

## 7 · 5:55–6:45 · Arquitectura

El entrenamiento lee el CSV y guarda un solo objeto con el preprocesador y la regresión. Pydantic valida las categorías y los rangos. FastAPI carga el objeto una vez al arrancar y lo reutiliza para cada consulta. El dashboard puede servir una predicción local o llamar al endpoint. Ambos mecanismos usan las mismas reglas para formar las entradas y redondear la salida. El JSON de resultados conserva la evidencia de validación y alimenta las tarjetas y el control de la meta.

## 8 · 6:45–8:05 · Demostración

Comienzo con 30 años e IMC 25, cero hijos, no fumador y región noreste. En modo local el cargo estimado es de 4.335,51 dólares. [Cambia el IMC de 25 a 30 y muestra el recálculo. Devuelve el IMC a 25.] Selecciono API REST y pulso Consultar API. El valor coincide con el local. [Abre Swagger o muestra el JSON de la diapositiva.] El endpoint de salud devuelve ok. Si ingreso edad 17, la API responde 422. [Muestra la pestaña Análisis si queda tiempo.] Aquí se puede revisar la distribución por tabaquismo y el efecto sobre el error al permutar cada variable. La pestaña de plan registra la brecha respecto al MAE objetivo.

## 9 · 8:05–9:00 · Plan y ejecución

Linear reúne cuatro hitos y 13 issues con puntos, responsable y estados. [Muestra los hitos y abre DUO-12.] El cambio técnico principal fue introducir una regresión directa porque el modelo logarítmico previo superaba el umbral. El reporte por hito registra la decisión y su evidencia. La demostración es local, dentro del alcance. La iniciativa superior quedó registrada en la descripción del proyecto y su enlace formal está pendiente. El issue de exposición sigue abierto hasta defender el trabajo y responder preguntas.

## 10 · 9:00–10:00 · ROI y decisión

Con 15.000 dólares de costo total en el primer año, el escenario conservador suma 16.000 dólares de beneficio bruto. Eso entrega un ROI de 6,7 %. El optimista suma 38.000 y alcanza 153,3 %. En ambos contamos corrección parcial de la brecha, margen de renovaciones incrementales y tiempo operativo liberado. Los valores son supuestos editables. Un estudio de plataforma analítica reportó alrededor de cuatro veces el costo en ROI neto y 11 meses de recuperación, en un horizonte y una escala distintos. La recomendación es un piloto en paralelo con cartera representativa, revisión por segmento y medición del impacto antes de incorporar el modelo a decisiones de primas. [Cierra en 10:00.]

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

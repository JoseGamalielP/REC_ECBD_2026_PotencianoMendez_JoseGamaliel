# Planeación del Proyecto de Análisis de Datos

UNIVERSIDAD TECNOLÓGICA DE TULA-TEPEJI

Ingeniería en Desarrollo y Gestión de Software

**Asignatura:** Extracción de Conocimiento en Bases de Datos

**Modalidad:** Recursamiento 2026

**Unidad I:** Introducción al análisis de datos

**Proyecto:** Análisis y predicción de calidad del aire

**Alumno:** José Gamaliel Potenciano Méndez

**Matrícula:** 23301258

**Grupo:** 10IDGS - G1

**Docente:** Ing. Jose Luis Herrera Gallardo

**Periodo:** Septiembre-Diciembre de 2026

**Fecha de elaboración:** 1 de octubre de 2026

**Entrega de Unidad I:** 2 de octubre de 2026

---

## 1. Contexto y descripción del proyecto

El proyecto estudiará el conjunto Air Quality, que relaciona las respuestas horarias de cinco sensores químicos con mediciones de referencia de contaminantes y condiciones ambientales de un sitio urbano italiano. La fuente advierte sensibilidad cruzada y cambios en el comportamiento de los sensores a lo largo del tiempo (Vito, 2008). Por ello, una lectura del sensor no debe interpretarse directamente como la concentración real de un contaminante.

La necesidad de información consiste en determinar qué señales del dispositivo permiten estimar CO y qué limitaciones tendría esa estimación. El producto será académico: un análisis reproducible que contraste predicciones con la medición de referencia y explique sus errores. No sustituirá un equipo certificado ni emitirá alertas de salud pública.

### 1.1 Planteamiento del problema

Se dispone de datos históricos, pero todavía no se ha establecido la capacidad de las señales PT08 para estimar CO en observaciones no utilizadas durante el ajuste. También es necesario distinguir las relaciones con temperatura y humedad de los patrones debidos al tiempo, los faltantes o la deriva instrumental. Sin una planeación de variables, particiones y métricas, podría obtenerse una evaluación optimista que no represente el uso previsto.

### 1.2 Pregunta principal de análisis

¿En qué medida las cinco respuestas de los sensores PT08 y las variables T, RH y AH permiten estimar CO(GT) en observaciones posteriores del mismo sitio, y cómo cambia el error entre bandas de concentración definidas para el proyecto?

### 1.3 Objetivo general

Analizar la relación entre las respuestas de los sensores, las condiciones ambientales y la concentración de CO para desarrollar y evaluar posteriormente una estimación reproducible de CO(GT), una clasificación por bandas académicas y una descripción de patrones ambientales, aplicando CRISP-DM y validación temporal.

### 1.4 Objetivos específicos

1. Documentar la procedencia, integridad, variables y limitaciones del dataset mediante una ficha técnica y un diccionario de sus 15 columnas.
2. Establecer un protocolo reproducible para el tratamiento posterior de faltantes y la separación temporal, sin modificar el archivo original.
3. Comparar posteriormente un modelo de regresión lineal y un bosque aleatorio con una referencia constante, mediante MAE, RMSE y R² en periodos reservados.
4. Evaluar posteriormente una clasificación de CO en tres bandas mediante macro-F1, matriz de confusión y recall por clase, documentando los límites de cada intervalo.
5. Examinar posteriormente patrones mediante clustering y PCA, reportando perfiles, estabilidad de grupos y varianza explicada sin atribuirles significado sanitario automático.

---

## 2. Alcance y limitaciones

**Alcance del proyecto integrador.** Se analizará únicamente el sitio y periodo contenidos en Air Quality. La unidad de análisis será una observación horaria. Se propondrá estimar la concentración de la misma hora usando las respuestas sensor/ambiente disponibles en ese momento; no se plantea un pronóstico del día siguiente. NO2(GT) podrá describirse como variable contextual, sin sustituir el objetivo principal de CO.

**Alcance de esta entrega.** Unidad I incluye planeación, consulta de fuentes, revisión estructural del original y documentación de GitHub. No se ejecutan limpieza, ETL, modelos, clasificación, clustering, PCA, Data Warehouse ni dashboard. Las carpetas de la plantilla reservadas para esas tareas se conservan sin implementación.

### 2.1 Limitaciones y respuesta prevista

| Limitación | Consecuencia para el análisis | Respuesta propuesta |
| --- | --- | --- |
| Un sitio y datos históricos | No permiten generalizar directamente a otras ciudades ni a 2026. | Delimitar las conclusiones al archivo y proponer validación externa como trabajo futuro. |
| Faltantes codificados como -200 | Pueden confundirse con valores físicos y sesgar métricas. | En una copia futura, identificarlos antes de analizar; no imputar la variable objetivo. |
| Dependencia temporal y deriva | Una partición aleatoria puede sobreestimar la generalización. | Reservar periodos posteriores y revisar errores por bloque temporal. |
| Sensibilidad cruzada y correlación entre sensores | Las señales nominales no son mediciones exclusivas de cada gas. | Comparar entradas y reconocer incertidumbre; no inferir causalidad. |
| Diferencias entre ficha y archivo | El conteo y el periodo pueden reportarse incorrectamente. | Separar explícitamente los metadatos publicados de los observados. |
| Bandas académicas de CO | No equivalen a riesgo sanitario ni a un índice oficial. | Mantener nombres de concentración y advertir su propósito didáctico. |

La ficha UCI presenta CC BY 4.0 y también una nota histórica de uso solo para investigación. Ante esa discrepancia, el alcance adoptado será estrictamente académico, con atribución y sin explotación comercial. No se añadirán datos personales, tráfico, viento o ubicación detallada que no estén disponibles en las columnas.

---

## 3. Descripción del conjunto de datos

**Nombre y fuente:** Air Quality, UCI Machine Learning Repository. Referencia oficial: Vito (2008), DOI 10.24432/C59K5F. Archivo de trabajo: `data/raw/air+quality/AirQualityUCI.xlsx`; hoja `AirQualityUCI`. Se conservan el CSV y el ZIP originales.

La ficha anuncia **9,358 registros y 15 características**. La lectura local identificó **9,357 filas con datos, más un encabezado, y 15 columnas con nombre**. La hoja tiene dimensiones físicas de 9,472 × 17 por celdas vacías adicionales. Contarlas no representa observaciones extra. No se eliminaron filas ni columnas: el conteo se realizó solo en memoria.

El archivo abarca del **10 de marzo de 2004 a las 18:00 al 4 de abril de 2005 a las 14:00**. La descripción general de UCI menciona marzo de 2004 a febrero de 2005; se conserva la diferencia sin alterar fechas. El tamaño local es 1,298,197 bytes, aproximadamente 1.30 MB. El XLSX coincide byte por byte con el del ZIP.

### 3.1 Diccionario preliminar de variables

| Variable real | Información y unidad | Tipo general y uso previsto |
| --- | --- | --- |
| Date | Fecha del registro. | Temporal; ordenar y derivar calendario. |
| Time | Hora del registro. | Temporal; ordenar y derivar hora. |
| CO(GT) | CO de referencia; mg/m³. | Numérica; objetivo principal. |
| PT08.S1(CO) | Respuesta del sensor nominal de CO. | Numérica; entrada candidata. |
| NMHC(GT) | Hidrocarburos no metánicos; µg/m³. | Numérica; referencia contextual. |
| C6H6(GT) | Benceno; µg/m³. | Numérica; referencia contextual. |
| PT08.S2(NMHC) | Respuesta nominal a NMHC. | Numérica; entrada candidata. |
| NOx(GT) | Óxidos de nitrógeno; ppb. | Numérica; referencia contextual. |
| PT08.S3(NOx) | Respuesta nominal a NOx. | Numérica; entrada candidata. |
| NO2(GT) | Dióxido de nitrógeno; µg/m³. | Numérica; descripción contextual. |
| PT08.S4(NO2) | Respuesta nominal a NO2. | Numérica; entrada candidata. |
| PT08.S5(O3) | Respuesta nominal a O3. | Numérica; entrada candidata. |
| T | Temperatura; °C. | Numérica; entrada ambiental. |
| RH | Humedad relativa; %. | Numérica; entrada ambiental. |
| AH | Humedad absoluta. | Numérica; entrada ambiental. |

Las cinco PT08 son respuestas instrumentales, no concentraciones de gas. No se asigna una unidad no documentada a esas señales ni a AH. Aunque algunas etiquetas de tipo de la ficha UCI son categóricas o enteras, el archivo presenta mediciones numéricas, algunas decimales. Para el diseño se utilizará su significado físico. El marcador -200 representa faltantes (Vito, 2008).

---

## 4. Comparación conceptual

IA, Machine Learning, Data Mining y Big Data no son sinónimos. IA es un campo amplio; ML aprende a partir de datos y puede formar parte de una solución de IA. Data Mining busca patrones útiles con apoyo de estadística y ML. Big Data se refiere a necesidades de escala y arquitectura, no a un algoritmo. La siguiente comparación aplica estas distinciones al proyecto (National Institute of Standards and Technology [NIST], s. f.-a, s. f.-b; IBM, s. f.-b; Chang & Grady, 2019).

### 4.1 Inteligencia Artificial y Machine Learning

| Dimensión | Inteligencia Artificial | Machine Learning |
| --- | --- | --- |
| Características | Sistemas orientados a tareas de razonamiento, percepción, aprendizaje o decisión. Incluye reglas y técnicas aprendidas. | Ajusta modelos con ejemplos; distingue aprendizaje supervisado y no supervisado. Requiere evaluación con datos no usados para ajustar. |
| Beneficios | Apoya decisiones y automatiza tareas complejas o repetitivas. Puede combinar conocimiento explícito y predicciones. | Permite estimar valores, asignar clases y descubrir estructura sin programar cada relación manualmente. |
| Restricciones | Depende de objetivos, información y supervisión adecuados; una salida plausible no garantiza que sea correcta. | La calidad y representatividad de los datos limitan la generalización. No demuestra causalidad. |
| Retos | Explicabilidad, sesgos, responsabilidad y control de resultados. | Sobreajuste, fuga de información, faltantes, desbalance y cambios temporales. |
| Casos de aplicación | Asistentes, sistemas de apoyo a decisiones y robots; en este caso, marco conceptual para apoyo ambiental. | Predicción de demanda, detección de fraude y calibración de sensores; aquí, regresión de CO y clasificación de sus bandas. |
| Lenguajes y herramientas | Python; reglas programadas y bibliotecas de aprendizaje como scikit-learn. No se requiere una IA generativa. | Python o R; scikit-learn para regresión, clasificación, validación y transformaciones. |
| Papel en el proyecto | Enmarca el uso responsable de una estimación; no se construirá un agente autónomo. | Aporta los modelos y las métricas propuestos para etapas posteriores. |

La selección del modelo no se basará en que una técnica se anuncie como IA, sino en su utilidad, trazabilidad y error sobre datos reservados. Un método sencillo será preferible si logra resultados comparables y permite explicar mejor sus límites.

---

### 4.2 Data Mining y Big Data

| Dimensión | Data Mining | Big Data |
| --- | --- | --- |
| Características | Busca patrones, asociaciones, grupos y relaciones útiles en datos, dentro de un proceso analítico. | Conjuntos con volumen, velocidad, variedad o variabilidad que justifican arquitectura escalable. |
| Beneficios | Convierte registros en hallazgos interpretables y plantea hipótesis verificables. | Permite integrar y procesar flujos o colecciones que exceden una solución local adecuada. |
| Restricciones | Los patrones dependen de la calidad de los datos y no implican causas. Puede no encontrar relaciones útiles. | Más infraestructura no asegura datos mejores ni modelos más precisos; añade costos y complejidad. |
| Retos | Distinguir señales reales de asociaciones espurias, elegir variables e interpretar grupos. | Particionado, distribución, consistencia, seguridad y coordinación de recursos. |
| Casos de aplicación | Segmentación de clientes, asociaciones de compra y detección de anomalías; aquí, patrones sensor/ambiente. | Telemetría de miles de dispositivos y flujos de eventos a gran escala; una red urbana masiva podría requerirlo. |
| Lenguajes y herramientas | Python, R y SQL; pandas, SQLite y scikit-learn. | Python, SQL, Scala o Java; Apache Spark como ejemplo de procesamiento distribuido. |
| Papel en el proyecto | Orienta la extracción y evaluación de conocimiento usando CRISP-DM. | Tema comparativo: el archivo local no justifica implementar Spark ni un clúster. |

Para Air Quality, el volumen observado permite planear un flujo local. Esta decisión se basa en el tamaño del archivo y la complejidad prevista, no en un umbral universal de filas. Los conceptos se complementan, pero no todos requieren una implementación separada (IBM, s. f.-b; Chang & Grady, 2019; Apache Software Foundation, s. f.).

---

## 5. Lenguaje y herramientas propuestas

Se propone un entorno local con Python 3 y bibliotecas abiertas. La combinación permite documentar lectura, preparación futura, modelos y evaluación sin una infraestructura distribuida. Las versiones exactas se fijarán cuando comience la implementación; no se presentan paquetes propuestos como ya instalados.

| Componente | Función propuesta | Justificación y límite |
| --- | --- | --- |
| Python 3 | Lenguaje del flujo analítico. | Integra lectura, estadística y modelos en scripts reproducibles. |
| pandas y NumPy | Tablas, fechas, operaciones numéricas y revisión de datos. | Adecuados para el tamaño local; las transformaciones futuras se documentarán. |
| openpyxl | Lectura del archivo XLSX. | Permite inspeccionar el original sin guardarlo ni cambiarlo. |
| scikit-learn | Pipelines, modelos supervisados, clustering, PCA y métricas. | Interfaz consistente; separación explícita entre ajuste y evaluación. |
| SQLite y SQL | Guardar una copia preparada y consultar resúmenes posteriormente. | Gestor embebido suficiente para trabajo individual y este volumen; no requiere servidor. No se crea una base en Unidad I. |
| Jupyter y VS Code | Exploración documentada y edición de scripts. | Combina explicación con código; los resultados deben poder reproducirse. |
| Matplotlib | Gráficas temporales, dispersión, errores y resultados. | Permite producir figuras etiquetadas para el informe. No se construye un dashboard en esta entrega. |
| Git y GitHub | Control de versiones y entrega de evidencias. | Permite revisar cambios, conservar la plantilla y vincular documentos con su historial. |

La propuesta de tablas se apoya en la documentación de pandas; la elección de SQLite, en sus usos para análisis local; y la visualización, en Matplotlib. El uso de pipelines y la separación de prueba se fundamentan en las recomendaciones de scikit-learn (pandas development team, s. f.; SQLite, s. f.; Matplotlib development team, s. f.; scikit-learn developers, s. f.-b).

### 5.1 Forma de trabajo y reproducibilidad

El original permanecerá en `data/raw`. Los derivados futuros se guardarán en `data/processed`; el código, en `src` o `notebooks`; las consultas, en `sql`; y los documentos, en `docs`. Antes de modelar se registrarán versiones, parámetros, semillas y reglas de selección. El repositorio distinguirá propuestas de resultados ejecutados. No se publicarán contraseñas, tokens ni archivos de entorno personales.

El análisis será ejecutable en una computadora local. La instalación o uso de un gestor distribuido no se justifica por el tamaño actual. Si los requisitos del curso cambian, se revisará la planeación antes de incorporar nuevas herramientas.

---

## 6. Metodología CRISP-DM

CRISP-DM significa Cross-Industry Standard Process for Data Mining. Organiza el trabajo en seis etapas y permite revisar decisiones cuando la evidencia obliga a volver a una fase anterior. Se selecciona porque relaciona la pregunta del proyecto con los datos, la evaluación y la entrega, en lugar de comenzar directamente con algoritmos (Chapman et al., 2000; IBM, s. f.-a).

En términos generales, sus etapas son: comprender la necesidad; conocer los datos; prepararlos; modelar; evaluar la utilidad y validez; y entregar o poner en uso los resultados. El ciclo no garantiza éxito ni sustituye la revisión humana. En este proyecto, el despliegue será académico: documentación reproducible y resultados explicados, no un servicio de alertas.

### 6.1 Aplicación preliminar al caso asignado

| Etapa y propósito | Aplicación propuesta a Air Quality | Evidencia o criterio de revisión |
| --- | --- | --- |
| Comprensión del negocio: definir necesidad y éxito. | Delimitar estimación horaria de CO, usuarios académicos, objetivos, exclusiones y bandas. | Planeación de Unidad I y pregunta verificable. |
| Comprensión de datos: revisar significado y calidad. | Confirmar origen, conteos y diccionario; después medir faltantes, fechas repetidas y cobertura temporal. | Ficha actual y futuro informe de calidad; no confundir -200 con concentración. |
| Preparación: construir entradas apropiadas. | Trabajar solo con copias; convertir -200 a faltante, formar fecha-hora, revisar duplicados y definir particiones. Aprender imputación y escala solo en entrenamiento. | Protocolo, conteos antes/después y transformaciones reproducibles. |
| Modelado: ajustar alternativas. | Comparar regresión lineal y bosque aleatorio; clasificación logística y árbol; explorar K-means y PCA. | Configuraciones y modelos futuros con referencias sencillas de comparación. |
| Evaluación: contrastar validez y utilidad. | Medir errores, macro-F1, matriz de confusión y estabilidad. Revisar por periodos, bandas y disponibilidad de sensores. | Tabla de resultados reales y explicación de fallos; volver a preparación si hay problemas. |
| Despliegue: comunicar y conservar resultados. | Entregar informe, scripts, documentación y repositorio reproducible; declarar límites y trabajo pendiente. | Evidencias finales y explicación individual. No se desplegará un sistema operativo de salud. |

**Estado al cierre de Unidad I:** se completan la planeación y una primera revisión estructural. La preparación, el modelado y su evaluación quedan programados, no realizados. Si la calidad del objetivo o la cobertura temporal impiden un análisis válido, se reportará la limitación y se consultará al docente antes de cambiar el alcance.

---

## 7. Definición preliminar del análisis posterior

### 7.1 Regresión

La variable objetivo será **CO(GT)**, concentración horaria de CO en mg/m³. La hipótesis a evaluar es que las señales de los sensores y el ambiente permiten una estimación mejor que una referencia constante; no se afirma que ya exista ese resultado.

Las ocho entradas iniciales serán **PT08.S1(CO), PT08.S2(NMHC), PT08.S3(NOx), PT08.S4(NO2), PT08.S5(O3), T, RH y AH**. S1 es una candidata por su orientación nominal a CO; las otras respuestas pueden aportar señales complementarias. La selección final dependerá de cobertura, redundancia y validación, no del nombre del sensor solamente. Date y Time servirán para ordenar; hora, día de la semana o mes serán variables derivadas opcionales, no columnas originales adicionales.

Se compararán regresión lineal y Random Forest con un predictor constante obtenido del entrenamiento. La métrica principal será MAE; RMSE señalará errores grandes y R² complementará la comparación. No se incluirá CO(GT) entre las entradas. Las otras concentraciones GT se excluyen del escenario principal porque requieren un analizador de referencia que se busca complementar; esa exclusión es de disponibilidad, no la afirmación de que toda correlación sea fuga.

### 7.2 Clasificación y criterio de categorías

Se propondrá crear **banda_CO** a partir de un CO válido, con intervalos fijados antes de observar resultados de modelos:

| Clase académica | Regla en mg/m³ |
| --- | --- |
| Concentración baja | 0 ≤ CO(GT) < 1 |
| Concentración media | 1 ≤ CO(GT) < 3 |
| Concentración alta | CO(GT) ≥ 3 |

Estos cortes son una decisión didáctica preliminar que facilita comparar tres rangos con límites simples. **No proceden de una norma sanitaria, no equivalen a buena/mala calidad del aire y no son etiquetas ya presentes en UCI.** Se revisará el número de ejemplos por clase antes de entrenar. Si alguna clase carece de soporte suficiente, se consultará al docente y se documentará cualquier revisión usando solo entrenamiento, nunca los resultados de prueba.

Los registros con CO faltante (-200 o celda vacía) no tendrán etiqueta y no se imputarán para entrenar o evaluar. CO(GT) y banda_CO se excluirán de las entradas. Se compararán regresión logística multiclase y árbol de decisión con una referencia de clase mayoritaria, usando macro-F1, recall por clase y matriz de confusión; accuracy será solo complementaria.

---

### 7.3 Análisis no supervisado

Se propondrá aplicar K-means a las mismas ocho variables sensor/ambiente, después de un tratamiento documentado de faltantes y escalamiento. Se explorarán de dos a seis grupos con silueta, estabilidad frente a semillas e interpretación de sus perfiles. Un resultado sin separación útil también será válido y deberá comunicarse; los grupos no se llamarán categorías sanitarias.

PCA se utilizará para resumir variación, estudiar cargas y visualizar componentes. Se informará la varianza explicada y no se supondrá que dos componentes conservan toda la información. CO(GT) podrá utilizarse después para describir los grupos, no para construirlos. Estas operaciones se planearon, pero no se ejecutaron (scikit-learn developers, s. f.-a, s. f.-d).

### 7.4 Evaluación temporal y control de fuga

Se propone ordenar por fecha-hora y asignar, antes de aprender transformaciones, el 60% inicial a entrenamiento, el 20% siguiente a validación y el 20% final a prueba. Las fronteras conservarán juntas las observaciones de una misma fecha-hora. Los conteos efectivos se documentarán tras la revisión de calidad; no se inventan ahora.

Los parámetros de imputación de entradas, escalamiento, selección y modelos se obtendrán solamente de entrenamiento; validación permitirá elegir alternativas y prueba se reservará para una evaluación final. No se rellenarán huecos con información futura entre particiones. Si se utilizan rezagos, se respetará su disponibilidad y se ajustará la separación temporal. Este diseño responde a la dependencia de la serie (scikit-learn developers, s. f.-b, s. f.-c).

**Criterio preliminar de éxito:** superar la referencia en validación para MAE y macro-F1 y contrastar después el resultado en prueba. No se fija una precisión garantizada. Si el modelo no supera la referencia o falla en periodos/bandas, se reportará y se limitarán las conclusiones. También se contará como resultado útil detectar sensores con cobertura insuficiente o relaciones inestables.

## 8. Resultados esperados

1. Diccionario verificable y diagnóstico posterior de faltantes, cobertura temporal y coherencia de variables.
2. Gráficas que describan relaciones sensor/ambiente/CO y su variación temporal sin interpretarlas como causalidad.
3. Comparación de errores de regresión y desempeño de clasificación contra referencias simples, con resultados por banda y periodo.
4. Perfiles de grupos y resumen PCA, si la calidad de datos permite interpretarlos.
5. Evidencias reproducibles y conclusiones que identifiquen utilidad, incertidumbre y límites del estudio.

Estos son productos esperados, no hallazgos obtenidos. En esta entrega no se informan correlaciones calculadas, métricas de modelos ni grupos descubiertos.

---

## 9. Cronograma preliminar

La guía oficial establece el periodo **23 de septiembre al 20 de noviembre de 2026** y la entrega de Unidad I el **2 de octubre** (Herrera Gallardo, 2026). Las fechas intermedias de la tabla son propuestas personales de planeación, sujetas a las instrucciones de las siguientes unidades; no se presentan como fechas oficiales adicionales.

| Periodo de 2026 | Trabajo previsto | Producto y dependencia |
| --- | --- | --- |
| 23-28 de septiembre | Inicio y conservación del dataset; estructura del repositorio. | Base de Actividad 0, realizada previamente. |
| 29 de septiembre-2 de octubre | Contexto, objetivos, revisión estructural, comparación conceptual, CRISP-DM y plan. | PDF y README de Unidad I; entrega oficial 2 de octubre. |
| 3-9 de octubre | Revisión de calidad y diseño de preparación. | Informe de faltantes/fechas/unidades, previa autorización de la etapa. |
| 10-16 de octubre | Preparación reproducible y consultas SQL propuestas. | Copia derivada y reglas; depende de revisión de calidad. |
| 17-23 de octubre | Descripción de relaciones y comparación de regresión. | Gráficas y métricas de validación; depende de particiones documentadas. |
| 24-30 de octubre | Clasificación por bandas y revisión por clase. | Matrices y macro-F1; depende de soporte suficiente de las clases. |
| 31 de octubre-6 de noviembre | Clustering y PCA. | Perfiles y varianza explicada; depende de datos preparados. |
| 7-13 de noviembre | Evaluación final y revisión de estabilidad y errores. | Resultados de prueba y límites; depende de selección con validación. |
| 14-20 de noviembre | Integración, revisión del repositorio y preparación de explicación individual. | Entrega integradora según guía final; cierre oficial del periodo el 20 de noviembre. |

**Responsable:** José Gamaliel Potenciano Méndez. Se reservará tiempo de la última semana para corregir documentación y verificar reproducción. Una falta de datos útiles se tratará como una limitación, no se resolverá inventando observaciones ni cambiando de dataset sin autorización.

## 10. Evidencias y control de integridad

Repositorio: https://github.com/JoseGamalielP/REC_ECBD_2026_PotencianoMendez_JoseGamaliel

Entregables de Unidad I: este PDF, el README actualizado y el dataset original conservado en `data/raw/air+quality/`. Se mantiene toda la estructura de la plantilla, incluidas las carpetas reservadas para tareas futuras. El archivo de entrega usa el nombre indicado en la publicación de la actividad: **PotencianoMendez_JoseGamaliel_U1_PlaneacionProyecto.pdf**.

SHA-256 de `AirQualityUCI.xlsx`, verificado el 1 de octubre de 2026:

`c92d102bb35cd4c0b42c0b6a1336c4065ccdca7069f80a6890ee1b7e3124bd5d`

El hash y la igualdad con el ZIP permiten comprobar que el original no cambió. Las evidencias no incluyen resultados de etapas todavía no realizadas.

---

## 11. Referencias

Apache Software Foundation. (s. f.). *Spark documentation*. Recuperado el 1 de octubre de 2026, de https://spark.apache.org/docs/latest/

Chang, W. L., & Grady, N. (2019). *NIST Big Data Interoperability Framework: Volume 1, Definitions* (NIST SP 1500-1r2). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.1500-1r2

Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS. https://public.dhe.ibm.com/software/analytics/spss/documentation/modeler/14.2/es/CRISP-DM.pdf

Herrera Gallardo, J. L. (2026). *Actividad de evaluación - Unidad I: Recursamiento 2026. Extracción de Conocimiento en Bases de Datos* [Guía de actividad, archivo 05_Actividad_Evaluacion_U1_Recursamiento_ECBD_2026.pdf]. Universidad Tecnológica de Tula-Tepeji.

IBM. (s. f.-a). *Data preparation in the mining process*. Recuperado el 1 de octubre de 2026, de https://www.ibm.com/docs/en/db2/11.1.0?topic=studio-data-preparation-in-mining-process

IBM. (s. f.-b). *What is data mining?* Recuperado el 1 de octubre de 2026, de https://www.ibm.com/think/topics/data-mining

Matplotlib development team. (s. f.). *Quick start guide*. Recuperado el 1 de octubre de 2026, de https://matplotlib.org/stable/users/explain/quick_start.html

National Institute of Standards and Technology. (s. f.-a). *Artificial intelligence*. Computer Security Resource Center Glossary. Recuperado el 1 de octubre de 2026, de https://csrc.nist.gov/glossary/term/artificial_intelligence

National Institute of Standards and Technology. (s. f.-b). *Machine learning*. Computer Security Resource Center Glossary. Recuperado el 1 de octubre de 2026, de https://csrc.nist.gov/glossary/term/machine_learning

pandas development team. (s. f.). *Package overview*. Recuperado el 1 de octubre de 2026, de https://pandas.pydata.org/docs/getting_started/overview.html

---

## Referencias continuación

scikit-learn developers. (s. f.-a). *Clustering*. Recuperado el 1 de octubre de 2026, de https://scikit-learn.org/stable/modules/clustering.html

scikit-learn developers. (s. f.-b). *Common pitfalls and recommended practices*. Recuperado el 1 de octubre de 2026, de https://scikit-learn.org/stable/common_pitfalls.html

scikit-learn developers. (s. f.-c). *Cross-validation: Evaluating estimator performance*. Recuperado el 1 de octubre de 2026, de https://scikit-learn.org/stable/modules/cross_validation.html

scikit-learn developers. (s. f.-d). *Decomposing signals in components (matrix factorization problems)*. Recuperado el 1 de octubre de 2026, de https://scikit-learn.org/stable/modules/decomposition.html

SQLite. (s. f.). *Appropriate uses for SQLite*. Recuperado el 1 de octubre de 2026, de https://www.sqlite.org/whentouse.html

Vito, S. (2008). *Air Quality* [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C59K5F

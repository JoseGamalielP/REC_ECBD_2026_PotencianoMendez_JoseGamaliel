# Análisis y predicción de calidad del aire

Proyecto Integrador de Recursamiento 2026 de **Extracción de Conocimiento en Bases de Datos (ECBD)**.
Este repositorio no corresponde a la asignatura Aplicaciones Web Progresivas.

**Alumno:** José Gamaliel Potenciano Méndez.

**Grupo:** 10IDGS - G1.

**Docente:** Ing. Jose Luis Herrera Gallardo.

**Periodo:** 23 de septiembre al 20 de noviembre de 2026.

## Estado y entrega actual

Unidad I: planeación formal del análisis. Se verificó el original en modo lectura y se documentaron el problema, objetivos, herramientas, CRISP-DM, análisis posteriores y cronograma.

- [Planeación de Unidad I en PDF](docs/PotencianoMendez_JoseGamaliel_U1_PlaneacionProyecto.pdf).
- [Versión editable del contenido en Markdown](docs/U1_PlaneacionProyecto.md).
- Entrega de Unidad I: **2 de octubre de 2026**; valor de la actividad según la guía: 20% del proyecto de recursamiento.
- En esta entrega **no se ha realizado limpieza, ETL, entrenamiento, clasificación, clustering, PCA, Data Warehouse ni dashboard**. Las actividades analíticas descritas son propuestas para etapas posteriores.

## Problema y pregunta de análisis

Se busca estudiar si las respuestas del dispositivo multisensor y las condiciones ambientales permiten estimar la concentración de CO de referencia en observaciones no usadas para ajustar el modelo.

**Pregunta principal:** ¿En qué medida las cinco respuestas de los sensores PT08 y las variables T, RH y AH permiten estimar CO(GT) en observaciones posteriores del mismo sitio, y cómo cambia el error entre bandas de concentración definidas para el proyecto?

El objetivo es una estimación de la misma hora a partir de mediciones disponibles, no un pronóstico del día siguiente ni una evaluación sanitaria.

## Dataset original

- Nombre: **Air Quality**.
- Fuente: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/360/air+quality).
- Referencia: Vito, S. (2008). *Air Quality* [Conjunto de datos]. UCI Machine Learning Repository. https://doi.org/10.24432/C59K5F
- Archivo principal: [`data/raw/air+quality/AirQualityUCI.xlsx`](data/raw/air%2Bquality/AirQualityUCI.xlsx).
- Se conservan también el CSV original y el ZIP descargado.
- La ficha UCI anuncia 9,358 registros. El Excel local contiene **9,357 filas con datos, más el encabezado, y 15 columnas con nombre**. La dimensión física de la hoja es 9,472 filas por 17 columnas e incluye celdas vacías; no equivale al número de observaciones y variables.
- Fechas observadas en el archivo: **10/03/2004 18:00 a 04/04/2005 14:00**. No coinciden exactamente con el intervalo resumido en la descripción de UCI; se preserva y documenta esta diferencia.
- Tamaño del XLSX: 1,298,197 bytes.
- UCI identifica **-200** como marcador de valores faltantes. En el original no se reemplazó ningún valor.
- El XLSX coincide byte por byte con el contenido del ZIP local (verificación del 1 de octubre de 2026).
- SHA-256 del XLSX: `c92d102bb35cd4c0b42c0b6a1336c4065ccdca7069f80a6890ee1b7e3124bd5d`.

Columnas reales: `Date`, `Time`, `CO(GT)`, `PT08.S1(CO)`, `NMHC(GT)`, `C6H6(GT)`, `PT08.S2(NMHC)`, `NOx(GT)`, `PT08.S3(NOx)`, `NO2(GT)`, `PT08.S4(NO2)`, `PT08.S5(O3)`, `T`, `RH`, `AH`.

La ficha pública muestra CC BY 4.0 y, en su descripción histórica, una restricción a investigación. Este proyecto se limita al uso académico, atribuye el dataset y no propone explotación comercial.

## Análisis propuesto para etapas posteriores

- **Regresión:** estimar `CO(GT)` (mg/m³). Entradas principales: las cinco columnas PT08, `T`, `RH`, `AH`; hora y calendario derivados de `Date`/`Time` se evaluarán como extensión documentada.
- **Clasificación:** construir posteriormente `banda_CO` a partir del CO válido: baja si `0 <= CO < 1`, media si `1 <= CO < 3`, alta si `CO >= 3` mg/m³. Son intervalos académicos prefijados, no índices sanitarios ni etiquetas presentes en el original. Los objetivos faltantes no recibirán clase ni se imputarán.
- **Sin fuga de información:** no incluir `CO(GT)` ni `banda_CO` en las entradas. Las otras concentraciones de referencia tampoco se usarán en el escenario principal, porque requieren el analizador que se busca complementar.
- **No supervisado:** proponer clustering de las ocho variables sensor/ambiente y PCA para describir patrones y variación; no se ejecutan en Unidad I.
- **Evaluación prevista:** separación temporal 60%/20%/20% (entrenamiento/validación/prueba), parámetros aprendidos solo con entrenamiento, métricas MAE/RMSE/R² y macro-F1/matriz de confusión. No se promete un desempeño antes de medirlo.

## Forma de trabajo

1. Conservar `data/raw` sin cambios. Cualquier preparación futura tendrá una salida distinta en `data/processed` y una justificación documentada.
2. Revisar unidades, faltantes, orden temporal y disponibilidad real de las variables antes de modelar.
3. Mantener separados entrenamiento, validación y prueba; no aprender imputaciones, escalas o selección de variables con el conjunto de prueba.
4. Versionar documentos y código con Git; registrar dependencias y semillas cuando comience la implementación.
5. Registrar resultados reales, incluidos los negativos, sin fabricar métricas ni interpretar asociación como causalidad.

Herramientas propuestas: Python 3, pandas, NumPy, openpyxl para lectura, scikit-learn, SQLite, Jupyter/VS Code, Matplotlib, Git y GitHub. No es necesario instalar paquetes ni ejecutar modelos para consultar esta entrega: abre el PDF en `docs` y el original de Excel en `data/raw`.

## Estructura de la plantilla

```text
data/
  raw/
    air+quality.zip
    air+quality/
      AirQualityUCI.xlsx
      AirQualityUCI.csv
  processed/       # reservado para derivados futuros
docs/              # planeación y documentación
notebooks/         # reservado para análisis reproducibles
src/               # reservado para código
sql/               # reservado para consultas futuras
modelos/           # reservado para modelos futuros
dashboard/         # reservado por la plantilla; no implementado
README.md
```

Las carpetas vacías se conservan con `.gitkeep`; su existencia no implica que esas etapas ya se hayan realizado.

Repositorio: https://github.com/JoseGamalielP/REC_ECBD_2026_PotencianoMendez_JoseGamaliel

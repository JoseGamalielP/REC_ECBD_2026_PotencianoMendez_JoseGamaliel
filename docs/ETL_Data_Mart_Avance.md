# Avance de ETL y Data Mart

## Alcance

Esta etapa lee el CSV original de Air Quality y genera una copia procesada. El archivo de `data/raw/` no se modifica.

## Proceso ETL

1. **Extracción:** lectura de `AirQualityUCI.csv` con separador punto y coma y coma decimal.
2. **Transformación:** conversión del marcador `-200` a valor faltante en la copia, creación de `DateTime`, extracción de año, mes, día y hora, orden temporal y creación de `banda_CO` con las bandas académicas documentadas.
3. **Carga:** escritura de `data/processed/air_quality_etl.csv` en UTF-8.

El CSV conserva 9,471 filas físicas porque el archivo original contiene filas finales sin fecha y hora. Esas filas se conservan en la copia para que el diagnóstico sea trazable; las 114 fechas que no se pueden interpretar quedan como `DateTime` vacío y deberán tratarse con una regla documentada antes de modelar.

## Data Mart propuesto

El esquema SQL contiene una dimensión de tiempo (`dim_tiempo`), una dimensión descriptiva de sensores (`dim_sensor`) y una tabla de hechos (`hecho_calidad_aire`). La tabla de hechos concentra las mediciones de contaminantes, sensores y condiciones ambientales, relacionadas con la dimensión de tiempo mediante `tiempo_id`.

## Archivos de esta etapa

- `src/etl_air_quality.py`: proceso ETL reproducible.
- `data/processed/air_quality_etl.csv`: salida derivada; no reemplaza el original.
- `sql/data_mart_schema.sql`: esquema inicial del Data Mart.
- `src/load_datamart.py`: carga las tablas del Data Mart.
- `data/processed/air_quality_datamart.sqlite`: base SQLite generada con las tablas cargadas.

La carga verificada contiene 9,357 filas en `dim_tiempo`, 5 sensores en `dim_sensor` y 9,357 mediciones relacionadas en `hecho_calidad_aire`, sin mediciones huérfanas.

Esta etapa no entrena modelos y no modifica `data/raw/`.

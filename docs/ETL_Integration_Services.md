# ETL con SQL Server Integration Services

Se creó el proyecto `ssis/AirQuality_SSIS` con un paquete `Package.dtsx`. El paquete se conecta a `localhost`, base `AirQualityDW`, y muestra cuatro etapas encadenadas:

1. `01 Extracción CSV a Staging` carga el archivo original en `stg_air_quality`.
2. `02 Transformar y cargar dim_tiempo` normaliza fecha/hora y llena la dimensión de tiempo.
3. `03 Transformar y cargar hecho_calidad_aire` convierte faltantes, calcula `banda_co` y llena la tabla de hechos.
4. `Validar carga del Data Mart` comprueba que no existan duplicados.

Las tres primeras tareas llaman procedimientos SQL separados para que el flujo sea visible y explicable. `dim_sensor` conserva los cinco sensores documentados.

La ejecución validada cargó **9,357 registros**. Al repetirla se obtuvieron nuevamente **9,357** en la dimensión de tiempo y la tabla de hechos, sin duplicados.

El SQL está en `sql/sqlserver_datamart_schema.sql` y `sql/etl_sqlserver_full_load.sql`.

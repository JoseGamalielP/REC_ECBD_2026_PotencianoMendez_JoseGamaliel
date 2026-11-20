# ETL con SQL Server Integration Services

Se creó el proyecto `ssis/AirQuality_SSIS` con un paquete `Package.dtsx`. El paquete contiene la tarea **ETL AirQuality - Carga Full**, que se conecta a `localhost`, base `AirQualityDW`, y ejecuta `dbo.usp_cargar_air_quality_full`.

El procedimiento realiza la carga completa reproducible: vacía hechos y tiempo, carga el CSV original a staging, convierte `-200` en nulos, transforma fecha/hora, calcula `banda_co` y carga `dim_tiempo` y `hecho_calidad_aire`. `dim_sensor` conserva los cinco sensores documentados.

La ejecución validada cargó **9,357 registros**. Al repetirla se obtuvieron nuevamente **9,357** en la dimensión de tiempo y la tabla de hechos, sin duplicados.

El SQL está en `sql/sqlserver_datamart_schema.sql` y `sql/etl_sqlserver_full_load.sql`.

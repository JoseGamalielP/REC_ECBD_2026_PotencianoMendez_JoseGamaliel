/* Esquema SQL Server para el modelo estrella de Air Quality.
   La base se crea separada del Data Mart SQLite existente. */
IF DB_ID(N'AirQualityDW') IS NULL
BEGIN
    CREATE DATABASE AirQualityDW;
END;
GO

USE AirQualityDW;
GO

IF OBJECT_ID(N'dbo.hecho_calidad_aire', N'U') IS NOT NULL DROP TABLE dbo.hecho_calidad_aire;
IF OBJECT_ID(N'dbo.dim_sensor', N'U') IS NOT NULL DROP TABLE dbo.dim_sensor;
IF OBJECT_ID(N'dbo.dim_tiempo', N'U') IS NOT NULL DROP TABLE dbo.dim_tiempo;
GO

CREATE TABLE dbo.dim_tiempo (
    tiempo_id INT NOT NULL PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TINYINT NOT NULL,
    mes TINYINT NULL,
    anio SMALLINT NULL
);
GO

CREATE TABLE dbo.dim_sensor (
    sensor_id INT NOT NULL PRIMARY KEY,
    nombre_sensor NVARCHAR(50) NOT NULL,
    contaminante_nominal NVARCHAR(20) NULL
);
GO

CREATE TABLE dbo.hecho_calidad_aire (
    medicion_id INT NOT NULL PRIMARY KEY,
    tiempo_id INT NOT NULL,
    co_gt FLOAT NULL,
    nmhc_gt FLOAT NULL,
    c6h6_gt FLOAT NULL,
    nox_gt FLOAT NULL,
    no2_gt FLOAT NULL,
    pt08_s1_co FLOAT NULL,
    pt08_s2_nmhc FLOAT NULL,
    pt08_s3_nox FLOAT NULL,
    pt08_s4_no2 FLOAT NULL,
    pt08_s5_o3 FLOAT NULL,
    temperatura FLOAT NULL,
    humedad_relativa FLOAT NULL,
    humedad_absoluta FLOAT NULL,
    banda_co NVARCHAR(10) NULL,
    CONSTRAINT FK_hecho_tiempo FOREIGN KEY (tiempo_id)
        REFERENCES dbo.dim_tiempo(tiempo_id)
);
GO

CREATE INDEX IX_hecho_tiempo_id ON dbo.hecho_calidad_aire(tiempo_id);
GO

INSERT INTO dbo.dim_sensor (sensor_id, nombre_sensor, contaminante_nominal)
VALUES
    (1, N'PT08.S1(CO)', N'CO'),
    (2, N'PT08.S2(NMHC)', N'NMHC'),
    (3, N'PT08.S3(NOx)', N'NOx'),
    (4, N'PT08.S4(NO2)', N'NO2'),
    (5, N'PT08.S5(O3)', N'O3');
GO

SELECT DB_NAME() AS base_creada,
       (SELECT COUNT(*) FROM dbo.dim_sensor) AS sensores_cargados;
GO

/* Vista ligera para Power BI: reúne tiempo y hechos sin cargar todo el
   modelo estrella cuando el tablero solo necesita estas columnas. */
CREATE OR ALTER VIEW dbo.vw_powerbi_calidad_aire
AS
SELECT
    h.medicion_id,
    h.tiempo_id,
    t.fecha,
    t.anio,
    t.mes,
    t.hora,
    h.co_gt,
    h.nmhc_gt,
    h.c6h6_gt,
    h.nox_gt,
    h.no2_gt,
    h.pt08_s1_co,
    h.pt08_s2_nmhc,
    h.pt08_s3_nox,
    h.pt08_s4_no2,
    h.pt08_s5_o3,
    h.temperatura,
    h.humedad_relativa,
    h.humedad_absoluta,
    h.banda_co
FROM dbo.hecho_calidad_aire AS h
INNER JOIN dbo.dim_tiempo AS t
    ON t.tiempo_id = h.tiempo_id;
GO

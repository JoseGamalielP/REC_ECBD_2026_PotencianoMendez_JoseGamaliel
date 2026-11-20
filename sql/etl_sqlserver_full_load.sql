/* ETL de carga completa para AirQualityDW.
   El paquete SSIS ejecutará dbo.usp_cargar_air_quality_full. */
USE AirQualityDW;
GO

IF OBJECT_ID(N'dbo.stg_air_quality', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.stg_air_quality (
        fecha_txt NVARCHAR(30) NULL,
        hora_txt NVARCHAR(30) NULL,
        co_txt NVARCHAR(30) NULL,
        pt08_s1_co_txt NVARCHAR(30) NULL,
        nmhc_txt NVARCHAR(30) NULL,
        c6h6_txt NVARCHAR(30) NULL,
        pt08_s2_nmhc_txt NVARCHAR(30) NULL,
        nox_txt NVARCHAR(30) NULL,
        pt08_s3_nox_txt NVARCHAR(30) NULL,
        no2_txt NVARCHAR(30) NULL,
        pt08_s4_no2_txt NVARCHAR(30) NULL,
        pt08_s5_o3_txt NVARCHAR(30) NULL,
        temperatura_txt NVARCHAR(30) NULL,
        humedad_relativa_txt NVARCHAR(30) NULL,
        humedad_absoluta_txt NVARCHAR(30) NULL,
        extra_1 NVARCHAR(30) NULL,
        extra_2 NVARCHAR(30) NULL
    );
END;
GO

CREATE OR ALTER PROCEDURE dbo.usp_cargar_air_quality_full
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    BEGIN TRANSACTION;
    BEGIN TRY
        DELETE FROM dbo.hecho_calidad_aire;
        DELETE FROM dbo.dim_tiempo;
        TRUNCATE TABLE dbo.stg_air_quality;

        BULK INSERT dbo.stg_air_quality
        FROM 'C:\REC_ECBD_2026_PotencianoMendex_JoseGamaliel\data\raw\air+quality\AirQualityUCI.csv'
        WITH (
            FIRSTROW = 2,
            FIELDTERMINATOR = ';',
            ROWTERMINATOR = '0x0a',
            CODEPAGE = '65001',
            TABLOCK
        );

        ;WITH normalizado AS (
            SELECT
                TRY_CONVERT(date, fecha_txt, 103) AS fecha,
                TRY_CONVERT(tinyint, LEFT(hora_txt, 2)) AS hora,
                TRY_CONVERT(float, REPLACE(NULLIF(co_txt, '-200'), ',', '.')) AS co_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s1_co_txt, '-200'), ',', '.')) AS pt08_s1_co,
                TRY_CONVERT(float, REPLACE(NULLIF(nmhc_txt, '-200'), ',', '.')) AS nmhc_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(c6h6_txt, '-200'), ',', '.')) AS c6h6_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s2_nmhc_txt, '-200'), ',', '.')) AS pt08_s2_nmhc,
                TRY_CONVERT(float, REPLACE(NULLIF(nox_txt, '-200'), ',', '.')) AS nox_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s3_nox_txt, '-200'), ',', '.')) AS pt08_s3_nox,
                TRY_CONVERT(float, REPLACE(NULLIF(no2_txt, '-200'), ',', '.')) AS no2_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s4_no2_txt, '-200'), ',', '.')) AS pt08_s4_no2,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s5_o3_txt, '-200'), ',', '.')) AS pt08_s5_o3,
                TRY_CONVERT(float, REPLACE(NULLIF(temperatura_txt, '-200'), ',', '.')) AS temperatura,
                TRY_CONVERT(float, REPLACE(NULLIF(humedad_relativa_txt, '-200'), ',', '.')) AS humedad_relativa,
                TRY_CONVERT(float, REPLACE(NULLIF(humedad_absoluta_txt, '-200'), ',', '.')) AS humedad_absoluta
            FROM dbo.stg_air_quality
        ), fechas AS (
            SELECT *, DATEADD(HOUR, hora, CAST(fecha AS datetime2)) AS fecha_hora
            FROM normalizado
            WHERE fecha IS NOT NULL AND hora IS NOT NULL
        )
        INSERT INTO dbo.dim_tiempo (tiempo_id, fecha, hora, mes, anio)
        SELECT ROW_NUMBER() OVER (ORDER BY fecha_hora), fecha, hora, MONTH(fecha), YEAR(fecha)
        FROM fechas;

        ;WITH normalizado AS (
            SELECT
                TRY_CONVERT(date, fecha_txt, 103) AS fecha,
                TRY_CONVERT(tinyint, LEFT(hora_txt, 2)) AS hora,
                TRY_CONVERT(float, REPLACE(NULLIF(co_txt, '-200'), ',', '.')) AS co_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s1_co_txt, '-200'), ',', '.')) AS pt08_s1_co,
                TRY_CONVERT(float, REPLACE(NULLIF(nmhc_txt, '-200'), ',', '.')) AS nmhc_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(c6h6_txt, '-200'), ',', '.')) AS c6h6_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s2_nmhc_txt, '-200'), ',', '.')) AS pt08_s2_nmhc,
                TRY_CONVERT(float, REPLACE(NULLIF(nox_txt, '-200'), ',', '.')) AS nox_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s3_nox_txt, '-200'), ',', '.')) AS pt08_s3_nox,
                TRY_CONVERT(float, REPLACE(NULLIF(no2_txt, '-200'), ',', '.')) AS no2_gt,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s4_no2_txt, '-200'), ',', '.')) AS pt08_s4_no2,
                TRY_CONVERT(float, REPLACE(NULLIF(pt08_s5_o3_txt, '-200'), ',', '.')) AS pt08_s5_o3,
                TRY_CONVERT(float, REPLACE(NULLIF(temperatura_txt, '-200'), ',', '.')) AS temperatura,
                TRY_CONVERT(float, REPLACE(NULLIF(humedad_relativa_txt, '-200'), ',', '.')) AS humedad_relativa,
                TRY_CONVERT(float, REPLACE(NULLIF(humedad_absoluta_txt, '-200'), ',', '.')) AS humedad_absoluta
            FROM dbo.stg_air_quality
        ), fechas AS (
            SELECT *, DATEADD(HOUR, hora, CAST(fecha AS datetime2)) AS fecha_hora
            FROM normalizado
            WHERE fecha IS NOT NULL AND hora IS NOT NULL
        ), numeradas AS (
            SELECT f.*, ROW_NUMBER() OVER (ORDER BY fecha_hora) AS medicion_id,
                   ROW_NUMBER() OVER (ORDER BY fecha_hora) AS tiempo_id
            FROM fechas f
        )
        INSERT INTO dbo.hecho_calidad_aire (
            medicion_id, tiempo_id, co_gt, nmhc_gt, c6h6_gt, nox_gt, no2_gt,
            pt08_s1_co, pt08_s2_nmhc, pt08_s3_nox, pt08_s4_no2, pt08_s5_o3,
            temperatura, humedad_relativa, humedad_absoluta, banda_co
        )
        SELECT medicion_id, tiempo_id, co_gt, nmhc_gt, c6h6_gt, nox_gt, no2_gt,
               pt08_s1_co, pt08_s2_nmhc, pt08_s3_nox, pt08_s4_no2, pt08_s5_o3,
               temperatura, humedad_relativa, humedad_absoluta,
               CASE WHEN co_gt IS NULL THEN NULL
                    WHEN co_gt < 1 THEN N'Baja'
                    WHEN co_gt < 3 THEN N'Media'
                    ELSE N'Alta' END
        FROM numeradas;

        COMMIT TRANSACTION;
        SELECT COUNT(*) AS registros_cargados FROM dbo.hecho_calidad_aire;
    END TRY
    BEGIN CATCH
        IF XACT_STATE() <> 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
GO

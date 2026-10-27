# Unidad II Preparación de datos

**Materia:** Extracción de Conocimiento en Bases de Datos, Recursamiento 2026  
**Proyecto:** Análisis y predicción de calidad del aire  
**Fecha de avance:** 27 de octubre de 2026

## 1. Diccionario y exploración

Se revisó el CSV original de UCI en modo lectura. El archivo tiene 9,471 filas físicas y 15 variables; 9,357 filas contienen registros de medición y las filas restantes corresponden a separadores o espacios sin datos.

Las variables son Date, Time, CO(GT), PT08.S1(CO), NMHC(GT), C6H6(GT), PT08.S2(NMHC), NOx(GT), PT08.S3(NOx), NO2(GT), PT08.S4(NO2), PT08.S5(O3), T, RH y AH. Date y Time identifican el momento; las variables GT son mediciones de referencia; PT08 son respuestas instrumentales; T, RH y AH describen el ambiente.

## 2. Calidad y limpieza inicial

La documentación de UCI identifica `-200` como marcador de dato faltante. En la copia de trabajo se convirtió ese marcador a valor vacío (`NaN`) para evitar tratarlo como una medición real. El archivo de `data/raw` no se modificó.

| Variable | Faltantes detectados |
|---|---:|
| CO(GT) | 1,797 |
| NOx(GT) | 1,753 |
| NO2(GT) | 1,756 |
| NMHC(GT) | 8,557 |
| PT08.S1(CO), C6H6(GT), PT08.S2(NMHC), PT08.S3(NOx), PT08.S4(NO2), PT08.S5(O3), T, RH, AH | 480 cada una |
| Date y Time | 114 cada una |

Para los modelos supervisados se conservaron únicamente filas completas en las variables usadas. No se imputó el objetivo CO(GT).

## 3. ETL realizado

1. **Extracción:** lectura del CSV original separado por punto y coma y con coma decimal.
2. **Transformación:** conversión de `-200` a faltante, creación de fecha-hora, orden temporal y selección de variables de trabajo.
3. **Carga:** escritura de una copia derivada en `data/processed/air_quality_prepared.csv`.

El flujo se puede repetir con `src/avance_real_proyecto.py`. La copia derivada se utiliza para análisis; el Excel, CSV y ZIP originales permanecen en `data/raw`.

## 4. Propuesta de Data Mart

Se propone un Data Mart local con una tabla de hechos horarios y dimensiones de tiempo y sensor. La tabla de hechos conservará las mediciones de referencia y las respuestas instrumentales; permitirá consultas por fecha, hora y contaminante sin alterar el dataset original.

## 5. Unidad III preparada hasta el 30 de octubre

Ya se ejecutaron regresión y clasificación sobre la copia procesada. La regresión lineal obtuvo MAE 0.344, RMSE 0.484 y R² 0.862 en el periodo de evaluación. La clasificación por bandas baja, media y alta obtuvo accuracy 0.865 y macro-F1 0.849. Estos resultados y sus gráficas están en `docs/Avance_Real_Proyecto.md`.

La clasificación utiliza estas bandas académicas: baja si CO < 1 mg/m³, media si 1 ≤ CO < 3 mg/m³ y alta si CO ≥ 3 mg/m³. Las bandas no son una norma sanitaria.

## Estado al 30 de octubre

Quedan documentados el diccionario, la exploración, la limpieza inicial, el ETL, los datos procesados, la propuesta de Data Mart y los modelos supervisados con métricas. No se incluyen clustering ni PCA porque corresponden a una etapa posterior del calendario.

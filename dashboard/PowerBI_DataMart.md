# Conexión del Data Mart con Power BI

Power BI Desktop está instalado en el equipo. La conexión preparada utiliza los tres CSV exportados desde el Data Mart, porque permite abrir el avance sin instalar un controlador adicional para SQLite.

## Archivos para cargar

En Power BI Desktop se usa **Obtener datos > Texto/CSV** para cargar:

- `data/processed/powerbi/dim_tiempo.csv`
- `data/processed/powerbi/dim_sensor.csv`
- `data/processed/powerbi/hecho_calidad_aire.csv`

## Relaciones

En la vista Modelo se debe relacionar:

- `dim_tiempo[tiempo_id]` (uno) con `hecho_calidad_aire[tiempo_id]` (muchos).

La dimensión de sensores documenta las cinco respuestas PT08. La tabla de hechos contiene las mediciones, contaminantes, condiciones ambientales y `banda_co`.

## Visualizaciones iniciales

- Tarjetas: número de mediciones, promedio de CO y promedio de NO2.
- Línea: promedio de CO por fecha.
- Columnas: cantidad de mediciones por `banda_co`.
- Dispersión: `pt08_s1_co` frente a `co_gt`.
- Segmentadores: año, mes y banda de CO.

El dashboard debe interpretar las bandas como etiquetas académicas del proyecto, no como límites sanitarios oficiales.

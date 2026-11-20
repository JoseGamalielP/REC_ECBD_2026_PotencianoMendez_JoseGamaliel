# Conexión del Data Mart con Power BI

Power BI Desktop está instalado en el equipo. La conexión recomendada para la versión final utiliza SQL Server y la vista `dbo.vw_powerbi_calidad_aire` de la base `AirQualityDW`. La vista reúne las mediciones con la dimensión de tiempo y evita cargar todo el modelo estrella.

## Conexión recomendada

En Power BI Desktop seleccionar **Obtener datos > SQL Server**, indicar el servidor local usado por SQL Server y la base `AirQualityDW`. En el navegador seleccionar:

- `dbo.vw_powerbi_calidad_aire` para el dashboard;
- opcionalmente `dbo.dim_sensor` si se requiere mostrar el catálogo de sensores.

La vista fue validada con 9,357 filas y se alimenta de `hecho_calidad_aire` y `dim_tiempo`.

## Archivos de respaldo

Si se necesita abrir el avance sin conexión a SQL Server, se pueden usar los CSV exportados:

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

## Plantilla visual

Se incluye `dashboard/plantilla_dashboard_calidad_aire_v10.png` como fondo limpio de plantilla: conserva el diseño, resalta los títulos de filtros con una franja azul y deja `Banda de CO` en un recuadro vertical alto para cuatro opciones. Las versiones anteriores quedan como alternativas. En Power BI se puede usar desde **Formato de página > Fondo de lienzo**, ajustar la transparencia a 0% y colocar los visuales encima de cada sección.

El dashboard debe interpretar las bandas como etiquetas académicas del proyecto, no como límites sanitarios oficiales.

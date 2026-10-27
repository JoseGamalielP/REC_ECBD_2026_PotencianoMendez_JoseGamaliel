# Avance real del proyecto: Air Quality

**Materia:** Extracción de Conocimiento en Bases de Datos (ECBD), Recursamiento 2026  
**Proyecto:** Análisis y predicción de calidad del aire  
**Fecha:** 27 de octubre de 2026

## 1. Preparación de datos

Se leyó el CSV original en modo lectura. El original no se modificó. Para el análisis se creó una copia derivada en `data/processed/air_quality_prepared.csv`; los valores `-200` se trataron como faltantes únicamente en esa copia.

- Filas completas para modelos: **7344**.
- Entrenamiento temporal: **5875** registros.
- Evaluación temporal: **1469** registros.

## 2. Regresión de CO(GT)

Se estimó `CO(GT)` usando las cinco respuestas PT08 y las variables T, RH y AH.

| Modelo | MAE | RMSE | R² |
|---|---:|---:|---:|
| Regresión lineal | 0.344 | 0.484 | 0.862 |
| Bosque aleatorio | 0.370 | 0.540 | 0.827 |

La gráfica `docs/figuras_avance/regresion_co.png` compara los valores reales y estimados en el periodo de evaluación.

## 3. Clasificación de CO

Se creó `banda_CO`: Baja (<1), Media (1 a <3) y Alta (≥3 mg/m³).

| Banda | Registros |
|---|---:|
| Baja | 1556 |
| Media | 4289 |
| Alta | 1829 |
| Sin etiqueta | 1797 |

La clasificación logística obtuvo **accuracy 0.865** y **macro-F1 0.849** sobre el periodo de evaluación. Matriz de confusión (filas reales, columnas predichas; orden Baja, Media, Alta):

```text
[[241  91   0]
 [ 40 796  23]
 [  0  45 233]]
```

## 4. Clustering y PCA

Se formaron 3 grupos con las variables sensor/ambiente. El coeficiente de silueta fue **0.265**. PCA resumió la variación en dos componentes con varianza explicada total de **0.775**.

## 5. Conclusión preliminar

Las variables de sensores y ambiente contienen información útil para estimar CO(GT). Las bandas tienen tamaños diferentes, por lo que la clasificación debe interpretarse con cuidado. El clustering y PCA permiten explorar patrones, pero no representan categorías sanitarias. Este avance es preliminar y debe complementarse con revisión de calidad, comparación de periodos y explicación de limitaciones.

## Archivos generados

- `data/processed/air_quality_prepared.csv`
- `docs/figuras_avance/regresion_co.png`
- `docs/figuras_avance/bandas_co.png`
- `docs/figuras_avance/clustering_pca.png`
- `src/avance_real_proyecto.py`

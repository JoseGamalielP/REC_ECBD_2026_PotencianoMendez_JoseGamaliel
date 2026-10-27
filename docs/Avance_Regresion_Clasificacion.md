# Avance de regresión y clasificación

**Proyecto:** Análisis y predicción de calidad del aire  
**Materia:** Extracción de Conocimiento en Bases de Datos (ECBD), Recursamiento 2026  
**Fecha:** 27 de octubre de 2026

## 1. Regresión de CO(GT)

Se utilizó `CO(GT)` como valor que se desea estimar. Las entradas fueron las cinco respuestas `PT08.*`, `T`, `RH` y `AH`. El archivo original se leyó sin modificarlo. Para este avance se quitaron únicamente de la copia en memoria los registros sin valor completo en las variables usadas.

- Registros completos usados: **7344**.
- Entrenamiento temporal (80%): **5875** registros.
- Evaluación temporal (20%): **1469** registros.
- Periodo de entrenamiento: **2004-03-10 18:00 a 2005-01-28 11:00**.
- Periodo de evaluación: **2005-01-28 12:00 a 2005-04-04 14:00**.

### Resultado preliminar

| Comparación | MAE | RMSE | R² |
|---|---:|---:|---:|
| Referencia constante | 1.068 | 1.320 | — |
| Regresión lineal | 0.344 | 0.484 | 0.862 |

La regresión lineal se calculó con operaciones numéricas reproducibles. La comparación indica si las entradas aportan una mejora frente a usar solamente el promedio del entrenamiento. Este resultado es preliminar y no sustituye una validación con `scikit-learn` cuando se habilite esa biblioteca.

## 2. Clasificación por bandas de CO

Se creó en memoria la variable `banda_CO` con los límites académicos definidos en la planeación: Baja si CO < 1 mg/m³, Media si 1 ≤ CO < 3 mg/m³ y Alta si CO ≥ 3 mg/m³. Los valores faltantes no reciben categoría.

| Banda | Regla | Registros |
|---|---|---:|
| Baja | CO(GT) < 1 | 1556 |
| Media | 1 ≤ CO(GT) < 3 | 4289 |
| Alta | CO(GT) ≥ 3 | 1829 |

La siguiente tarea es revisar si las tres bandas tienen suficientes registros y, con `scikit-learn` disponible, entrenar y evaluar un clasificador. No se modificó ni se sobrescribió el dataset original.

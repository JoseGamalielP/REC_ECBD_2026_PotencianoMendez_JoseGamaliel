"""Avance reproducible de regresion y clasificacion para Air Quality.
No modifica el archivo original; lee el CSV y genera solo un reporte.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / 'data/raw/air+quality/AirQualityUCI.csv'
OUT = ROOT / 'docs/Avance_Regresion_Clasificacion.md'

df = pd.read_csv(CSV, sep=';', decimal=',', na_values=['-200', '-200.0'], encoding='latin1')
df = df.iloc[:, :15].copy()
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'].str.replace('.', ':', regex=False), dayfirst=True, errors='coerce')
df = df.sort_values('DateTime').reset_index(drop=True)
features = ['PT08.S1(CO)', 'PT08.S2(NMHC)', 'PT08.S3(NOx)', 'PT08.S4(NO2)', 'PT08.S5(O3)', 'T', 'RH', 'AH']
target = 'CO(GT)'
work = df[features + [target, 'DateTime']].dropna().reset_index(drop=True)
n = len(work)
cut = int(n * .8)
train, test = work.iloc[:cut], work.iloc[cut:]
Xtr = np.c_[np.ones(len(train)), train[features].to_numpy(float)]
Xte = np.c_[np.ones(len(test)), test[features].to_numpy(float)]
ytr, yte = train[target].to_numpy(float), test[target].to_numpy(float)
coef = np.linalg.lstsq(Xtr, ytr, rcond=None)[0]
pred = Xte @ coef
baseline = np.full_like(yte, ytr.mean())
mae = lambda y, p: float(np.mean(np.abs(y-p)))
rmse = lambda y, p: float(np.sqrt(np.mean((y-p)**2)))
r2 = float(1 - np.sum((yte-pred)**2) / np.sum((yte-yte.mean())**2))
bands = pd.cut(df[target], bins=[-np.inf, 1, 3, np.inf], labels=['Baja', 'Media', 'Alta'], right=False)
counts = bands.value_counts(sort=False, dropna=False)
lines = [
    '# Avance de regresión y clasificación', '',
    '**Proyecto:** Análisis y predicción de calidad del aire  ',
    '**Materia:** Extracción de Conocimiento en Bases de Datos (ECBD), Recursamiento 2026  ',
    '**Fecha:** 27 de octubre de 2026', '',
    '## 1. Regresión de CO(GT)', '',
    'Se utilizó `CO(GT)` como valor que se desea estimar. Las entradas fueron las cinco respuestas `PT08.*`, `T`, `RH` y `AH`. El archivo original se leyó sin modificarlo. Para este avance se quitaron únicamente de la copia en memoria los registros sin valor completo en las variables usadas.', '',
    f'- Registros completos usados: **{n}**.',
    f'- Entrenamiento temporal (80%): **{len(train)}** registros.',
    f'- Evaluación temporal (20%): **{len(test)}** registros.',
    f'- Periodo de entrenamiento: **{train.DateTime.min():%Y-%m-%d %H:%M} a {train.DateTime.max():%Y-%m-%d %H:%M}**.',
    f'- Periodo de evaluación: **{test.DateTime.min():%Y-%m-%d %H:%M} a {test.DateTime.max():%Y-%m-%d %H:%M}**.', '',
    '### Resultado preliminar', '',
    '| Comparación | MAE | RMSE | R² |', '|---|---:|---:|---:|',
    f'| Referencia constante | {mae(yte, baseline):.3f} | {rmse(yte, baseline):.3f} | — |',
    f'| Regresión lineal | {mae(yte, pred):.3f} | {rmse(yte, pred):.3f} | {r2:.3f} |', '',
    'La regresión lineal se calculó con operaciones numéricas reproducibles. La comparación indica si las entradas aportan una mejora frente a usar solamente el promedio del entrenamiento. Este resultado es preliminar y no sustituye una validación con `scikit-learn` cuando se habilite esa biblioteca.', '',
    '## 2. Clasificación por bandas de CO', '',
    'Se creó en memoria la variable `banda_CO` con los límites académicos definidos en la planeación: Baja si CO < 1 mg/m³, Media si 1 ≤ CO < 3 mg/m³ y Alta si CO ≥ 3 mg/m³. Los valores faltantes no reciben categoría.', '',
    '| Banda | Regla | Registros |', '|---|---|---:|',
    f'| Baja | CO(GT) < 1 | {int(counts.get("Baja", 0))} |',
    f'| Media | 1 ≤ CO(GT) < 3 | {int(counts.get("Media", 0))} |',
    f'| Alta | CO(GT) ≥ 3 | {int(counts.get("Alta", 0))} |', '',
    'La siguiente tarea es revisar si las tres bandas tienen suficientes registros y, con `scikit-learn` disponible, entrenar y evaluar un clasificador. No se modificó ni se sobrescribió el dataset original.',
]
OUT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(OUT)
print(f'complete={n} train={len(train)} test={len(test)} mae={mae(yte,pred):.3f} rmse={rmse(yte,pred):.3f} r2={r2:.3f}')
print(counts.to_string())

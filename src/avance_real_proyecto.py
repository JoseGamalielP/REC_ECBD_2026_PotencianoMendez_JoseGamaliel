"""Avance real reproducible del proyecto Air Quality.
Genera derivados sin modificar data/raw.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, f1_score, confusion_matrix, silhouette_score

ROOT=Path(__file__).resolve().parents[1]; raw=ROOT/'data/raw/air+quality/AirQualityUCI.csv'; out=ROOT/'data/processed'; docs=ROOT/'docs'; fig=docs/'figuras_avance'; out.mkdir(exist_ok=True); fig.mkdir(exist_ok=True)
df=pd.read_csv(raw,sep=';',decimal=',',na_values=['-200','-200.0'],encoding='latin1').iloc[:,:15]
df['DateTime']=pd.to_datetime(df['Date']+' '+df['Time'].str.replace('.',':',regex=False),dayfirst=True,errors='coerce')
df=df.sort_values('DateTime').reset_index(drop=True)
features=['PT08.S1(CO)','PT08.S2(NMHC)','PT08.S3(NOx)','PT08.S4(NO2)','PT08.S5(O3)','T','RH','AH']; target='CO(GT)'
modeldf=df[features+[target,'DateTime']].dropna().reset_index(drop=True)
split=int(len(modeldf)*.8); tr=modeldf.iloc[:split]; te=modeldf.iloc[split:]
Xtr,Xte=tr[features],te[features]; ytr,yte=tr[target],te[target]
models={'Regresión lineal':make_pipeline(SimpleImputer(),StandardScaler(),LinearRegression()),'Bosque aleatorio':make_pipeline(SimpleImputer(),RandomForestRegressor(n_estimators=100,random_state=42,n_jobs=1))}
preds={}; scores=[]
for name,m in models.items():
    m.fit(Xtr,ytr); p=m.predict(Xte); preds[name]=p; scores.append((name,mean_absolute_error(yte,p),mean_squared_error(yte,p)**.5,r2_score(yte,p)))
bands=pd.cut(df[target],[-np.inf,1,3,np.inf],labels=['Baja','Media','Alta'],right=False); df['banda_CO']=bands
valid=df.dropna(subset=features+[target]).copy(); vtr=valid.iloc[:int(len(valid)*.8)]; vte=valid.iloc[int(len(valid)*.8):]
clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)); clf.fit(vtr[features],vtr['banda_CO']); cp=clf.predict(vte[features]); acc=accuracy_score(vte['banda_CO'],cp); f1=f1_score(vte['banda_CO'],cp,average='macro'); cm=confusion_matrix(vte['banda_CO'],cp,labels=['Baja','Media','Alta'])
cluster=valid[features].copy(); cluster=StandardScaler().fit_transform(cluster); km=KMeans(n_clusters=3,random_state=42,n_init=10); labels=km.fit_predict(cluster); sil=silhouette_score(cluster,labels); pca=PCA(n_components=2,random_state=42); pc=pca.fit_transform(cluster)
df.to_csv(out/'air_quality_prepared.csv',index=False,encoding='utf-8-sig')
plt.figure(figsize=(9,4)); plt.plot(te['DateTime'],yte,label='Real',lw=1); plt.plot(te['DateTime'],preds['Regresión lineal'],label='Estimado',lw=1); plt.legend(); plt.title('CO(GT): valores reales y estimados'); plt.tight_layout(); plt.savefig(fig/'regresion_co.png',dpi=150); plt.close()
plt.figure(figsize=(6,4)); df['banda_CO'].value_counts(sort=False).plot.bar(color=['#7db7e8','#f2c14e','#e76f51']); plt.title('Registros por banda de CO'); plt.ylabel('Registros'); plt.tight_layout(); plt.savefig(fig/'bandas_co.png',dpi=150); plt.close()
plt.figure(figsize=(6,4)); plt.scatter(pc[:,0],pc[:,1],c=labels,s=4,cmap='viridis'); plt.xlabel('PC1'); plt.ylabel('PC2'); plt.title('Clustering y PCA'); plt.tight_layout(); plt.savefig(fig/'clustering_pca.png',dpi=150); plt.close()
lines=['# Avance real del proyecto: Air Quality','', '**Materia:** Extracción de Conocimiento en Bases de Datos (ECBD), Recursamiento 2026  ','**Proyecto:** Análisis y predicción de calidad del aire  ','**Fecha:** 27 de octubre de 2026','', '## 1. Preparación de datos','',f'Se leyó el CSV original en modo lectura. El original no se modificó. Para el análisis se creó una copia derivada en `data/processed/air_quality_prepared.csv`; los valores `-200` se trataron como faltantes únicamente en esa copia.', '',f'- Filas completas para modelos: **{len(valid)}**.',f'- Entrenamiento temporal: **{len(vtr)}** registros.',f'- Evaluación temporal: **{len(vte)}** registros.', '', '## 2. Regresión de CO(GT)','', 'Se estimó `CO(GT)` usando las cinco respuestas PT08 y las variables T, RH y AH.', '', '| Modelo | MAE | RMSE | R² |','|---|---:|---:|---:|']
for n,a,b,c in scores: lines.append(f'| {n} | {a:.3f} | {b:.3f} | {c:.3f} |')
lines += ['', 'La gráfica `docs/figuras_avance/regresion_co.png` compara los valores reales y estimados en el periodo de evaluación.', '', '## 3. Clasificación de CO','', 'Se creó `banda_CO`: Baja (<1), Media (1 a <3) y Alta (≥3 mg/m³).','', '| Banda | Registros |','|---|---:|']
for b,c in df['banda_CO'].value_counts(sort=False,dropna=False).items(): lines.append(f'| {b if pd.notna(b) else "Sin etiqueta"} | {c} |')
lines += ['',f'La clasificación logística obtuvo **accuracy {acc:.3f}** y **macro-F1 {f1:.3f}** sobre el periodo de evaluación. Matriz de confusión (filas reales, columnas predichas; orden Baja, Media, Alta):', '', '```text', str(cm), '```', '', '## 4. Clustering y PCA','',f'Se formaron 3 grupos con las variables sensor/ambiente. El coeficiente de silueta fue **{sil:.3f}**. PCA resumió la variación en dos componentes con varianza explicada total de **{pca.explained_variance_ratio_.sum():.3f}**.', '', '## 5. Conclusión preliminar','', 'Las variables de sensores y ambiente contienen información útil para estimar CO(GT). Las bandas tienen tamaños diferentes, por lo que la clasificación debe interpretarse con cuidado. El clustering y PCA permiten explorar patrones, pero no representan categorías sanitarias. Este avance es preliminar y debe complementarse con revisión de calidad, comparación de periodos y explicación de limitaciones.', '', '## Archivos generados','', '- `data/processed/air_quality_prepared.csv`', '- `docs/figuras_avance/regresion_co.png`', '- `docs/figuras_avance/bandas_co.png`', '- `docs/figuras_avance/clustering_pca.png`', '- `src/avance_real_proyecto.py`']
(docs/'Avance_Real_Proyecto.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('OK',len(valid),scores,acc,f1,sil,pca.explained_variance_ratio_.sum())

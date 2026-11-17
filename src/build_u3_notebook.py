from pathlib import Path
import nbformat as nbf
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
path = root / 'notebooks' / 'PotencianoMendez_JoseGamaliel_U3_Modelos.ipynb'
cells = []
def md(s): cells.append(nbf.v4.new_markdown_cell(s))
def code(s): cells.append(nbf.v4.new_code_cell(s))
md('# Unidad III. Modelos supervisados y análisis exploratorio\n\n**Proyecto:** Análisis y predicción de calidad del aire\n\nEste notebook usa la copia procesada y no modifica `data/raw/`. Se ejecutan regresión lineal, clasificación logística, clustering y PCA con resultados reales.')
code("from pathlib import Path\nimport pandas as pd\nimport numpy as np\nfrom sklearn.pipeline import make_pipeline\nfrom sklearn.impute import SimpleImputer\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LinearRegression, LogisticRegression\nfrom sklearn.cluster import KMeans\nfrom sklearn.decomposition import PCA\nfrom sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, f1_score, confusion_matrix, silhouette_score\nROOT=Path.cwd().parent if Path.cwd().name=='notebooks' else Path.cwd()\ndf=pd.read_csv(ROOT/'data/processed/air_quality_etl.csv', parse_dates=['DateTime'])\nfeatures=['PT08.S1(CO)','PT08.S2(NMHC)','PT08.S3(NOx)','PT08.S4(NO2)','PT08.S5(O3)','T','RH','AH']\nvalid=df.dropna(subset=features+['CO(GT)']).sort_values('DateTime').reset_index(drop=True)\nvalid.shape")
md('Se usa una separación temporal 80/20 para evitar mezclar observaciones futuras con el entrenamiento.')
code("split=int(len(valid)*.8); tr=valid.iloc[:split]; te=valid.iloc[split:]\nreg=make_pipeline(SimpleImputer(),StandardScaler(),LinearRegression())\nreg.fit(tr[features],tr['CO(GT)']); pred=reg.predict(te[features])\nregresion={'MAE':mean_absolute_error(te['CO(GT)'],pred),'RMSE':mean_squared_error(te['CO(GT)'],pred)**.5,'R2':r2_score(te['CO(GT)'],pred)}\npd.Series(regresion).round(3)")
md('La regresión lineal estima la concentración numérica de CO. MAE y RMSE son errores; R² indica qué proporción de variación explica el modelo en el periodo de prueba.')
code("valid['banda_CO']=pd.cut(valid['CO(GT)'],[-np.inf,1,3,np.inf],labels=['Baja','Media','Alta'],right=False)\nclf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000))\nclf.fit(tr[features],tr['banda_CO']); clase=clf.predict(te[features])\nclasificacion={'accuracy':accuracy_score(te['banda_CO'],clase),'macro_f1':f1_score(te['banda_CO'],clase,average='macro')}\nprint(pd.Series(clasificacion).round(3)); print(confusion_matrix(te['banda_CO'],clase,labels=['Baja','Media','Alta']))")
md('La clasificación logística asigna una banda de CO. Accuracy es la proporción total de aciertos y macro-F1 promedia el desempeño entre las tres bandas.')
code("Z=StandardScaler().fit_transform(valid[features])\nlabels=KMeans(n_clusters=3,n_init=10,random_state=42).fit_predict(Z)\nprint('Silueta:',round(silhouette_score(Z,labels),3))\npca=PCA(n_components=2,random_state=42).fit(Z)\nprint('Varianza explicada por PCA:',round(pca.explained_variance_ratio_.sum(),3))")
md('Clustering y PCA son análisis no supervisados: buscan patrones sin utilizar una etiqueta objetivo. Los grupos son exploratorios y no equivalen a categorías sanitarias.')
nb=nbf.v4.new_notebook(); nb['metadata']['kernelspec']={'display_name':'Python 3','language':'python','name':'python3'}; nb['cells']=cells
path.write_text(nbf.writes(nb),encoding='utf-8'); NotebookClient(nb,timeout=600,kernel_name='python3',resources={'metadata':{'path':str(path.parent)}}).execute(); path.write_text(nbf.writes(nb),encoding='utf-8'); print(path)

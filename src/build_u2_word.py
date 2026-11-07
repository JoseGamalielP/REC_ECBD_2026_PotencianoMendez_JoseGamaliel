from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'docs/PotencianoMendez_JoseGamaliel_U2_AE1_Diagnostico.docx'
doc=Document(); sec=doc.sections[0]; sec.top_margin=sec.bottom_margin=Inches(.75); sec.left_margin=sec.right_margin=Inches(.8)
for name in ['Normal','Title','Heading 1','Heading 2']:
 s=doc.styles[name]; s.font.name='Arial'; s.font.color.rgb=RGBColor(0,0,0)
doc.styles['Normal'].font.size=Pt(10.5); doc.styles['Normal'].paragraph_format.space_after=Pt(6)
for n,z in [('Title',20),('Heading 1',14),('Heading 2',11.5)]: doc.styles[n].font.size=Pt(z); doc.styles[n].font.bold=True
f=sec.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.RIGHT; x=OxmlElement('w:fldSimple'); x.set(qn('w:instr'),'PAGE'); f._p.append(x)
def para(t,style=None):
 p=doc.add_paragraph(style=style)
 for i,v in enumerate(t.split('**')):
  r=p.add_run(v); r.bold=i%2==1
 return p
def table(headers, rows, widths):
 t=doc.add_table(rows=1,cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=False
 for c,w in zip(t.columns,widths): c.width=Inches(w)
 for i,rowvals in enumerate([headers]+rows):
  row=t.rows[0] if i==0 else t.add_row()
  for j,(cell,val) in enumerate(zip(row.cells,rowvals)):
   cell.text=str(val); cell.width=Inches(widths[j])
   sh=OxmlElement('w:shd'); sh.set(qn('w:fill'),'DCE6F1' if i==0 else ('F4F6F8' if i%2==0 else 'FFFFFF')); cell._tc.get_or_add_tcPr().append(sh)
   for p in cell.paragraphs:
    for r in p.runs: r.font.size=Pt(9); r.bold=i==0
 return t
def page(): doc.add_page_break()

p=doc.add_paragraph(style='Title'); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run('Actividad de Evaluación 1 – Unidad II. Exploración y diagnóstico del conjunto de datos')
for t in ['Universidad Tecnológica de Tula-Tepeji','Ingeniería en Desarrollo y Gestión de Software','Asignatura: Extracción de Conocimiento en Bases de Datos','Recursamiento 2026','Proyecto: Análisis y predicción de calidad del aire','Alumno: José Gamaliel Potenciano Méndez','Matrícula: 23301258','Grupo: 10IDGS - G1','Docente: Ing. Jose Luis Herrera Gallardo','Fecha de entrega: 9 de noviembre de 2026']:
 p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.paragraph_format.space_after=Pt(10); p.add_run(t).font.size=Pt(12)
page(); doc.add_heading('1. Identificación del dataset',level=1)
para('**Nombre del proyecto:** Análisis y predicción de calidad del aire.')
para('**Dataset:** Air Quality. **Fuente:** UCI Machine Learning Repository. **Formato:** CSV y XLSX. **Archivo original:** data/raw/air+quality/AirQualityUCI.csv y AirQualityUCI.xlsx.')
para('El conjunto contiene registros horarios de contaminantes, respuestas de instrumentos y condiciones ambientales. La lectura del CSV presenta 9,471 filas físicas y 15 variables; algunas filas finales son espacios sin medición. La ficha de UCI anuncia aproximadamente 9,358 registros y 15 características. El original se conserva sin cambios.')
doc.add_heading('2. Carga y exploración inicial',level=1)
para('El notebook ejecuta y explica `df.head()`, `df.shape`, `df.columns`, `df.info()`, `df.dtypes` y `df.describe()`. Estas instrucciones permiten comprobar las primeras filas, la dimensión, los nombres, los tipos y los resúmenes estadísticos.')
para('Date y Time se cargan como texto; las mediciones se cargan como valores numéricos. La conversión de fecha-hora y cualquier tratamiento de faltantes quedan para la siguiente etapa de preparación.')
doc.add_heading('3. Diccionario de datos',level=1)
rows=[['Date','Fecha del registro','object','Temporal','Fecha','Ordenar'],['Time','Hora del registro','object','Temporal','Hora','Ordenar'],['CO(GT)','CO de referencia','float64','Cuantitativa continua','mg/m³','Objetivo de regresión'],['PT08.S1(CO)','Respuesta sensor CO','int64','Cuantitativa continua','Señal','Entrada candidata'],['NMHC(GT)','NMHC de referencia','float64','Cuantitativa continua','µg/m³','Contexto'],['C6H6(GT)','Benceno de referencia','float64','Cuantitativa continua','µg/m³','Contexto'],['PT08.S2(NMHC)','Respuesta sensor NMHC','int64','Cuantitativa continua','Señal','Entrada candidata'],['NOx(GT)','NOx de referencia','float64','Cuantitativa continua','ppb','Contexto'],['PT08.S3(NOx)','Respuesta sensor NOx','int64','Cuantitativa continua','Señal','Entrada candidata'],['NO2(GT)','NO2 de referencia','float64','Cuantitativa continua','µg/m³','Contexto'],['PT08.S4(NO2)','Respuesta sensor NO2','int64','Cuantitativa continua','Señal','Entrada candidata'],['PT08.S5(O3)','Respuesta sensor O3','int64','Cuantitativa continua','Señal','Entrada candidata'],['T','Temperatura','float64','Cuantitativa continua','°C','Entrada ambiental'],['RH','Humedad relativa','float64','Cuantitativa continua','%','Entrada ambiental'],['AH','Humedad absoluta','float64','Cuantitativa continua','No especificada','Entrada ambiental']]
table(['Variable','Descripción','Tipo Python','Tipo','Unidad','Utilidad'],rows,[1.2,1.75,1.0,1.2,1.0,1.35]); page()
doc.add_heading('4. Tipo y fuente de los datos',level=1); para('La fuente es UCI Machine Learning Repository. Son datos estructurados, tabulares y generados principalmente por instrumentos y sensores, con mediciones de referencia y marcas de tiempo. El archivo no corresponde a transacciones, redes sociales ni datos biométricos.')
doc.add_heading('5. Diagnóstico de calidad',level=1); doc.add_heading('5.1 Valores faltantes',level=2)
table(['Variable o grupo','Faltantes'],[['CO(GT)','1,797'],['NOx(GT)','1,753'],['NO2(GT)','1,756'],['NMHC(GT)','8,557'],['PT08.S1, C6H6, PT08.S2, PT08.S3, PT08.S4, PT08.S5, T, RH, AH','480 cada una'],['Date y Time','114 cada una']],[4.8,1.7]); para('UCI documenta `-200` como marcador de faltante. No se sustituyó ni eliminó durante esta actividad. En una etapa posterior se tratará en una copia.')
doc.add_heading('5.2 Registros duplicados',level=2); para('El notebook calcula `df.duplicated().sum()` y deja visible el resultado. Los duplicados se revisarían por fecha y hora antes de decidir si corresponden a una repetición real o a un problema de captura. No se eliminaron.')
doc.add_heading('5.3 Inconsistencias y valores extremos',level=2); para('Se revisan valores negativos distintos de `-200`, fechas y horas que no puedan interpretarse, rangos y valores extremos. Los valores alejados del centro se consideran candidatos a atípicos, no errores automáticos; podrían representar episodios reales o lecturas instrumentales que deben verificarse.')
doc.add_heading('6. Análisis estadístico inicial',level=1)
table(['Variable','Media','Mediana','Mínimo','Máximo','Desv. estándar'],[['CO(GT)','2.153','1.800','0.100','11.900','1.453'],['NO2(GT)','113.091','109.000','2.000','340.000','48.370'],['T','18.318','17.800','-1.900','44.600','8.832'],['RH','49.234','49.600','9.200','88.700','17.317'],['AH','1.026','0.995','0.185','2.231','0.404']],[1.4,1.0,1.0,1.0,1.0,1.3]); para('La media y mediana permiten comparar el centro de los datos. Los rangos muestran la variación de contaminantes y ambiente; no se interpretan como límites sanitarios.')
page(); doc.add_heading('7. Detección inicial de valores atípicos',level=1); para('El notebook genera boxplots para CO(GT), NO2(GT) y T. Las observaciones alejadas del rango central se reportan como candidatas a atípicos. No se eliminan en esta actividad porque la guía solicita diagnóstico antes de limpiar.')
for name,cap in [('boxplots.png','Boxplots de variables numéricas seleccionadas'),('exploracion_inicial.png','Histogramas y relación exploratoria')]:
 p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run().add_picture(str(ROOT/'docs/figuras_u2'/name),width=Inches(6.2)); q=doc.add_paragraph(cap); q.alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_heading('8. Visualización inicial',level=1); para('Se incluyen histogramas de CO y temperatura y una gráfica de dispersión entre CO(GT) y PT08.S1(CO). Cada gráfica incluye título, ejes e interpretación en el notebook. La dispersión sirve para explorar una relación; no demuestra causalidad.')
doc.add_heading('9. Preparación para análisis posteriores',level=1)
para('**Regresión:** CO(GT) como objetivo numérico; PT08.S1(CO), PT08.S2(NMHC), PT08.S3(NOx), PT08.S4(NO2), PT08.S5(O3), T, RH y AH como entradas candidatas.\n**Clasificación:** una variable derivada de CO(GT) con bandas académicas baja, media y alta.\n**Agrupamiento:** las cinco respuestas PT08 junto con T, RH y AH para buscar patrones de comportamiento.')
doc.add_heading('10. Conclusión del diagnóstico',level=1); para('El dataset contiene mediciones horarias de contaminantes, señales instrumentales y ambiente. Es adecuado para continuar con el Proyecto Integrador, pero requiere tratamiento posterior por los faltantes `-200`, posibles duplicados, validación de fechas y horas y revisión de valores extremos. No se modificó el original. El notebook contiene el código, resultados, tablas, visualizaciones, interpretaciones y propuestas solicitadas.')
doc.add_heading('Entrega y repositorio',level=1); para('Notebook ejecutable: notebooks/PotencianoMendez_JoseGamaliel_U2_AE1_Exploracion.ipynb\nInforme editable: docs/PotencianoMendez_JoseGamaliel_U2_AE1_Diagnostico.docx\nRepositorio: https://github.com/JoseGamalielP/REC_ECBD_2026_PotencianoMendez_JoseGamaliel')
doc.core_properties.title='Actividad de Evaluación 1 Unidad II Exploración y diagnóstico'; doc.core_properties.author='José Gamaliel Potenciano Méndez'; doc.save(out); print(out)

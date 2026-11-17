"""ETL inicial de Air Quality.

Lee el archivo original sin modificarlo y genera una copia procesada para
las siguientes etapas del proyecto. No entrena modelos.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "air+quality" / "AirQualityUCI.csv"
OUT = ROOT / "data" / "processed" / "air_quality_etl.csv"


def extract() -> pd.DataFrame:
    return pd.read_csv(RAW, sep=";", decimal=",", encoding="latin1").iloc[:, :15]


def transform(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    numeric = result.select_dtypes(include="number").columns
    result[numeric] = result[numeric].replace(-200, pd.NA)
    time_text = result["Time"].astype("string").str.replace(".", ":", regex=False)
    result["DateTime"] = pd.to_datetime(
        result["Date"].astype("string") + " " + time_text,
        dayfirst=True,
        errors="coerce",
    )
    result["anio"] = result["DateTime"].dt.year.astype("Int64")
    result["mes"] = result["DateTime"].dt.month.astype("Int64")
    result["dia"] = result["DateTime"].dt.day.astype("Int64")
    result["hora"] = result["DateTime"].dt.hour.astype("Int64")
    result["banda_CO"] = pd.cut(
        pd.to_numeric(result["CO(GT)"], errors="coerce"),
        bins=[-float("inf"), 1, 3, float("inf")],
        labels=["Baja", "Media", "Alta"],
        right=False,
    )
    return result.sort_values("DateTime").reset_index(drop=True)


def load(df: pd.DataFrame) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    extracted = extract()
    transformed = transform(extracted)
    load(transformed)
    print(f"Archivo original leído: {RAW}")
    print(f"Archivo procesado generado: {OUT}")
    print(f"Registros: {len(transformed)} | Variables: {len(transformed.columns)}")
    print(f"Fechas no interpretadas: {transformed['DateTime'].isna().sum()}")

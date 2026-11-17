"""Construye el Data Mart SQLite a partir de la salida ETL."""
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ETL = ROOT / "data" / "processed" / "air_quality_etl.csv"
DB = ROOT / "data" / "processed" / "air_quality_datamart.sqlite"
PBI = ROOT / "data" / "processed" / "powerbi"


def main() -> None:
    df = pd.read_csv(ETL, parse_dates=["DateTime"])
    DB.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as con:
        con.executescript("DROP TABLE IF EXISTS hecho_calidad_aire; DROP TABLE IF EXISTS dim_sensor; DROP TABLE IF EXISTS dim_tiempo;")
        con.executescript((ROOT / "sql" / "data_mart_schema.sql").read_text(encoding="utf-8"))

        time_dim = (
            df[["DateTime", "Date", "hora", "mes", "anio"]]
            .dropna(subset=["DateTime"])
            .drop_duplicates(subset=["DateTime"])
            .sort_values("DateTime")
            .reset_index(drop=True)
        )
        time_dim.insert(0, "tiempo_id", range(1, len(time_dim) + 1))
        time_dim = time_dim.rename(columns={"DateTime": "fecha_hora", "Date": "fecha"})
        time_dim[["tiempo_id", "fecha", "hora", "mes", "anio"]].to_sql(
            "dim_tiempo", con, if_exists="append", index=False
        )

        sensors = pd.DataFrame(
            [
                (1, "PT08.S1(CO)", "CO"),
                (2, "PT08.S2(NMHC)", "NMHC"),
                (3, "PT08.S3(NOx)", "NOx"),
                (4, "PT08.S4(NO2)", "NO2"),
                (5, "PT08.S5(O3)", "O3"),
            ],
            columns=["sensor_id", "nombre_sensor", "contaminante_nominal"],
        )
        sensors.to_sql("dim_sensor", con, if_exists="append", index=False)

        time_lookup = time_dim[["tiempo_id", "fecha_hora"]]
        fact = df.merge(time_lookup, left_on="DateTime", right_on="fecha_hora", how="inner")
        fact.insert(0, "medicion_id", range(1, len(fact) + 1))
        fact = fact.rename(
            columns={
                "CO(GT)": "co_gt",
                "NMHC(GT)": "nmhc_gt",
                "C6H6(GT)": "c6h6_gt",
                "NOx(GT)": "nox_gt",
                "NO2(GT)": "no2_gt",
                "PT08.S1(CO)": "pt08_s1_co",
                "PT08.S2(NMHC)": "pt08_s2_nmhc",
                "PT08.S3(NOx)": "pt08_s3_nox",
                "PT08.S4(NO2)": "pt08_s4_no2",
                "PT08.S5(O3)": "pt08_s5_o3",
                "T": "temperatura",
                "RH": "humedad_relativa",
                "AH": "humedad_absoluta",
                "banda_CO": "banda_co",
            }
        )
        cols = [
            "medicion_id",
            "tiempo_id",
            "co_gt",
            "nmhc_gt",
            "c6h6_gt",
            "nox_gt",
            "no2_gt",
            "pt08_s1_co",
            "pt08_s2_nmhc",
            "pt08_s3_nox",
            "pt08_s4_no2",
            "pt08_s5_o3",
            "temperatura",
            "humedad_relativa",
            "humedad_absoluta",
            "banda_co",
        ]
        fact[cols].to_sql("hecho_calidad_aire", con, if_exists="append", index=False)
        PBI.mkdir(parents=True, exist_ok=True)
        time_dim[["tiempo_id", "fecha", "hora", "mes", "anio"]].to_csv(PBI / "dim_tiempo.csv", index=False, encoding="utf-8-sig")
        sensors.to_csv(PBI / "dim_sensor.csv", index=False, encoding="utf-8-sig")
        fact[cols].to_csv(PBI / "hecho_calidad_aire.csv", index=False, encoding="utf-8-sig")
        counts = {
            table: con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in ["dim_tiempo", "dim_sensor", "hecho_calidad_aire"]
        }
    print(f"Data Mart creado: {DB}")
    print(f"Archivos para Power BI: {PBI}")
    print(counts)


if __name__ == "__main__":
    main()

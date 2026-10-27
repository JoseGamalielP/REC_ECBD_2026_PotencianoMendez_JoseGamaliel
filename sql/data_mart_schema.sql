-- Propuesta de esquema para el Data Mart de Air Quality.
CREATE TABLE dim_tiempo (
    tiempo_id INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    hora INTEGER NOT NULL,
    mes INTEGER,
    anio INTEGER
);

CREATE TABLE dim_sensor (
    sensor_id INTEGER PRIMARY KEY,
    nombre_sensor TEXT NOT NULL,
    contaminante_nominal TEXT
);

CREATE TABLE hecho_calidad_aire (
    medicion_id INTEGER PRIMARY KEY,
    tiempo_id INTEGER NOT NULL,
    co_gt REAL,
    nmhc_gt REAL,
    c6h6_gt REAL,
    nox_gt REAL,
    no2_gt REAL,
    pt08_s1_co REAL,
    pt08_s2_nmhc REAL,
    pt08_s3_nox REAL,
    pt08_s4_no2 REAL,
    pt08_s5_o3 REAL,
    temperatura REAL,
    humedad_relativa REAL,
    humedad_absoluta REAL,
    FOREIGN KEY (tiempo_id) REFERENCES dim_tiempo(tiempo_id)
);

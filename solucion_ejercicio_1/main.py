import pandas

#Punto A: Normalización de lecturas
def limpiar_lectura_medidor(registro_raw: dict)-> dict:
    datos_df = pandas.DataFrame(registro_raw)

    # Normalización de columna "zona"
    datos_df["medidor_id"] = datos_df["medidor_id"].str.strip()

    # Normalización de columna "caudal"
    datos_df["caudal"] = datos_df["caudal"].str.lower()
    datos_df["caudal"] = datos_df["caudal"].str.replace("l/min", "")
    datos_df["caudal"] = datos_df["caudal"].str.replace(",", ".")
    try:
        float(datos_df.at[0, "caudal"])
    except:
        raise ValueError(f"El caudal ingresado {registro_raw.get("caudal")} \
            no tiene ningún valor asignado"
        )
    datos_df["caudal"] = pandas.to_numeric(datos_df["caudal"])
    
    # Normalización de columna "zona"
    datos_df["zona"] = datos_df["zona"].str.strip()
    datos_df["zona"] = datos_df["zona"].replace("", pandas.NA).fillna("Zona no asignada")

    return datos_df.to_dict(orient="records")[0]

# Punto B: Reporte de caudal
def generar_reporte_caudal(lista_lecturas_limpias: list[dict], caudal_maximo: float)-> tuple:
    caudales_acumulados = 0
    ids_a_devolver = []
    for lectura in lista_lecturas_limpias:
        caudales_acumulados += lectura.get("caudal")
        if caudal_maximo < lectura.get("caudal"):
            ids_a_devolver.append(lectura.get("medidor_id"))

    promedio_caudales = caudales_acumulados / len(lista_lecturas_limpias)
    return (ids_a_devolver, promedio_caudales)

lista_registros = [
    {
        "medidor_id": [" MED-104 "], 
        "caudal": ["asdasdasadssa"], 
        "zona": [None]
    },
    {
        "medidor_id": [" MED-1078 "], 
        "caudal": ["20 l/min"], 
        "zona": [None]
    },
    {
        "medidor_id": [" MED-108 "], 
        "caudal": ["30 l/min"], 
        "zona": [None]
    },
]

lista_registros_limpios = []
for registro in lista_registros:
    try: lista_registros_limpios.append(limpiar_lectura_medidor(registro))
    except: continue

print(lista_registros_limpios)
print(generar_reporte_caudal(lista_registros_limpios, 5))
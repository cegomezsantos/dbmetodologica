from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# 1. Cargar los cuatro CSV con pandas
df_general    = pd.read_csv("data/_general.csv")
df_unidades   = pd.read_csv("data/_Unidades.csv")
df_contenidos = pd.read_csv("data/_contenidos.csv")
df_cursos     = pd.read_csv("data/_CURSOS_argos.csv")

###############################################################################
# RUTA DE INICIO
###############################################################################
@app.route("/")
def index():
    """
    Página de inicio con enlaces para:
      - Mostrar cada CSV individual
      - Realizar una consulta combinada
    """
    return render_template("index.html")

###############################################################################
# RUTA PARA MOSTRAR CADA CSV
###############################################################################
@app.route("/mostrar/<archivo>")
def mostrar_archivo(archivo):
    """
    Muestra los datos de cada CSV en una tabla HTML.
    El parámetro <archivo> define cuál de los 4 CSV se mostrará.
    """
    if archivo == "general":
        data = df_general
        titulo = "_general.csv"
    elif archivo == "unidades":
        data = df_unidades
        titulo = "_Unidades.csv"
    elif archivo == "contenidos":
        data = df_contenidos
        titulo = "_contenidos.csv"
    elif archivo == "cursos":
        data = df_cursos
        titulo = "_CURSOS_argos.csv"
    else:
        return "Archivo no reconocido."

    # Convertimos el DataFrame en lista de diccionarios para pasarlo a la plantilla
    registros = data.to_dict(orient="records")
    columnas = list(data.columns)

    return render_template("consulta.html", 
                           registros=registros, 
                           columnas=columnas, 
                           titulo=titulo)

###############################################################################
# RUTA PARA CONSULTA COMBINADA (MERGE)
###############################################################################
@app.route("/consulta", methods=["GET", "POST"])
def consulta():
    """
    Permite al usuario filtrar por la columna TXT003.
    En GET muestra un formulario simple.
    En POST hace el merge de los 4 CSV y filtra por el valor de TXT003 ingresado.
    """
    if request.method == "POST":
        # Obtener el valor que el usuario ingresa para filtrar por TXT003
        valor_id = request.form.get("valor_id", "").strip()

        # Hacemos el merge de los cuatro DataFrames usando la columna "TXT003"
        merged_df = df_general.merge(df_unidades, on="TXT003", how="inner")
        merged_df = merged_df.merge(df_contenidos, on="TXT003", how="inner")
        merged_df = merged_df.merge(df_cursos, on="TXT003", how="inner")

        # Si el usuario ingresó algo en el campo "valor_id", filtramos
        if valor_id:
            # Convertimos la columna "TXT003" a cadena y comparamos
            merged_df = merged_df[merged_df["TXT003"].astype(str) == valor_id]

        # Convertimos el resultado a lista de diccionarios para la plantilla
        registros = merged_df.to_dict(orient="records")
        columnas = list(merged_df.columns)

        return render_template("consulta.html", 
                               registros=registros, 
                               columnas=columnas, 
                               titulo="Consulta Combinada")
    else:
        # GET -> mostramos el formulario para filtrar
        return render_template("consulta_form.html")

###############################################################################
# EJECUCIÓN DE LA APLICACIÓN
###############################################################################
if __name__ == "__master__":
    app.run(debug=True)

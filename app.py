from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Función para leer el CSV y obtener la lista de cursos de la columna TXT003
def obtener_cursos():
    archivo_csv = "_CURSOS_argos.csv"  # Nombre del archivo en la raíz del proyecto
    df = pd.read_csv(archivo_csv, encoding="utf-8")  # Leer CSV con codificación UTF-8
    cursos = df["TXT003"].dropna().unique().tolist()  # Tomar valores únicos, eliminando NaN
    return cursos

@app.route("/")
def home():
    cursos = obtener_cursos()  # Llamar a la función para obtener los cursos
    return render_template("index.html", cursos=cursos)  # Pasar cursos a la plantilla

if __name__ == "__main__":
    app.run(debug=True)

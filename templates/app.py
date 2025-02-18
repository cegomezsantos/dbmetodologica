from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Función para leer el CSV y obtener la lista de valores únicos de TXT003
def obtener_cursos():
    archivo_csv = "_CURSOS_argos.csv"  # Nombre del archivo en la raíz del proyecto
    df = pd.read_csv(archivo_csv, encoding="utf-8")  # Asegura que los caracteres se lean correctamente
    cursos = df["TXT003"].dropna().unique().tolist()  # Elimina valores NaN y toma solo valores únicos
    return cursos

@app.route("/")
def home():
    cursos = obtener_cursos()
    return render_template("index.html", cursos=cursos)

if __name__ == "__main__":
    app.run(debug=True)

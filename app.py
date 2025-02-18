from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Función para leer el CSV y obtener la lista de cursos de la columna TXT003
def obtener_cursos():
    archivo_csv = "_CURSOS_argos.csv"  # Asegúrate de que este archivo está en la raíz del proyecto
    try:
        df = pd.read_csv(archivo_csv, encoding="utf-8")  # Leer CSV con codificación UTF-8
        print(df.head())  # Muestra las primeras filas en la terminal para verificar
        if "TXT003" not in df.columns:
            print("❌ ERROR: La columna 'TXT003' no existe en el CSV")
            return []
        cursos = df["TXT003"].dropna().unique().tolist()  # Tomar valores únicos, eliminando NaN
        print("Cursos obtenidos:", cursos)  # Verificar en la terminal los valores extraídos
        return cursos
    except Exception as e:
        print("❌ ERROR al leer el CSV:", e)
        return []

@app.route("/")
def home():
    cursos = obtener_cursos()
    return render_template("index.html", cursos=cursos)

if __name__ == "__main__":
    app.run(debug=True)

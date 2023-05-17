
from flask import Flask, render_template, request
import csv
import mysql.connector 
import pandas as pd

app = Flask(__name__)

mydb = mysql.connector.connect(
  user="root",
  password="9b687h3b",
  host="localhost",
  database="productos"
)
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM productos")

resultados = mycursor.fetchall()

# funciones que intentan printar lo indicado



productos = {}

# # Lee el csv

with open('productos.csv', 'r') as archivo:
    lector_csv = csv.reader(archivo)
    # Ignora la primera fila (encabezados)
    next(lector_csv)
    for fila in lector_csv:
        nombre = fila[0]
        descripcion = fila[1]
        precio = float(fila[2])
        categoria = fila[3]
        productos[nombre] = {'descripcion': descripcion, 'precio': precio, 'categoria': categoria}

# # Esto es para printar todos los productos del csv

nombres_productos = []




for producto in productos:
    nombres_productos.append(producto)

df = pd.read_csv("productos.csv")
nombres = df["nombre"].tolist()

nombres_productos = []

for producto in productos:
    nombres_productos.append(producto)

# def buscar(nombre):
#     resultados_desc = mostrar_descripcion(nombre)
#     resultados_precio = mostrar_precio(nombre)
#     resultados_cat = mostrar_categoria(nombre)
#     return resultados_desc, resultados_precio, resultados_cat

@app.route('/', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        # print(nombre)
        # Ejecutar la consulta SQL
        cursor_1 = mydb.cursor()
        cursor_1.execute(f"SELECT descripcion FROM productos where nombre = '{nombre}'")
        desc = cursor_1.fetchall()
        resultados_desc = desc[0][0]
        print(resultados_desc)

        cursor_2 = mydb.cursor()
        cursor_2.execute(f"SELECT precio FROM productos where nombre = '{nombre}'")
        precio = cursor_2.fetchall()
        resultados_precio = precio[0][0]
        print(resultados_precio)

        cursor_3 = mydb.cursor()
        cursor_3.execute(f"SELECT categoría FROM productos where nombre = '{nombre}'")
        cat = cursor_3.fetchall()
        resultados_cat = cat[0][0]
        print(resultados_cat)

        data = {
            'titulo': 'Productos',
            'bienvenida': 'Bienvenido, a continuación le mostraremos la lista de productos:',
        }
        return render_template('buscar.html',data=data,descripcion=resultados_desc,precio=resultados_precio,categoria=resultados_cat)
    else:
        cursor = mydb.cursor()
        cursor.execute(f"SELECT nombre FROM productos")
         # Obtener los resultados de la consulta
        resultados_GET = cursor.fetchall()
        data = {
            'titulo': 'Productos',
            'bienvenida': 'Bienvenido, a continuación le mostraremos la lista de productos:'
        }
        return render_template('index.html',data=data,nombres=resultados_GET, )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
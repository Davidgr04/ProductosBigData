from flask import Flask, render_template, request
import csv
import mysql.connector

app = Flask(__name__)

# conecta bd
# uf3 ultima practica como hacer para poner archivo sql en visualstudio para q lo pueda ver.
mydb = mysql.connector.connect(
  user="root",
  password="9b687h3b",
  host="localhost",
  database="productos_2"
)
# crea un objeto para moverse en mydb
mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM productos")

resultados = mycursor.fetchall()

# Crea el diccionario

productos = {}

# # Lee el csv

with open('productos.csv', 'r') as archivo:
    lector_csv = csv.reader(archivo)
    next(lector_csv)
    for fila in lector_csv:
        nombre = fila[0]
        descripcion = fila[1]
        precio = float(fila[2])
        categoria = fila[3]
        img = fila[4]
        # esta linea es la que guarda la descripcion el precio y la categoria en el diccionario "productos"
        productos[nombre] = {'descripcion': descripcion, 'precio': precio, 'categoria': categoria, 'img': img,}

@app.route('/', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
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

        cursor_4 = mydb.cursor()
        cursor_4.execute(f"SELECT categoría FROM productos where nombre = '{nombre}'")
        img = cursor_3.fetchall()
        resultados_img = img[0][0]
        print(resultados_img)

        data = {
            'titulo': 'Productos',
            'bienvenida': 'Bienvenido, a continuación le mostraremos la lista de productos:',
            'img_error': "Imagen de el producto : '{nombre}'"
        }
        return render_template('buscar.html',data=data,descripcion=resultados_desc,precio=resultados_precio,categoria=resultados_cat,img=resultados_img)
    else:
        # crea una lista llamada que contiene todos los nombres de productos del diccionario productos
        nombres_productos = list(productos.keys())
        data = {
            'titulo': 'Productos',
            'bienvenida': 'Bienvenido, a continuación le mostraremos la lista de productos:',
            'img_error': "Imagen de el producto : '{nombre}'"
        }
        return render_template('index.html', data=data, nombres=nombres_productos)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
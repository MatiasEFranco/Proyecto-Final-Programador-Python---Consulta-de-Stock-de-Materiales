'''
API Control de Stock
---------------------------
Autor: Franco Matias
Version: 1.1
 
Descripcion:
Se utiliza Flask para crear un WebServer que levanta las consultas realizadas sobre
los materiales de stock de una empresa, en este caso una Ferreteria.

Ejecución: Lanzar el programa y abrir en un navegador la siguiente dirección URL
NOTA: Si es la primera vez que se lanza este programa crear la base de datos
entrando a la siguiente URL
http://127.0.0.1:5000/reset

Ingresar a la siguiente URL para ver los endpoints disponibles
http://127.0.0.1:5000/
'''
__author__ = "Matias Ezequiel Franco"
__email__ = "franco_matias@live.com.ar"
__version__ = "1.1"

import csv
import os
import traceback
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for, flash
import stock
from datetime import datetime
from config import config

# Datos de la Configuracion del programa
# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))
# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
dataset = config('dataset', config_path_name)

# Crear el server Flask
app = Flask(__name__)

app.secret_key = 'mysecretkey'
planilla = []
planilla_stock = []

# Ruta que se ingresa por la ULR 127.0.0.1:5000 Pagina de Inicio
@app.route("/")
def index():
    try:
        return render_template('index.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000 Pagians principal de Consultas, mustras las consultas que se peuden realizar
@app.route("/consultas")
def consultas():
    try:
        print("Renderizar consultas.html")
        return render_template('consultas.html')
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000 Pagina donde realizamos las cosnultas del stock total
@app.route("/consultar_el_stock_total/<estado>", methods=['GET', 'POST'])
def consultar_el_stock_total(estado):
    if request.method == 'GET': 
        
        if estado == "no_mostrar":      # utilizamos este if para mostrar o no la planilla de stock, en este caso ocultamos la planilla "stock"  
            try:
                planilla_stock = []
            
                # Obtener de la query string los valores de limit y offset
                limit_str = str(request.args.get('limit'))
                offset_str = str(request.args.get('offset'))

                limit = 0
                offset = 0

                if(limit_str is not None) and (limit_str.isdigit()):
                    limit = int(limit_str)

                if(offset_str is not None) and (offset_str.isdigit()):
                    offset = int(offset_str)
    
                # Obtener el reporte
                planilla_stock = stock.report(limit=limit, offset=offset)
        
                # print(planilla_stock)
                # planilla_stock = 10
            
                # Renderizar el temaplate HTML stock total.html
                return render_template('consultar_el_stock_total.html', data_1=planilla_stock, data_2=[], estado=estado)
        
            except:
                return jsonify({'trace': traceback.format_exc()})
            
        if estado == "borrar":      # aqui estamos renderizando el template de la planilla stock con la eliminacion de un material desde la misma pagina HTML del stock
            try:
                return render_template('consultar_el_stock_total.html', estado=estado)
        
            except:
                return jsonify({'trace': traceback.format_exc()})
      
        if estado == "mostrar":     # utilizamos este if para mostrar o no la planilla de stock, en este caso mostramos la planilla "stock"        
            try:
                planilla_stock = []
            
                # Obtener de la query string los valores de limit y offset
                limit_str = str(request.args.get('limit'))
                offset_str = str(request.args.get('offset'))

                limit = 0
                offset = 0

                if(limit_str is not None) and (limit_str.isdigit()):
                    limit = int(limit_str)

                if(offset_str is not None) and (offset_str.isdigit()):
                    offset = int(offset_str)
    
                # Obtener el reporte
                planilla_stock = stock.report(limit=limit, offset=offset)
        
                # print(planilla_stock)
                # planilla_stock = 10
            
                # Renderizar el temaplate HTML stock total.html
                return render_template('consultar_el_stock_total.html', data_1=planilla_stock, data_2=[], estado=estado)
        
            except:
                return jsonify({'trace': traceback.format_exc()})
    
    if request.method == 'POST':        # aqui realiamos la consulta en la planilla de stock sobre un material si esta en sistema
        try:
            planilla_stock = []
            planilla = []
        
            # Obtener de la query string los valores de limit y offset
            limit_str = str(request.args.get('limit'))
            offset_str = str(request.args.get('offset'))

            limit = 0
            offset = 0

            if(limit_str is not None) and (limit_str.isdigit()):
                limit = int(limit_str)

            if(offset_str is not None) and (offset_str.isdigit()):
                offset = int(offset_str)
    
            # Obtener el reporte
            planilla_stock = stock.report(limit=limit, offset=offset)
           
            if str(request.form.get('codigo interno')) != "":
                codigo_a_buscar = str(request.form.get('codigo interno'))
            else:
                return redirect(url_for('consultar_el_stock_total', estado=estado))

            if(codigo_a_buscar is None or codigo_a_buscar.isdigit() is False): # aqui validamaos que no sea vacio y que sea un digito el valor ingresado
                # Datos ingresados incorrectos
                return Response(status=400)
                        
            planilla = stock.busqueda(codigo_a_buscar)
                
            #print(planilla_stock)
            #print(planilla)

            return render_template('consultar_el_stock_total.html', data_1=planilla_stock, data_2=planilla, codigo=codigo_a_buscar, accion="POST", estado=estado)
            
        except:
            return jsonify({'trace': traceback.format_exc()})        


# Ruta que se ingresa por la ULR 127.0.0.1:5000 Pagina donde realizamos las consultas por amteriales puntales
@app.route("/consultar_materiales", methods=['GET', 'POST'])
def consultar_materiales():
    if request.method == 'GET':     # aqui mostramos el template del HTML de consultar materiales 
        try:            
            print("Renderizar consultar materiales.html")
            #return render_template('consultar_materiales.html')
            return render_template('consultar_materiales.html', accion="No Consultar")

        except:
            return jsonify({'trace': traceback.format_exc()})
    
    if request.method == 'POST':        # aqui realiamos la busqueda del ccódigo del amterial a buscar
        try:
            codigo_b = str(request.form.get('codigo interno'))
            planilla = []

            if(codigo_b is None or codigo_b.isdigit() is False): # aqui validamaos que no sea vacio y que sea un digito el valor ingresado
                # Datos ingresados incorrectos
                return Response(status=400)
                        
            planilla = stock.busqueda(codigo_b)
            #print(planilla)
            return render_template('consultar_materiales.html', data=planilla, codigo=codigo_b, accion="Consultar")

        except:
            return jsonify({'trace': traceback.format_exc()})
            

# Ruta que se ingresa por la ULR 127.0.0.1:5000 Pagina donde realizamos la carga de nuevo materiales al sistema de stock
@app.route("/agregar/<codigo_a>", methods=['GET', 'POST']) 
def agregar(codigo_a):   
    if request.method == 'GET':
        try:
            # print(codigo_a)  
            if(codigo_a is None or codigo_a.isdigit() is False):                           
                return render_template('agregar.html', codigo_a=codigo_a, cargado="no")
            else:                           
                return render_template('agregar.html', codigo_a=int(codigo_a), cargado="no")
        
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:
            if ( str(request.form.get('codigo interno')) == None  and codigo_a != 11111 ):   
                codigo_interno = codigo_a
            else:
                codigo_interno = str(request.form.get('codigo interno'))
   
            cantidad_stock = str(request.form.get('cantidad'))
            descripcion = str(request.form.get('descripcion')).lower()
            print(codigo_interno, cantidad_stock, descripcion)
            
            if(codigo_interno is None or cantidad_stock is None or descripcion is None or codigo_interno.isdigit() is False or cantidad_stock.isdigit() is False): # aqui validamaos que no sea 0 y que sea un digito el valor ingresado
                # Datos ingresados incorrectos
                    return Response(status=400)

            planilla = []
            planilla = stock.busqueda(codigo_interno)
            
            if planilla != []:
                flash('El código interno ingresado ya existe en el sistema')
                return redirect('agregar.html')
            # print(planilla)
            stock.insert(int(codigo_interno), int(cantidad_stock), descripcion)
            print("Se agregaron correctamente")
            
            return render_template('agregar.html',  cargado="si", codigo_a=int(codigo_a))
        
        except:
            return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000 Pagina donde elimanamos materiales del sistema
@app.route("/delete/<codigo>", methods=['GET', 'POST'])
def borrar_material(codigo):
    if request.method == 'POST':        # utilizo un if porque puedo ingresar a esta funcion sin necesidad de que se por un POST, sino directamente desde la planilla que esta cargada como stock
        try:
            codigo = str(request.form.get('codigo interno'))
            
            if(codigo is None or codigo.isdigit() is False):                           
                flash('El código ingresado es erroneo')
                return render_template('consultar_el_stock_total', estado='borrar')
                
            tabla_1 = []
            tabla_2 = []
            limit_str = str(request.args.get('limit'))
            offset_str = str(request.args.get('offset'))
            limit = 0
            offset = 0
            
            if(limit_str is not None) and (limit_str.isdigit()):
                limit = int(limit_str)
            
            if(offset_str is not None) and (offset_str.isdigit()):
                offset = int(offset_str)
            
            tabla_1 = stock.report(limit=limit, offset=offset)
            tabla_2 = stock.busqueda(int(codigo))
            # print(tabla_1)
            # print(tabla_2)
            stock.delete(int(codigo)) 
                         
            return render_template('consultar_el_stock_total.html', data_1=tabla_1, data_2=tabla_2, accion="Borrar", estado='borrar')

        except:
            return jsonify({'trace': traceback.format_exc()})
        
    else:
        try:            
            if(codigo is None or codigo.isdigit() is False):                           
                flash('El código ingresado es erroneo')
                return render_template('consultar_el_stock_total', estado='borrar')
            
            stock.delete(int(codigo))       
            tabla_1 = []
            tabla_2 = []
            limit_str = str(request.args.get('limit'))
            offset_str = str(request.args.get('offset'))
            limit = 0
            offset = 0
            
            if(limit_str is not None) and (limit_str.isdigit()):
                limit = int(limit_str)
            
            if(offset_str is not None) and (offset_str.isdigit()):
                offset = int(offset_str)
            
            tabla_1 = stock.report(limit=limit, offset=offset)
            tabla_2 = stock.busqueda(int(codigo))
            # print(tabla_1)
            # print(tabla_2)
                         
            return render_template('consultar_el_stock_total.html', data_1=tabla_1, data_2=tabla_2, accion="Borrar", estado='mostrar')

        except:
            return jsonify({'trace': traceback.format_exc()})

# Ruta que se ingresa por la ULR 127.0.0.1:5000 Pagina donde podemos modifcar la cantidad y la descripcion de los materiales ya cargados en el sistema
@app.route("/modificar/<codigo>", methods=['GET', 'POST'])
def modificar_material(codigo):    
    if request.method == "GET":
        try:       
            tabla_1 = []
            tabla_2 = []
            limit_str = str(request.args.get('limit'))
            offset_str = str(request.args.get('offset'))
            limit = 0
            offset = 0
            
            if(limit_str is not None) and (limit_str.isdigit()):
                limit = int(limit_str)
            
            if(offset_str is not None) and (offset_str.isdigit()):
                offset = int(offset_str)
            
            tabla_1 = stock.report(limit=limit, offset=offset)
            tabla_2 = stock.busqueda(codigo)
            
            # print("Planilla de Stock")
            # print(tabla_1)
            # print("Planilla de Material")
            # print(tabla_2)
            # print(codigo)
            
            return render_template('consultar_el_stock_total.html',codigo=int(codigo), data_1=tabla_1, data_2=tabla_2, accion="Modificar", estado="no_mostrar")
        
        except:
            return jsonify({'trace': traceback.format_exc()})
    
    if request.method == "POST":
        try:
            cantidad_stock = str(request.form.get('cantidad'))
            descripcion = str(request.form.get('descripcion')).lower()
            stock.modificar(int(codigo), cantidad_stock, descripcion)       
            tabla_1 = []
            tabla_2 = []
            limit_str = str(request.args.get('limit'))
            offset_str = str(request.args.get('offset'))
            limit = 0
            offset = 0
            
            if(limit_str is not None) and (limit_str.isdigit()):
                limit = int(limit_str)
            
            if(offset_str is not None) and (offset_str.isdigit()):
                offset = int(offset_str)
            
            tabla_1 = stock.report(limit=limit, offset=offset)
            tabla_2 = stock.busqueda(codigo)
                         
            return render_template('consultar_el_stock_total.html', data_1=tabla_1, data_2=tabla_2, accion="Cambio", estado="no_mostrar")

        except:
            return jsonify({'trace': traceback.format_exc()})


###############################################################################################################################################################
# Este método se ejecutará solo una vez
# la primera vez que ingresemos a un endpoint generaremos la BD del Stock
@app.before_first_request
def before_first_request_func():        # con esta funcion creamos la BD y cargamos en la BD la informacion que tenemos en el CSV
# Indicamos al sistema (app) de donde leer la base de datos del Stock
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base de datos/stock.db"
    stock.db.init_app(app)
    #stock.db.drop_all()  # aqui limpiamos la BD al inciar el programa
    stock.db.create_all()

# Cargamos el CSV a la BD
    with open (dataset['stock']) as planilla_csv:     # Leemos todos los datos y los almaacenamos en una  lista de diccionarios
        planilla_stock = list(csv.DictReader(planilla_csv))
    stock.carga(planilla_stock) # aqui cargamos el archivo CSV a la BD por primera vez


    print("Base de datos del Stock generada")


if __name__ == '__main__':
    # Lanzar server
    app.run(host="127.0.0.1", port=5000)
    app.run(debug = True)

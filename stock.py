__author__ = "Matias Ezequiel Franco"
__email__ = "franco_matias@live.com.ar"
__version__ = "1.1"

from datetime import datetime
import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, update
from sqlalchemy.orm import relationship
import app_control_stock
db = SQLAlchemy()


class stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    codigo_interno = db.Column(db.Integer)
    cantidad_stock = db.Column(db.Integer)
    descripcion = db.Column(db.String)
    
    def __repr__(self):
        return f"codigo interno {self.codigo_interno} cantidad en stock {self.cantidad_stock} descripcion {self.descripcion}"


def insert(codigo, cantidad, descripcion): # funcion para agregar nuevos materiales  a la BD existente
    # Crear un nuevo material
    material = stock(codigo_interno=codigo, cantidad_stock=cantidad, descripcion=descripcion)

    # Agregar el material a la BD
    db.session.add(material)
    db.session.commit()


def report(limit, offset): 
    json_result_list = []

    query = db.session.query(stock)

    # Ordenamos por "codigo interno"
    query = query.order_by(stock.codigo_interno)

    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    for result in query:

        # print(result)
        json_result = {}
        json_result['codigo interno'] = result.codigo_interno
        json_result['cantidad en stock'] = result.cantidad_stock
        json_result['descripcion'] = result.descripcion
        json_result_list.append(json_result)

    return json_result_list


def busqueda(dato): # funcion que utilizamos para realizar la busqueda del material, nos devuelve la respuesta del query segun el dato enviado
    json_result_list = []
    
    query = db.session.query(stock).filter(stock.codigo_interno == dato)
    
    query_result = query.all()
    # print(query_result)
    
    if query_result is None or len(query_result) == 0:
        # No data register
        # Bug a proposito dejado para poner a prueba el traceback
        # ya que el sistema espera una tupla
        return []
    
    for result in query_result:
        # print(result)
        json_result = {}
        json_result['codigo interno'] = result.codigo_interno
        json_result['cantidad en stock'] = result.cantidad_stock
        json_result['descripcion'] = result.descripcion
        json_result_list.append(json_result)

    return json_result_list


def carga(planilla):    # funcion para cargar la BD stokc por primera vez    
    query = db.session.query(stock).all()
    # rint(query)
    if query is None or len(query) == 0:
        # print("vacia")
        for row in planilla:
            insert(int(row['ï»¿Codigo Interno']), row['Cantidad de stock'], row['Descripcion'])
 
 
def delete(codigo):     # funcion para eliminar materiales del stock
    # Borrar la persona con nombre "name"
    material = db.session.query(stock).filter(stock.codigo_interno == codigo).delete()
    db.session.commit()
    # print(material)

           
def modificar(codigo, cantidad, descripcion):       # funcion para modificar materiales cargados en el stock
    material = db.session.query(stock).filter(stock.codigo_interno == codigo)
    material = material.first()
    # print(material)

    if cantidad != []:
        material.cantidad_stock =  cantidad
        
    if descripcion != "":
        material.descripcion =  descripcion

    # print(material)
    db.session.add(material)
    db.session.commit()


if __name__ == "__main__":
    print("Test del modulo stock.py")

    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stock_prueba.db"     # BD para realizar pruebas de las fucniones creadas
    # Bindear la DB con nuestra app Flask
    db.init_app(app)
    app.app_context().push()

    db.create_all()

    # Test "insert"
    # Generamos datos inventados y probamos si funciona correctamente
    # la función insert
    insert(codigo=1115, cantidad=1234, descripcion="Tornillos MADERA") # estos datos son los que se peuden modificar para realizar la prueb ade las funciones y de la BD.
    '''
    codigo=1122
    material_b = busqueda(codigo)
    for result in material_b:        
        codigo_i_b = result.codigo_interno
        cantidad_b = result.cantidad_stock
        descripcion_b = result.descripcion 
    print(material_b)
    '''
    modificar(1115, 20, "Taladros 10mm")
    
    db.session.remove()
    db.drop_all()
    
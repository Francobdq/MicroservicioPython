import logging
from flask import Flask, make_response
from bdd import *

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logging.debug("Log habilitad!")

inicializar_db()


@app.route('/')
def saludar():
    app.logger.debug('Pagina principal...')

    conn = crear_conexion(database)
    usuarios = obtener_dato_usuario(conn,"*")

    if len(usuarios) == 0:
        app.logger.debug('Lista de usuarios!')
        return 'Aún no hay datos cargados'
    else:
        app.logger.debug('Mostrando lista de usuarios...')
        salida =  "Usuarios cargados:<ul>"
        for i in range(len(usuarios)):
            salida += "<li>" + str(usuarios[i]) +"</li>"
        return salida + "</ul>"

@app.route('/insertar/usuario/<apellido>/<nombre>/<dni>/<email>')
def crear_usuario(apellido, nombre, dni, email):
    conn = crear_conexion(database)
    datos = [apellido, nombre,dni,email]
    insertar_usuario(conn, datos)
    
    return 'usuario %s creado' % nombre

@app.route('/insertar/aula/<nombre>/<cant_max_usuarios>')
def crear_aula(nombre, cant_max_usuarios):
    conn = crear_conexion(database)
    insertar_aula(conn, nombre, cant_max_usuarios)
    
    return 'aula %s creada' % nombre


# Combina las 2 listas en un unico string para crear el csv luego
def normalizarListasCSV(lista, lista1):
    total = ""
    for i in range(len(lista)):
        string = str(lista[i]) + "," + str(lista1[i])
        total += string + "\n"

    return total

def normalizarListaCSV(lista):
    total = ""
    for i in range(len(lista)):
        string = str(lista[i])
        total += string + "\n"

    return total


@app.route('/aulas/csv')  
def download_csv_aulas():  
    logging.debug("aulas csv!")
    # Creo conexión con la bdd y obtengo todos los usuarios
    conn = crear_conexion(database)

    nombres = obtener_dato_aula(conn, "nombre")
    cant_max_usuarios = obtener_dato_aula(conn, "cant_max_usuarios")

    csv = "\n" + normalizarListasCSV(nombres,cant_max_usuarios) #el \n es para dejar la cabecera sin nada
    response = make_response(csv)
    cd = 'attachment; filename=aulascsv.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response


@app.route('/csv/')  
def download_csv():  
    logging.debug("csv!")
    # Creo conexión con la bdd y obtengo todos los usuarios
    conn = crear_conexion(database)

    
    nombres = obtener_dato_usuario(conn, "*")

    logging.debug(nombres)

    csv = "\n" + normalizarListaCSV(nombres)
    response = make_response(csv)
    cd = 'attachment; filename=usuarioscsv.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response
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


    usuarios = obtener_dato(conn,"*")

    if len(usuarios) == 0:
        app.logger.debug('Lista de usuarios!')
        return 'Aún no hay datos cargados'
    else:
        app.logger.debug('Mostrando lista de usuarios...')
        salida =  "Usuarios cargados:<ul>"
        for i in range(len(usuarios)):
            salida += "<li>" + str(usuarios[i]) +"</li>"
        return salida + "</ul>"

@app.route('/insertar/usuario/<apellido>/<nombre>/<dni>/<email>/<num_telefono>')
def crear_usuario(apellido, nombre, dni, email, num_telefono):
    conn = crear_conexion(database)
    datos = [apellido, nombre,dni,email,num_telefono]
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



@app.route('/csv/')  
def download_csv():  
    logging.debug("csv!")
    # Creo conexión con la bdd y obtengo todos los usuarios
    conn = crear_conexion(database)

    nombres = obtener_dato(conn, "nombre")
    dni = obtener_dato(conn, "dni")

    csv = "\n" + normalizarListasCSV(nombres,dni) #el \n es para dejar la cabecera sin nada
    response = make_response(csv)
    cd = 'attachment; filename=mycsv.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response
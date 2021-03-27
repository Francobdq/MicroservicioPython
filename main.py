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
    nombre = obtener_usuarios(conn)
    dni = obtener_dni(conn)

    if len(nombre) == 0:
        app.logger.debug('Lista de usuarios!')
        return 'Aún no hay datos cargados'
    else:
        app.logger.debug('Mostrando lista de usuarios...')
        salida =  "Usuarios cargados:<ul>"
        for i in range(len(nombre)):
            salida += "<li>" + str(nombre[i]) + "  - " + str(dni[i]) +"</li>"
        return salida + "</ul>"



@app.route('/insertar/<nombre>/<dni>')
def saludar_usuario(nombre,dni):
    conn = crear_conexion(database)
    
    insertar_usuario(conn, nombre,dni)
    

    return 'Hola %s' % nombre


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
    nombres = obtener_usuarios(conn)
    dni = obtener_dni(conn)
    #csv = 'foo,bar,baz\nhai,bai,crai\n'  
    csv = "\n" + normalizarListasCSV(nombres,dni)#list_de_lista(saludados)  #el \n es para dejar la cabecera sin nada
    response = make_response(csv)
    cd = 'attachment; filename=mycsv.csv'
    response.headers['Content-Disposition'] = cd 
    response.mimetype='text/csv'

    return response
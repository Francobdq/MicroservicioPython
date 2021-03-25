import logging
from flask import Flask, render_template
from bdd import *

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
logging.debug("Log habilitad!")

inicializar_db()

@app.route('/')
def saludar():
    app.logger.debug('Pagina principal...')

    conn = crear_conexion(database)
    saludados = obtener_usuarios(conn)

    if len(saludados) == 0:
        app.logger.debug('Aun no saludo a ningún usuario!')
        return 'Aun no he saludado a nadie hoy'
    else:
        app.logger.debug('Mostrando lista de usuarios saludados...')
        ya_saludados =  "Hoy saludé a:<ul>"
        for nombre in saludados:
            ya_saludados += "<li>" + nombre + "</li>"
        return ya_saludados + "</ul>"




@app.route('/saludar/<usurname>')
def saludar_usuario(usurname):
    conn = crear_conexion(database)
    insertar_usuario(conn, usurname)
    return 'Hola %s' % usurname



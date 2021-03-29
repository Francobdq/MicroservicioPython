import os
import sqlite3
import logging

from sqlite3 import Error

nombreSQLSCRIPT = "bdd_sql.sql"
database = os.getcwd() + "\\sqlite_saludos.db"

def crear_conexion(db_file):

    conn = None
    try:
        logging.debug('Conectandose a la DB SQLite o creandola...')
        conn = sqlite3.connect(db_file)
        logging.debug('DB SQLITE creada ' + sqlite3.version)
    except Error as e:
        logging.error(e)

    return conn



def insertar_usuario(conn, usuario,dni):
    sql = 'INSERT INTO usuarios(nombre,dni) VALUES(?,?);'

    logging.debug("Insertando usuario: " + usuario)
    cur = conn.cursor() 
    cur.executemany(sql, [(usuario,dni)])
    conn.commit()
    logging.debug("Usuario insertado!")


def obtener_dato(conn, dato):
    logging.debug("Obteniendo usuarios...")
    cur = conn.cursor()
    cur.execute("SELECT %s FROM usuarios" % dato)

    usuarios = []
    
    rows = cur.fetchall()

    logging.debug(str(len(rows)) + " usuarios obtenidos...")

    for row in rows:
        usuarios.append(row)

    return usuarios

# Se inicializa la base de datos
def inicializar_db():          

    # Se comprueba la existencia de la db
    existeDB = os.path.isfile(database) 
    # se intenta crear la conexión      
    conn = crear_conexion(database) 
    if conn is not None:     
        try:
            # Si no existe se crean las tablas
            if(not existeDB):
                logging.debug("Creando tablas en la db...")
                # se abre el archivo .sql con las intrucciones para generar la base de datos
                sql_file = open(nombreSQLSCRIPT)
                # se lee el archivo
                sql_as_string = sql_file.read()
                # luego se executa en forma de script estas instrucciones (creando así la base de datos) 
                conn.executescript(sql_as_string)
            else:
                logging.debug("Las tablas no necesitan ser creadas. Ya lo están.")
        except Error as e:
            logging.error(e)
    else:
        logging.error("Error, no se puede crear la conexion:")

        
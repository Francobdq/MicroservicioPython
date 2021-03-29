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



def insertar_usuario(conn, datos):
    sql = 'INSERT INTO usuarios(apellido, nombre, dni, email, num_telefono) VALUES(?,?,?,?,?);'

    logging.debug("Insertando usuario: " + datos[0] + " " + datos[1])
    cur = conn.cursor() 
    cur.executemany(sql, [datos]) #cur.executemany(sql, [(datos[0],datos[1])])
    conn.commit()
    logging.debug("Usuario insertado!")


def insertar_aula(conn, nombre, cant_max_usuarios):
    sql = 'INSERT INTO aulas(nombre,cant_max_usuarios) VALUES(?,?);'
    logging.debug("Insertando aula: " + nombre)
    cur = conn.cursor() 
    cur.executemany(sql, [(nombre,cant_max_usuarios)])
    conn.commit()
    logging.debug("aula insertada!")


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

        
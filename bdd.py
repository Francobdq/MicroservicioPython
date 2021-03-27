import os
import sqlite3
import logging

from sqlite3 import Error

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

def crear_tabla(conn, create_table_sql):
    try:
        logging.debug("Creando tabla en la DB...")
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logging.error(e)

def insertar_usuario(conn, usuario,dni):
    sql = 'INSERT INTO usuarios(nombre,dni) VALUES(?,?);'

    logging.debug("Insertando usuario: " + usuario)
    cur = conn.cursor() 
    cur.executemany(sql, [(usuario,dni)])
    conn.commit()
    logging.debug("Usuario insertado!")

def obtener_usuarios(conn):
    logging.debug("Obteniendo usuarios...")
    cur = conn.cursor()
    cur.execute("SELECT nombre FROM usuarios")

    saludados = []
    
    rows = cur.fetchall()

    logging.debug(str(len(rows)) + " usuarios obtenidos...")

    for row in rows:
        saludados.append(row[0])

    return saludados

def obtener_dni(conn):
    logging.debug("Obteniendo usuarios...")
    cur = conn.cursor()
    cur.execute("SELECT dni FROM usuarios")

    saludados = []
    
    rows = cur.fetchall()

    logging.debug(str(len(rows)) + " dni obtenidos...")

    for row in rows:
        saludados.append(row[0])

    return saludados


def inicializar_db():

    sql_crear_tabla_usuarios = """ CREATE TABLE IF NOT EXISTS usuarios (
                                        id intenger PRIMARY KEY, 
                                        nombre text NOT NULL,
                                        dni intenger NOT NULL
                                    ); """
    conn = crear_conexion(database)

    if conn is not None:
        crear_tabla(conn, sql_crear_tabla_usuarios)
    else:
        logging.error("Error, no se puede crear la conexion:")

        
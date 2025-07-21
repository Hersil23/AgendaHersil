#importamos sqlite3 para manejar la base de datos

import sqlite3 # es un modulo de python que permite manejar una base de datos SQlite, es una parte de la libreria de python por la que no es necesario instalar nada mas.

#creamos la clase DBManager: esto es como  un objeto en js, y el self es como this en js, es una referencia a la instancia de la clase. 
class DBManager:

  def __init__(self, db_name="./Agenda/Agenda.db"):
    self.db_name = db_name
    self.conn = None
    self.cursor = None


  def Conn(self): #creamos el metodo que permite a nuestra clase DBManager conectarse a la base de datos.
    try: # se inicia la conexion de la base de datos con un bloque try para manejar posibles errores.
      self.conn = sqlite3.Connection(self.db_name) # esto crea una conexion a la base de datos, si no existe la crea.
      self.cursor = self.conn.cursor() # esto crea un cursor que nos permite ejecutar comandos SQL.
      print(f"Te has conectado a la Base de Datos correctamente") # esta linea imprime un mensaje de confirmacion si la conexion es exitosa.
      except sqlite3.Error as e: # si ocurre un error al conectar, se captura la excepcion y se imprime un mensaje de error.
      print(f"Error al conectar a la Base de Datos: {e}") # esto imprime el error especifico que ocurrio al intentar conectar a la base de datos.


  def close(self): #creamos el metodo cerrar mi conexion a la base de datos
    if self.conn:
      self.cursor.close()
      self.conn.close()
      print(f"Te has desconectado de la Base de Datos correctamente")
      


def create_table(self): # creamos el metodo que permite crear una tabla en la base de datos
  try:
    self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS contacts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL,
                            phone TEXT NOT NULL
                        );
                        """) # este comando SQL crea una tabla llamada contacts con cuatro columnas: id, name, email y phone.
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
                            phone TEXT UNIQUE NOT NULL 
                        );
                        """) # este comando SQL crea una tabla llamada contacts con cuatro columnas: id, name, email y phone.
  except sqlite3.Error as e:
    print(f"Error al crear la tabla: {e}")

def insert_contact(self, name, email, phone):
  try:
    self.Conn()
    self.cursor.execute("""
                        INSERT INTO contacts (name, email, phone) 
                        VALUES (?, ?, ?);
                        """, (name, email, phone)) # este comando SQL inserta un nuevo contacto en la tabla contacts.
    self.conn.commit() # esto guarda los cambios en la base de datos.
    print(f"Contacto {name} insertado correctamente") # esta linea imprime un mensaje de confirmacion si la insercion es exitosa.
    return True

  except sqlite3.IntegrityError as e:
    print(f" El contacto {name} ya existe en la base de datos, su numero ya esta registrado:")
    return False
  except sqlite3.Error as e:
    print(f"Error al insertar el contacto: {e}")
    return False
  finally:
    self.close()

def insert_many_contacts(self, list_contacts):
  try:
    self.Conn()
    self.cursor.executemany("INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?);", list_contacts) # este comando SQL inserta varios contactos en la tabla contacts.
    self.conn.commit() # esto guarda los cambios en la base de datos.
    print(f"Contactos insertados correctamente") # esta linea imprime un mensaje de confirmacion si la insercion es exitosa.
    return True 
  except sqlite3.IntegrityError as e:
    print(f" Uno o mas contactos ya existen en la base de datos, porque su numero ya esta registrado:")
    return False
  except sqlite3.Error as e:
    print(f"Error al insertar contactos: {e}")
    return False
  finally:
    self.close()

def read_contacts(self):
  try:
    self.Conn()
    self.cursor.execute("SELECT * FROM contacts;") # este comando SQL selecciona todos los contactos de la tabla contacts.
    contacts = self.cursor.fetchall() # esto obtiene todos los resultados de la consulta.
    return contacts # devuelve la lista de contactos.
  except sqlite3.Error as e:
    print(f"Error al leer los contactos: {e}")
    return []
  finally:
    self.close()

def search_contact(self, column, value): # creamos el metodo que permite buscar un contacto por una columna y un valor especifico
  try:
    self.Conn()
    if column not in ["name", "phone", "email"]: # verificamos si la columna existe en la tabla contacts
      print(f"La columna {column} no existe")
      return []
    #No hay errores y la columna existe
    self.cursor.execute(f"SELECT * FROM contacts WHERE {column} LIKE ?",(f"%{value}%",))# # este comando SQL busca contactos en la tabla contacts donde el valor de la columna especificada coincide con el valor dado.
    contact = self.cursor.fetchall()
    return contact
  except sqlite3.Error as e:
    print(f"Error al buscar el valor: {value} en la columna {column}: {e}")
    return []
  finally:
    self.close()

def update_contact(self,id,new_name=None,new_phone=None,new_email=None): # creamos el metodo que permite actualizar un contacto por su id
  try:
    self.Conn()
    query_part = [] # esta lista se usara para almacenar las partes de la consulta SQL que se van a actualizar
    values = [] # esta lista se usara para almacenar los valores que se van a actualizar
    
    if new_name is not None: # verificamos si se proporciono un nuevo nombre
      query_part.append("name = ?") # esto agrega la parte de la consulta para actualizar el nombre
      values.append(new_name) # esto agrega el nuevo nombre a la lista de valores
    if new_phone is not None: # verificamos si se proporciono un nuevo telefono
      query_part.append("phone = ?") # esto agrega la parte de la consulta para actualizar el telefono
      values.append(new_phone) # esto agrega el nuevo telefono a la lista de valores
    if new_email is not None: # verificamos si se proporciono un nuevo email
      query_part.append("email = ?") # esto agrega la parte de la consulta para actualizar el email
      values.append(new_email) # esto agrega el nuevo email a la lista de valores
    if not query_part:
      print("No se proporcionaron valores para actualizar")
      return False
    
    values.append(id)
    query = ", ".join(query_part)
    self.cursor.execute(f"UPDATE contacts SET {query} WHERE id = ?", tuple(values))
    self.conn.commit()
    
    if self.cursor.rowcount > 0:
      print(f"Contacto {id} actualizado con exito")
      return True
    else:
      print(f"Contacto {id} no encontrado")
      return False
  except sqlite3.IntegrityError as e:
    print(f"El contacto {id} ya existe en la agenda, porque su numero ya esta registrado")
    return False
  except sqlite3.Error as e:
    print(f"Error al actualizar el contacto: {e}")
    return False
  finally:
    self.close()

def delete_contact(self, contact_id): # creamos el metodo que permite eliminar un contacto por su id
  try:
    self.Conn()
    self.cursor.execute("DELETE FROM contacts WHERE id = ?",(contact_id,)) # este comando SQL elimina un contacto de la tabla contacts donde el id coincide con el id dado.
    self.conn.commit()
    if self.cursor.rowcount > 0: # verificamos si se elimino alguna fila
      print(f"Contacto {contact_id} eliminado con exito")
      return True
    else:
      print(f"Contacto {contact_id} no encontrado") # si no se elimino ninguna fila, significa que el contacto no existe
      return False
  except sqlite3.Error as e: # si ocurre un error al eliminar el contacto, se captura la excepcion y se imprime un mensaje de error
    print(f"Error al eliminar el contacto: {e}")
    return False
  finally:
    self.close()

if __name__ == "__main__":
  manager = DBManager()
  manager.Conn()
  manager.create_table() #Ejecutenlo 1 sola vez
  
  #Insert
  manager.insert_contact("Herasi","Herasi777@gmail","12312133445678")
  manager.insert_contact("Cris","crissivira9@gmail","135652345678")
  manager.insert_many_contacts([
    ("Herasi","Herasi777@gmail","1234768585678"),
    ("Cris","crissivira9@gmail","12343645755678"),
    ("Delvis","delvissivira9@gmail","127898089345678")
  ])
  
  #Read
  print(manager.read_contacts())
  print(manager.search_contact("name","Cris"))
  
  #Update
  manager.update_contact(1,new_name="PaulaTheRevolution",new_email="paulaDev25@gmail")
  
  #Delete
  manager.delete_contact(3)
  manager.close()
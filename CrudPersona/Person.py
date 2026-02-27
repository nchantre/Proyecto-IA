import mysql.connector
from mysql.connector import errorcode


def get_connection():
    """Establece y devuelve una conexión a la base de datos MySQL.
    La base de datos se llama `ia-person` y se asume que está accesible
    en localhost con usuario `root` y sin contraseña. Ajustar según sea necesario.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ia-person",
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe. Creando...")
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE `ia-person` DEFAULT CHARACTER SET 'utf8' ")
            conn.database = "ia-person"
            return conn
        else:
            raise


def create_table():
    """Crea la tabla `person` en la base de datos si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS person (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombres VARCHAR(255) NOT NULL,
            telefono VARCHAR(50),
            edad INT,
            cedula VARCHAR(50)
        ) ENGINE=InnoDB
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


def add_person(nombres: str, telefono: str, edad: int, cedula: str) -> int:
    """Inserta una nueva persona y devuelve el id creado."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO person (nombres, telefono, edad, cedula) VALUES (%s, %s, %s, %s)",
        (nombres, telefono, edad, cedula),
    )
    conn.commit()
    person_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return person_id


def get_person_by_id(person_id: int) -> dict | None:
    """Recupera una persona por su id. Devuelve un diccionario o None si no existe."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM person WHERE id = %s", (person_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


def get_all_persons() -> list[dict]:
    """Devuelve todas las personas registradas."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM person")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def update_person(person_id: int, nombres: str, telefono: str, edad: int, cedula: str) -> bool:
    """Actualiza los datos de una persona. Devuelve True si se modificó alguna fila."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE person
        SET nombres = %s, telefono = %s, edad = %s, cedula = %s
        WHERE id = %s
        """,
        (nombres, telefono, edad, cedula, person_id),
    )
    conn.commit()
    modified = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return modified


def delete_person(person_id: int) -> bool:
    """Elimina una persona por id. Devuelve True si se borró alguna fila."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM person WHERE id = %s", (person_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    cursor.close()
    conn.close()
    return deleted


if __name__ == "__main__":
    # Ejemplo de uso simple en modo texto
    create_table()
    print("Tabla creada o ya existente.")
    while True:
        print("\nOperaciones disponibles:")
        print("1. Agregar persona")
        print("2. Ver persona por id")
        print("3. Listar todas las personas")
        print("4. Actualizar persona")
        print("5. Eliminar persona")
        print("6. Salir")
        op = input("Selecciona una opción: ")
        if op == "1":
            nombres = input("Nombres: ")
            telefono = input("Telefono: ")
            edad = int(input("Edad: "))
            cedula = input("Cedula: ")
            pid = add_person(nombres, telefono, edad, cedula)
            print(f"Persona insertada con id {pid}")
        elif op == "2":
            pid = int(input("Id: "))
            persona = get_person_by_id(pid)
            print(persona)
        elif op == "3":
            personas = get_all_persons()
            for p in personas:
                print(p)
        elif op == "4":
            pid = int(input("Id de la persona a actualizar: "))
            nombres = input("Nombres: ")
            telefono = input("Telefono: ")
            edad = int(input("Edad: "))
            cedula = input("Cedula: ")
            if update_person(pid, nombres, telefono, edad, cedula):
                print("Actualizado correctamente.")
            else:
                print("No se encontró la persona.")
        elif op == "5":
            pid = int(input("Id de la persona a eliminar: "))
            if delete_person(pid):
                print("Eliminado correctamente.")
            else:
                print("No se encontró la persona.")
        elif op == "6":
            break
        else:
            print("Opción inválida")

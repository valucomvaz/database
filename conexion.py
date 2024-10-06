import sqlite3
import pandas as pd

def menu():
    print("BASE DE DATOS DE MUSICA.")
    while True:
        try:
            eleccion = int(input("ELIJA UNA OPCION DEL MENU: \n 1. Ingresar datos de una cancion \n 2. Consultar datos \n 3. Modificar los datos de una cancion \n 4. Eliminar una cancion \n 5. Mostrar el contenido de la tabla \n 6. Salir \n ->"))
            if eleccion in [1, 2, 3, 4, 5, 6]:
                return eleccion
            else:
                print("Opcion no valida. Intente de nuevo.")
        except ValueError:
            print("Opcion no valida. Ingrese un numero.")


def ingresar_datos():
    print("1. INGRESAR LOS DATOS DE UNA CANCION")
    cancion = input("Ingrese el nombre de la cancion: ").capitalize()
    artista = input("Ingrese el artista: ").capitalize()
    genero = input("Ingrese el genero musical: ").capitalize()
    album = input("Ingrese el album: ").capitalize()
    año = int(input("Ingrese el año de lanzamiento: "))
    while año < 1900 or año > 2024:
        año = int(input("Ingrese un año valido (entre 1900 y 2024): "))
    curs.execute("INSERT INTO Musica (cancion, artista, genero, album, año) VALUES (?, ?, ?, ?, ?)", (cancion, artista, genero, album, año))
    conexion.commit()
    print("Cancion ingresada correctamente.")

def consultar_datos():
    print("2. CONSULTAR DATOS")
    mostrar_datos()
    consulta = input("¿Que le gustaria consultar? \n A. Todas las canciones de un artista \n B. Todas las canciones de un genero \n C. Todas las canciones de un album \n D. Todas las canciones de un año \n E. Mostrar las canciones ordenadas segun su orden alfabetico \n F. Ordenar las canciones segun su año de lanzamiento \n Ingrese una opcion de la lista: ").upper()
    if consulta == "A":
        a()
    elif consulta == "B":
        b()
    elif consulta == "C":
        c()
    elif consulta == "D":
        d()
    elif consulta == "E":
        e()
    elif consulta == "F":
        f()
    else:
        print("Opcion no valida.")
        return

def a():
    print("A. Todas las canciones de un artista")
    buscar = input("Ingrese el artista: ")
    curs.execute("SELECT * FROM Musica WHERE artista=?", (buscar,))
    busqueda = curs.fetchall()
    if busqueda:
        for datos in busqueda:
            print(datos)
    else:
        print(f"No se encontraron canciones de '{buscar}' en los registros.")


def b():
    print("B. Todas las canciones de un genero")
    buscar = input("Ingrese el genero: ")
    curs.execute("SELECT * FROM Musica WHERE genero=?", (buscar,))
    busqueda = curs.fetchall()
    if busqueda:
        for datos in busqueda:
            print(datos)
    else:
        print(f"No se encontraron canciones de '{buscar}' en los registros.")

def c():
    print("C. Todas las canciones de un album")
    buscar = input("Ingrese el album: ")
    curs.execute("SELECT * FROM Musica WHERE album=?", (buscar,))
    busqueda = curs.fetchall()
    if busqueda:
        for datos in busqueda:
            print(datos)
    else:
        print(f"No se encontraron canciones de '{buscar}' en los registros.")

def d():
    print("D. Todas las canciones de un año")
    buscar = int(input("Ingrese el año: "))
    curs.execute("SELECT * FROM Musica WHERE año=?", (buscar,))
    busqueda = curs.fetchall()
    if busqueda:
        for datos in busqueda:
            print(datos)
    else:
        print(f"No se encontraron canciones de '{buscar}' en los registros.")

def e():
    print("E. Mostrar las canciones segun su orden alfabetico")
    buscar = input("¿De que forma? \n A. De la A-Z \n B. De la Z-A \n ").upper()
    if buscar == "A":
        curs.execute("SELECT * FROM Musica ORDER BY cancion ASC")
        busqueda = curs.fetchall()
        for datos in busqueda:
            print(datos)
    elif buscar == "B":
        curs.execute("SELECT * FROM Musica ORDER BY cancion DESC")
        busqueda = curs.fetchall()
        for datos in busqueda:
            print(datos)

def f():
    print("F. Ordenar las canciones segun su año de lanzamiento")
    buscar = input("¿De que forma? \n A. Menor a mayor \n B. Mayor a menor \n ").upper()
    if buscar == "A":
        curs.execute("SELECT * FROM Musica ORDER BY año ASC")
        busqueda = curs.fetchall()
        for datos in busqueda:
            print(datos)
    elif buscar == "B":
        curs.execute("SELECT * FROM Musica ORDER BY año DESC")
        busqueda = curs.fetchall()
        for datos in busqueda:
            print(datos)
    else:
        print("Opcion no valida.")
        return

def modificar_datos():
    print("3. MODIFICAR LOS DATOS DE UNA CANCION")
    mostrar_datos()
    try:
        elemento = int(input("Ingrese el ID de la cancion que desea modificar: "))
    except ValueError:
        print("El ID debe ser un numero entero.")
        return
    categoria = input("Ingrese la categoria que desea modificar (cancion/artista/genero/album/año): ").lower()
    if categoria == "cancion":
        cancion_nueva = input("Ingrese un nuevo nombre para la cancion: ")
        curs.execute("UPDATE Musica SET cancion=? WHERE id=?", (cancion_nueva, elemento))
    elif categoria == "artista":
        artista_nuevo = input("Ingrese un nuevo artista para la cancion: ")
        curs.execute("UPDATE Musica SET artista=? WHERE id=?", (artista_nuevo, elemento))
    elif categoria == "genero":
        genero_nuevo = input("Ingrese un nuevo genero para la cancion: ")
        curs.execute("UPDATE Musica SET genero=? WHERE id=?", (genero_nuevo, elemento))
    elif categoria == "album":
        album_nuevo = input("Ingrese un nuevo album para la cancion: ")
        curs.execute("UPDATE Musica SET album=? WHERE id=?", (album_nuevo, elemento))
    elif categoria == "año":
        año_nuevo = int(input("Ingrese un nuevo año para la cancion: "))
        while año_nuevo < 1900 or año_nuevo > 2024:
            año_nuevo = int(input("Ingrese un año valido (entre 1900 y 2024): "))
        curs.execute("UPDATE Musica SET año=? WHERE id=?", (año_nuevo, elemento))
    else:
        print("Categoria no valida.")
        return
    conexion.commit()
    print("Datos actualizados correctamente.")

def eliminar_datos():
    print("4. ELIMINAR UNA CANCION")
    mostrar_datos()
    elemento = int(input("Ingrese el ID de la cancion que desea eliminar: "))
    curs.execute("DELETE FROM Musica WHERE id=?", (elemento,))
    # Elemento con la coma al final se convierte en tupla !!!
    conexion.commit()
    print("Cancion eliminada correctamente.")

def mostrar_datos():
    print("5. MOSTRAR EL CONTENIDO DE UNA TABLA")
    df = pd.read_sql_query("SELECT * FROM Musica", conexion)
    print(df)
    cantidad = len(df)
    print(f"En la tabla hay {cantidad} canciones.")

# MAIN -------------------------------

conexion = sqlite3.connect('musica.db')
curs = conexion.cursor()
# Crear la base de datos
try:
    curs.execute("""
        CREATE TABLE Musica (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cancion TEXT NOT NULL,
            artista TEXT NOT NULL,
            genero TEXT,
            album TEXT,
            año INT
        )
    """)
    conexion.commit()
except sqlite3.OperationalError:
    pass
# Usar el menú y realizar las operaciones, pero en bucle hasta que se decida salir
while True:
    funcion = menu()
    if funcion == 1:
        ingresar_datos()
    elif funcion == 2:
        consultar_datos()
    elif funcion == 3:
        modificar_datos()
    elif funcion == 4:
        eliminar_datos()
    elif funcion == 5:
        mostrar_datos()
    elif funcion == 6:
        print("Programa terminado.")
        break

# Cerrar la conexión
conexion.close()
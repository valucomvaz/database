from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = '0000'

def get_db_connection():
    conn = sqlite3.connect('musica.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    with get_db_connection() as conn:
        try:
            conn.execute("""
                CREATE TABLE Musica (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cancion TEXT NOT NULL,
                    artista TEXT NOT NULL,
                    genero TEXT,
                    album TEXT,
                    año INT
                )
            """)
            conn.commit()
        except sqlite3.OperationalError:
            pass

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar_cancion():
    if request.method == 'POST':
        cancion = request.form['titulo'].capitalize()
        artista = request.form['artista'].capitalize()
        genero = request.form['genero'].capitalize()
        album = request.form['album'].capitalize()
        
        try:
            año = int(request.form['año'])
            if año < 1900 or año > 2024:
                flash('Ingrese un año válido (entre 1900 y 2024).')
                return render_template('ingresar.html', 
                                       cancion=cancion, 
                                       artista=artista, 
                                       genero=genero, 
                                       album=album, 
                                       año=request.form['año'])

            with get_db_connection() as conn:
                conn.execute("INSERT INTO Musica (cancion, artista, genero, album, año) VALUES (?, ?, ?, ?, ?)", 
                             (cancion, artista, genero, album, año))
                conn.commit()

            flash('Canción ingresada correctamente.')
            return render_template('ingresar.html', 
                                   cancion=cancion, 
                                   artista=artista, 
                                   genero=genero, 
                                   album=album, 
                                   año=año)

        except ValueError:
            flash('El año debe ser un número entero.')
            return render_template('ingresar.html', 
                                   cancion=cancion, 
                                   artista=artista, 
                                   genero=genero, 
                                   album=album, 
                                   año=request.form['año'])

    return render_template('ingresar.html')

@app.route('/consultar', methods=['GET', 'POST'])
def consultar_canciones():
    conn = get_db_connection()
    
    if request.method == 'POST':
        consulta = request.form['consulta'].upper()
        df = None

        if consulta in ["E", "F"]:
            if consulta == "E":
                df = pd.read_sql_query("SELECT * FROM Musica ORDER BY cancion ASC", conn)
            elif consulta == "F":
                df = pd.read_sql_query("SELECT * FROM Musica ORDER BY año ASC", conn)
        else:
            if 'parametro' in request.form:
                parametro = request.form['parametro'].capitalize()
                if consulta == "A":
                    df = pd.read_sql_query("SELECT * FROM Musica WHERE artista=?", conn, params=(parametro,))
                elif consulta == "B":
                    df = pd.read_sql_query("SELECT * FROM Musica WHERE genero=?", conn, params=(parametro,))
                elif consulta == "C":
                    df = pd.read_sql_query("SELECT * FROM Musica WHERE album=?", conn, params=(parametro,))
                elif consulta == "D":
                    try:
                        año = int(parametro)
                        df = pd.read_sql_query("SELECT * FROM Musica WHERE año=?", conn, params=(año,))
                    except ValueError:
                        flash("Por favor, ingrese un año válido.")
                        df = pd.read_sql_query("SELECT * FROM Musica", conn)

        conn.close()
        return render_template('consultar.html', canciones=df.to_dict(orient='records') if df is not None else None)

    df = pd.read_sql_query("SELECT * FROM Musica", conn)
    conn.close()
    return render_template('consultar.html', canciones=None)



@app.route('/modificar', methods=['GET', 'POST'])
def modificar_cancion():
    mensaje = None
    if request.method == 'POST':
        id_cancion = request.form['id']
        categoria = request.form['categoria'].lower()
        nuevo_valor = request.form['nuevo_valor'].capitalize()

        try:
            if categoria == "año":
                nuevo_año = int(nuevo_valor)
                if nuevo_año < 1900 or nuevo_año > 2024:
                    flash('Ingrese un año válido (entre 1900 y 2024).')
                    return render_template('modificar.html', mensaje=mensaje)

            with get_db_connection() as conn:
                if categoria == "cancion":
                    conn.execute("UPDATE Musica SET cancion=? WHERE id=?", (nuevo_valor, id_cancion))
                elif categoria == "artista":
                    conn.execute("UPDATE Musica SET artista=? WHERE id=?", (nuevo_valor, id_cancion))
                elif categoria == "genero":
                    conn.execute("UPDATE Musica SET genero=? WHERE id=?", (nuevo_valor, id_cancion))
                elif categoria == "album":
                    conn.execute("UPDATE Musica SET album=? WHERE id=?", (nuevo_valor, id_cancion))
                elif categoria == "año":
                    conn.execute("UPDATE Musica SET año=? WHERE id=?", (nuevo_año, id_cancion))

                conn.commit()
            
            mensaje = "Datos actualizados correctamente."
            flash("Datos actualizados correctamente.")
        except ValueError:
            flash('El año debe ser un número entero.')

    return render_template('modificar.html', mensaje=mensaje)


@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar_cancion():
    mensaje = None
    if request.method == 'POST':
        id_cancion = request.form['id']
        
        with get_db_connection() as conn:
            conn.execute("DELETE FROM Musica WHERE id=?", (id_cancion,))
            conn.commit()

        mensaje = "Canción eliminada correctamente."
        flash(mensaje)

    return render_template('eliminar.html')


@app.route('/mostrar')
def mostrar_contenido():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM Musica", conn)
    conn.close()
    return render_template('mostrar.html', canciones=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
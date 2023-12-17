from flask import Flask, Response, render_template, request, jsonify, session, redirect, url_for
from utilidadas_request import request_id, request_print, sacar_id
import csv
import threading
import time

app = Flask(__name__)
app.secret_key = 'kUEnoKzrU5VB6CQ'  # Puedes generar una clave secreta aleatoria


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuarios = leer_usuarios_csv()

        if username in usuarios and usuarios[username]['password'] == password:
            session['usuario_logueado'] = username  # Establecer la sesión de usuario
            session['apikey'] = usuarios[username]['apikey']  # Almacenar la API key en la sesión
            return redirect('/dashboard')
        else:
            error = "Nombre de usuario o contraseña incorrectos."

    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'usuario_logueado' not in session:
        return redirect('/')    # Aquí puedes incluir lógicas para obtener datos para mostrar en el dashboard
    return render_template('dashboard.html')


@app.route('/imprimir_etiqueta', methods=['GET', 'POST'])
def imprimir_etiqueta():
    if 'usuario_logueado' not in session:
        return redirect('/')
    if 'usuario_logueado' in session:
        apikey = session['apikey']
    if request.method == 'POST':
        numero_envio = request.form['numero_envio']
        envio_modificado = leer_envio_origen(numero_envio)

        if envio_modificado:

            #response_id = sacar_id(envio_modificado)
            response_id = request_id(envio_modificado, apikey)
            if response_id and 'Data' in response_id and response_id['Data']['Data']:
                id_envio = response_id['Data']['Data'][0]['Id']
                html_response = request_print(id_envio, envio_modificado, apikey)
                if html_response:
                    ruta_pdf = guardar_pdf(html_response, envio_modificado)  # Guardar la etiqueta en PDF
                    url_pdf = url_for('static', filename=f'pdfs/{envio_modificado}.pdf')  # Obtener la URL del archivo
                    eliminar_pdf_despues(ruta_pdf, 300)  # Eliminar después de 5 minutos (300 segundos)
                    return jsonify({'pdf_url': url_pdf})
                else:
                    return jsonify({'error': 'Error al obtener la etiqueta HTML.'}), 400
            else:
                return jsonify({'error': 'Error al obtener ID del envío.'}), 400
        else:
            return jsonify({'error': 'El número de envío no tiene un formato válido. Intente nuevamente.'}), 400
    else:
        return render_template('imprimir_etiquetas.html')


@app.route('/logout')
def logout():
    session.pop('usuario_logueado', None)  # Eliminar el usuario de la sesión
    return redirect('/')


def leer_envio_origen(envio_origen):
    if len(envio_origen) == 12:
        # Procesamiento para envíos de 12 dígitos
        return envio_origen
    elif len(envio_origen) == 22:
        # Procesamiento para envíos de 22 dígitos
        parte1 = envio_origen[6:11]  # Del dígito 6 al 11
        parte2 = envio_origen[12:19]  # Del dígito 12 al 19
        return parte1 + parte2
    else:
        print("Número de envío no válido")
        return None


def guardar_pdf(response, envio_modificado):
    ruta_completa = f'static/pdfs/{envio_modificado}.pdf'
    with open(ruta_completa, 'wb') as f:
        f.write(response.content)
    return ruta_completa




def abrir_pdf_en_navegador(envio_modificado):
    file_path = f'etiquetas/{envio_modificado}.pdf'
    try:
        with open(file_path, 'rb') as file:
            pdf_data = file.read()
        return Response(pdf_data, content_type='application/pdf')
    except FileNotFoundError:
        return "Etiqueta no encontrada."

def eliminar_pdf_despues(ruta_archivo, retraso):
    """
    Elimina el archivo PDF después de un período de tiempo especificado.
    """
    def tarea():
        time.sleep(retraso)
        os.remove(ruta_archivo)

    thread = threading.Thread(target=tarea)
    thread.start()
def leer_usuarios_csv():
    with open('bdd.csv', mode='r') as file:
        reader = csv.DictReader(file)
        return {row['username']: {'password': row['password'], 'apikey': row['apikey']} for row in reader}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Ejecutar el servidor web Flask en segundo plano

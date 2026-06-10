from flask import Flask, render_template, request
import urllib.request
import urllib.parse
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Configuración segura de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
try:
    # Recuerda subir tu archivo .json a Render con este mismo nombre: creds-spa.json
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds-spa.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Datos Spa").sheet1
except Exception as e:
    print(f"Error con Google Sheets: {e}")
    sheet = None

def enviar_aviso_telegram(mensaje):
    if not TOKEN or not CHAT_ID:
        return
    try:
        params = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': mensaje})
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?{params}"
        with urllib.request.urlopen(url) as respuesta:
            return respuesta.read()
    except Exception as e:
        print(f"Error en Telegram: {e}")

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/agendar', methods=['POST'])
def agendar():
    nombre = request.form.get('nombre')
    servicio = request.form.get('servicio')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    
    if sheet:
        # 1. VERIFICAR SI EL LUGAR ESTÁ OCUPADO
        todas_las_citas = sheet.get_all_values()
        for fila in todas_las_citas:
            if len(fila) > 3 and fila[2] == fecha and fila[3] == hora:
                return render_template('index.html', error_ocupado=True, fecha_ocu=fecha, hora_ocu=hora)
        
        # 2. GUARDAR DATOS SI ESTÁ LIBRE
        sheet.append_row([nombre, servicio, fecha, hora])
        
        # 3. ORDENAR AUTOMÁTICAMENTE POR FECHA (Columna 3) Y HORA (Columna 4)
        sheet.sort((3, 'asc'), (4, 'asc'))
        
    # 4. MANDAR NOTIFICACIÓN DE ÉXITO A TU TELEGRAM
    mensaje_notificacion = (
        f"🎀 ¡NUEVA CITA CONFIRMADA! 🎀\n\n"
        f"👤 Clienta: {nombre}\n"
        f"💅 Servicio: {servicio}\n"
        f"📅 Fecha: {fecha}\n"
        f"⏰ Hora: {hora}\n\n"
        f"✅ Guardada y ordenada en Excel."
    )
    enviar_aviso_telegram(mensaje_notificacion)
    
    # 5. CARGAR EL NUEVO DOCUMENTO DE CONFIRMACIÓN
    return render_template('confirmacion.html', nombre=nombre, servicio=servicio, fecha=fecha, hora=hora)

@app.route('/cancelar', methods=['POST'])
def cancelar():
    nombre_cancela = request.form.get('nombre_cancelar')
    fecha_cancela = request.form.get('fecha_cancelar')
    
    if sheet:
        todas_las_citas = sheet.get_all_values()
        for index, fila in enumerate(todas_las_citas):
            if len(fila) > 2 and fila[0].lower() == nombre_cancela.lower() and fila[2] == fecha_cancela:
                sheet.delete_rows(index + 1)
                enviar_aviso_telegram(f"❌ Cita Cancelada: {nombre_cancela} eliminó su espacio del día {fecha_cancela}.")
                return render_template('index.html', cancelacion_exitosa=True)
                
    return render_template('index.html', cancelacion_error=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

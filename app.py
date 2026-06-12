from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Configuración de Google Sheets con búsqueda dual (Local y Render)
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
try:
    ruta_credenciales = '/etc/secrets/creds-spa.json'
    if not os.path.exists(ruta_credenciales):
        ruta_credenciales = 'creds-spa.json'
        
    creds = ServiceAccountCredentials.from_json_keyfile_name(ruta_credenciales, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Datos Spa").sheet1
except Exception as e:
    print(f"Error con Google Sheets: {e}")
    sheet = None

# FUNCIÓN 1: Te avisa a ti (Tu Telegram personal)
def enviar_aviso_telegram(mensaje):
    if not TOKEN or not CHAT_ID:
        return
    try:
        params = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': mensaje})
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?{params}"
        with urllib.request.urlopen(url) as respuesta:
            return respuesta.read()
    except Exception as e:
        print(f"Error en Telegram Gestor: {e}")

# FUNCIÓN 2: Le responde a tus clientas con un menú de botones táctiles
def enviar_mensaje_cliente(chat_id, mensaje):
    if not TOKEN:
        return
    try:
        teclado_interactivo = {
            "keyboard": [
                [{"text": "💅 Ver Servicios"}, {"text": "📍 Ubicación"}],
                [{"text": "📞 Hablar con Rubi"}]
            ],
            "resize_keyboard": True,
            "one_time_keyboard": False
        }
        
        data = {
            "chat_id": chat_id,
            "text": mensaje,
            "reply_markup": json.dumps(teclado_interactivo)
        }
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as respuesta:
            return respuesta.read()
    except Exception as e:
        print(f"Error respondiendo a la clienta: {e}")

@app.route('/')
def inicio():
    return render_template('index.html')

# RUTA MÁGICA: Escucha lo que escriben en Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        texto = update["message"].get("text", "")
        
        if texto.startswith("/start"):
            partes = texto.split(" ")
            if len(partes) > 1 and "Confirmacion_" in partes[1]:
                nombre_cliente = partes[1].replace("Confirmacion_", "").replace("_", " ")
                bienvenida = (
                    f"¡Hola {nombre_cliente}! 🎀✨\n\n"
                    f"Gracias por validar tu asistencia. Tu cita ya quedó agendada de forma segura en nuestro Excel administrativo. 📊\n\n"
                    f"¿Deseas consultar algo más? Usa los botones de abajo 👇"
                )
            else:
                bienvenida = (
                    "¡Hola Bella! 🎀✨\n\n"
                    "Bienvenida al asistente virtual de Glow & Elegance.\n"
                    "Aquí puedes consultar información y servicios al instante.\n\n"
                    "¿Qué te gustaría hacer hoy? Elige una opción 👇"
                )
            enviar_mensaje_cliente(chat_id, bienvenida)
            
        elif texto == "💅 Ver Servicios":
            servicios_txt = (
                "🎀 Nuestros Servicios Exclusivos 🎀\n\n"
                "💅 Manicura Spa ($350): Diseños coquette personalizados, acrílico y esmaltado semipermanente impecable.\n"
                "🌸 Masaje Relajante ($500): Desconexión total con aromaterapia floral y aceites esenciales.\n\n"
                "✨ Agenda tu espacio directamente en nuestra página web corporativa."
            )
            enviar_mensaje_cliente(chat_id, servicios_txt)
            
        elif texto == "📍 Ubicación":
            ubicacion_txt = (
                "📍 Glow & Elegance Spa\n\n"
                "Te esperamos en nuestro santuario de belleza.\n"
                "🕒 Horario: Lunes a Sábado de 10:00 AM a 7:00 PM.\n\n"
                "✨ ¡Recuerda asistir con 5 minutos de anticipación!"
            )
            enviar_mensaje_cliente(chat_id, ubicacion_txt)
            
        elif texto == "📞 Hablar con Rubi":
            rubi_txt = (
                "👤 Contacto Directo con Dirección:\n\n"
                "Hola, soy Rubi. Si tienes dudas sobre algún diseño especial o requieres atención personalizada, "
                "puedes marcarme o escribirme un WhatsApp. ¡Te atenderé con mucho gusto! 🌸"
            )
            enviar_mensaje_cliente(chat_id, rubi_txt)

    return "OK", 200

# CONFIGURADOR DE UN SOLO CLIC
@app.route('/configurar_bot')
def configurar_bot():
    base_url = request.base_url.replace('/configurar_bot', '')
    if "onrender.com" in base_url:
        base_url = base_url.replace("http://", "https://")
    
    webhook_url = f"{base_url}/webhook"
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
    try:
        with urllib.request.urlopen(url) as respuesta:
            res = respuesta.read().decode('utf-8')
            return f"🤖 ¡Bot configurado! Interactividad activada en: {webhook_url}. Respuesta: {res}"
    except Exception as e:
        return f"Error al enlazar el bot: {e}"

@app.route('/agendar', methods=['POST'])
def agendar():
    nombre = request.form.get('nombre')
    servicio = request.form.get('servicio')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    
    if sheet:
        # Validación para evitar duplicados
        todas_las_citas = sheet.get_all_values()
        for fila in todas_las_citas:
            if len(fila) > 3 and fila[2] == fecha and fila[3] == hora:
                return render_template('index.html', error_ocupado=True, fecha_ocu=fecha, hora_ocu=hora)
        
        # Guardar la nueva fila al final
        sheet.append_row([nombre, servicio, fecha, hora])
        
        # ORDENAMIENTO DINÁMICO INTELIGENTE
        # Contamos cuántas filas hay exactamente (incluyendo la nueva)
        total_filas = len(sheet.get_all_values())
        
        # Si hay más de 1 fila (es decir, hay títulos y al menos una cita)
        if total_filas > 1:
            # Ordenamos estrictamente desde la fila 2 hasta la fila exacta donde termina la información
            rango_exacto = f'A2:D{total_filas}'
            sheet.sort((3, 'asc'), (4, 'asc'), range=rango_exacto)
        
    mensaje_notificacion = f"🎀 ¡NUEVA CITA! 🎀\n\n👤 Clienta: {nombre}\n💅 Servicio: {servicio}\n📅 Fecha: {fecha}\n⏰ Hora: {hora}\n\n✅ Registrada en Excel."
    enviar_aviso_telegram(mensaje_notificacion)
    
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
                enviar_aviso_telegram(f"❌ Cita Cancelada: {nombre_cancela} liberó el día {fecha_cancela}.")
                return render_template('index.html', cancelacion_exitosa=True)
                
    return render_template('index.html', cancelacion_error=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

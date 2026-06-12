from flask import Flask, render_template, request, jsonify
import urllib.request
import urllib.parse
import os
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ==========================================
# 🎀 CONFIGURACIÓN DE TU SPA (LLENA TUS DATOS AQUÍ)
# ==========================================
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

NUMERO_WHATSAPP = "4501116459" # Pon tu número con código de país, sin el +
NUMERO_TELEFONO = "+524501116459" # Pon tu número con el +
LINK_GOOGLE_MAPS = "https://maps.google.com/?q=19.432608,-99.133209"
LATITUD = 19.432608 # Coordenada Norte/Sur
LONGITUD = -99.133209 # Coordenada Este/Oeste
URL_PAGINA_WEB = "https://spa-coquette.onrender.com" # Cambia por tu URL si es distinta

# ==========================================
# CONEXIÓN A GOOGLE SHEETS (INTACTA)
# ==========================================
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

# ==========================================
# HERRAMIENTAS AVANZADAS DE TELEGRAM
# ==========================================

# 1. Menú Principal Fijo (Teclado Inferior)
menu_principal = {
    "keyboard": [
        [{"text": "💅 Servicios"}, {"text": "📅 Agendar Cita"}],
        [{"text": "📍 Ubicación"}, {"text": "📞 Contacto"}],
        [{"text": "🎁 Promos"}, {"text": "🕒 Horarios"}],
        [{"text": "❓ Ayuda"}]
    ],
    "resize_keyboard": True,
    "is_persistent": True
}

# 2. Enviar "Escribiendo..." para dar realismo
def enviar_chat_action(chat_id, action="typing"):
    if not TOKEN: return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendChatAction"
        data = {"chat_id": chat_id, "action": action}
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except: pass

# 3. Enviar Mensaje con Teclados Interactivos
def enviar_mensaje(chat_id, texto, reply_markup=None):
    if not TOKEN: return
    try:
        data = {"chat_id": chat_id, "text": texto, "parse_mode": "HTML"}
        if reply_markup:
            data["reply_markup"] = reply_markup
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as e: print(f"Error enviando msg: {e}")

# 4. Enviar Foto Profesional
def enviar_foto(chat_id, photo_url, caption, reply_markup=None):
    if not TOKEN: return
    try:
        data = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": "HTML"}
        if reply_markup:
            data["reply_markup"] = reply_markup
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as e: print(f"Error enviando foto: {e}")

# 5. Enviar Ubicación GPS de Telegram
def enviar_ubicacion(chat_id, lat, lon, reply_markup=None):
    if not TOKEN: return
    try:
        data = {"chat_id": chat_id, "latitude": lat, "longitude": lon}
        if reply_markup:
            data["reply_markup"] = reply_markup
        url = f"https://api.telegram.org/bot{TOKEN}/sendLocation"
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except Exception as e: print(f"Error enviando ubicacion: {e}")

# 6. Registrar el menú flotante del bot ("/")
def configurar_menu_comandos():
    if not TOKEN: return
    comandos = {
        "commands": [
            {"command": "start", "description": "🎀 Ir al menú principal"},
            {"command": "servicios", "description": "💅 Ver catálogo de servicios"},
            {"command": "agendar", "description": "📅 Agendar cita en línea"},
            {"command": "ubicacion", "description": "📍 Ver ubicación y mapa"},
            {"command": "contacto", "description": "📞 Hablar con Rubi"},
            {"command": "promociones", "description": "🎁 Ver promos actuales"},
            {"command": "horarios", "description": "🕒 Consultar horarios"},
            {"command": "ayuda", "description": "❓ Ayuda y dudas"}
        ]
    }
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/setMyCommands"
        req = urllib.request.Request(url, data=json.dumps(comandos).encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
    except: pass

def enviar_aviso_telegram(mensaje):
    enviar_mensaje(CHAT_ID, mensaje)

# ==========================================
# RUTAS DE FLASK Y LÓGICA DEL BOT
# ==========================================

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    if "message" in update and "text" in update["message"]:
        chat_id = update["message"]["chat"]["id"]
        texto = update["message"]["text"]
        
        # Simulamos que el bot está pensando/escribiendo
        enviar_chat_action(chat_id, "typing")
        
        # 🎀 MENÚ PRINCIPAL Y /START
        if texto.startswith("/start") or texto == "🔙 Menú Principal" or texto == "start":
            partes = texto.split(" ")
            if len(partes) > 1 and "Confirmacion_" in partes[1]:
                nombre_cliente = partes[1].replace("Confirmacion_", "").replace("_", " ")
                bienvenida = f"<b>¡Hola {nombre_cliente}! 🎀✨</b>\n\nTu cita ya quedó agendada de forma segura en nuestro sistema administrativo. 📊\n\n¿En qué más te puedo ayudar hoy?"
            else:
                bienvenida = "<b>¡Bienvenida a Glow & Elegance! 🎀✨</b>\n\nTu santuario de belleza coquette. Soy tu asistente virtual y estoy aquí para ayudarte a lucir espectacular.\n\nPor favor, selecciona una opción del menú 👇"
            enviar_mensaje(chat_id, bienvenida, menu_principal)
            
        # 💅 SERVICIOS (Envía foto de catálogo)
        elif texto == "/servicios" or texto == "💅 Servicios":
            enviar_chat_action(chat_id, "upload_photo")
            img_url = "https://images.unsplash.com/photo-1604654894610-df63bc536371?auto=format&fit=crop&w=800&q=80"
            servicios_txt = (
                "<b>🎀 Catálogo de Servicios Exclusivos 🎀</b>\n\n"
                "💅 <b>Manicura Spa ($350)</b>\nDiseños coquette, acrílico y esmaltado semipermanente impecable.\n\n"
                "🌸 <b>Masaje Relajante ($500)</b>\nDesconexión total con aromaterapia floral y aceites esenciales.\n\n"
                "✨ <i>Todos nuestros servicios incluyen una bebida de cortesía.</i>"
            )
            enviar_foto(chat_id, img_url, servicios_txt, menu_principal)
            
        # 📅 AGENDAR (Botón en línea)
        elif texto == "/agendar" or texto == "📅 Agendar Cita":
            inline_agendar = {
                "inline_keyboard": [
                    [{"text": "🌐 Agendar en Línea Ahora", "url": f"{URL_PAGINA_WEB}/#reservas"}]
                ]
            }
            enviar_mensaje(chat_id, "¡Excelente elección! 🌸\n\nPara garantizar tu espacio y registrarlo en nuestra base de datos, por favor agenda a través de nuestra plataforma oficial segura👇", inline_agendar)

        # 📍 UBICACIÓN (GPS + Enlace a Maps)
        elif texto == "/ubicacion" or texto == "📍 Ubicación":
            enviar_chat_action(chat_id, "find_location")
            # Primero envía el mapa de Telegram interactivo
            enviar_ubicacion(chat_id, LATITUD, LONGITUD)
            # Luego envía los detalles con botón
            inline_maps = {
                "inline_keyboard": [
                    [{"text": "🗺️ Abrir en Google Maps", "url": LINK_GOOGLE_MAPS}]
                ]
            }
            ubi_txt = "<b>📍 Glow & Elegance Spa</b>\n\nEncuéntranos en nuestro santuario de belleza. Arriba tienes nuestra ubicación exacta.\n\n✨ <i>Te sugerimos llegar 5 minutos antes de tu cita.</i>"
            enviar_mensaje(chat_id, ubi_txt, inline_maps)
            
        # 📞 CONTACTO (Llamada + WhatsApp)
        elif texto == "/contacto" or texto == "📞 Contacto":
            inline_contacto = {
                "inline_keyboard": [
                    [{"text": "💬 Escribir por WhatsApp", "url": f"https://wa.me/{NUMERO_WHATSAPP}"}],
                    [{"text": "📱 Llamar a Dirección", "url": f"tel:{NUMERO_TELEFONO}"}]
                ]
            }
            contacto_txt = "<b>👤 Contacto Directo</b>\n\nHola, soy <b>Rubi</b>. Será un placer atenderte personalmente. Si necesitas un diseño especial o tienes dudas sobre un tratamiento, presiona los botones abajo 👇"
            enviar_mensaje(chat_id, contacto_txt, inline_contacto)

        # 🎁 PROMOCIONES
        elif texto == "/promociones" or texto == "🎁 Promos":
            enviar_chat_action(chat_id, "upload_photo")
            img_promo = "https://images.unsplash.com/photo-1522337660859-02fbefca4702?auto=format&fit=crop&w=800&q=80"
            promo_txt = "<b>✨ Promociones del Mes ✨</b>\n\n💖 <b>Paquete Coquette:</b>\nManicura Spa + Masaje Relajante por solo <b>$750 MXN</b> (Ahorras $100).\n\n👯‍♀️ <b>Promo Amigas:</b>\nTrae a una amiga y ambas reciben 15% de descuento en uñas acrílicas.\n\n<i>Válido mencionando este mensaje al agendar.</i>"
            enviar_foto(chat_id, img_promo, promo_txt, menu_principal)
            
        # 🕒 HORARIOS
        elif texto == "/horarios" or texto == "🕒 Horarios":
            horarios_txt = "<b>🕒 Nuestros Horarios de Atención</b>\n\n🌸 Lunes a Viernes: 10:00 AM - 7:00 PM\n🌸 Sábados: 10:00 AM - 4:00 PM\n💤 Domingos: Cerrado (Día de spa en casa)\n\n<i>Nota: Se atienden citas fuera de horario con previo aviso y costo extra.</i>"
            enviar_mensaje(chat_id, horarios_txt, menu_principal)

        # ❓ AYUDA / CUALQUIER OTRO TEXTO
        else:
            ayuda_txt = "<b>❓ Centro de Ayuda Glow</b>\n\nSi te perdiste, no te preocupes. Puedes usar mi menú de botones inferior, o escribir el símbolo <b>/</b> para ver los comandos rápidos.\n\n¿Qué deseas hacer?"
            enviar_mensaje(chat_id, ayuda_txt, menu_principal)

    return "OK", 200

# ==========================================
# RUTAS DE ADMINISTRACIÓN Y EXCEL
# ==========================================

@app.route('/configurar_bot')
def configurar_bot():
    base_url = request.base_url.replace('/configurar_bot', '')
    if "onrender.com" in base_url:
        base_url = base_url.replace("http://", "https://")
    
    webhook_url = f"{base_url}/webhook"
    
    # 1. Registramos el Webhook
    url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
    try:
        urllib.request.urlopen(url)
        # 2. Registramos el Menú de Comandos (/) de Telegram
        configurar_menu_comandos()
        return f"🤖 ¡Bot configurado y Comandos activados exitosamente en: {webhook_url}!"
    except Exception as e:
        return f"Error al enlazar el bot: {e}"

@app.route('/agendar', methods=['POST'])
def agendar():
    nombre = request.form.get('nombre')
    servicio = request.form.get('servicio')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    
    if sheet:
        todas_las_citas = sheet.get_all_values()
        for fila in todas_las_citas:
            if len(fila) > 3 and fila[2] == fecha and fila[3] == hora:
                return render_template('index.html', error_ocupado=True, fecha_ocu=fecha, hora_ocu=hora)
        
        sheet.append_row([nombre, servicio, fecha, hora])
        total_filas = len(sheet.get_all_values())
        if total_filas > 1:
            sheet.sort((3, 'asc'), (4, 'asc'), range=f'A2:D{total_filas}')
        
    mensaje_notificacion = f"🎀 ¡NUEVA CITA! 🎀\n\n👤 Clienta: <b>{nombre}</b>\n💅 Servicio: {servicio}\n📅 Fecha: {fecha}\n⏰ Hora: {hora}\n\n✅ Registrada en Excel."
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
                enviar_aviso_telegram(f"❌ Cita Cancelada: <b>{nombre_cancela}</b> liberó el día {fecha_cancela}.")
                return render_template('index.html', cancelacion_exitosa=True)
                
    return render_template('index.html', cancelacion_error=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import urllib.request
import urllib.parse

app = Flask(name)

# Configuración del Bot de Telegram (Fase 5)
TOKEN = "8630752464:AAEj-8UWE5DXPYlODb1nvRQubUtI4D4Nz-4"
CHAT_ID = "6373108325" 

def enviar_aviso_telegram(mensaje):
    """Función auxiliar para enviar notificaciones automáticas a Telegram"""
    if CHAT_ID == "6373108325":
        print("Aviso: Falta configurar el CHAT_ID de Telegram.")
        return
    try:
        texto_codificado = urllib.parse.quote(mensaje)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={texto_codificado}"
        # Realiza la petición en segundo plano
        urllib.request.urlopen(url)
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

# Esta ruta principal ("/") cargará tu archivo HTML e iniciará el bot
@app.route('/')
def inicio():
    # El bot te avisará cada vez que alguien cargue la página
    enviar_aviso_telegram("✨ ¡Rubi! Alguien acaba de visitar tu página de Spa Coquette 💅🎀")
    return render_template('index.html')

if name == 'main':
    app.run(debug=True)

from flask import Flask, render_template
import urllib.request
import urllib.parse

app = Flask(name)

# Configuración del Bot de Telegram
TOKEN = "8630752464:AAEj-8UWE5DXPYlODb1nvRQubUtI4D4Nz-4"
CHAT_ID = "6373108325" 

def enviar_aviso_telegram(mensaje):
    """Función auxiliar para enviar notificaciones automáticas a Telegram"""
    if CHAT_ID != "6373108325":
        print("Aviso: Falta configurar el CHAT_ID de Telegram.")
        return
    try:
        texto_codificado = urllib.parse.quote(mensaje)
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={texto_codificado}"
        urllib.request.urlopen(url)
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")
        
@app.route('/')
def inicio():
    enviar_aviso_telegram("✨ ¡Rubi! Alguien acaba de visitar tu página de Spa Coquette 💅🎀")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import urllib.request
import urllib.parse
import os

app = Flask(name)

# Lee las llaves desde Render (se configura en el paso 2)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_aviso_telegram(mensaje):
    if not TOKEN or not CHAT_ID:
        return
    try:
        params = urllib.parse.urlencode({'chat_id': CHAT_ID, 'text': mensaje})
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?{params}"
        with urllib.request.urlopen(url) as respuesta:
            return respuesta.read()
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def inicio():
    enviar_aviso_telegram("✨ ¡Rubi! Alguien acaba de visitar tu página de Spa Coquette 💅🎀")
    return render_template('index.html')

if name == 'main':
    app.run(debug=True)

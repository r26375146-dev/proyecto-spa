from flask import Flask, render_template

app = Flask(__name__)

# Esta ruta principal ("/") cargará tu archivo HTML
@app.route('/')
def inicio():
    return render_template('index.html')

if __name__ == '__main__':
    # El modo debug te ayuda a ver los cambios sin reiniciar el servidor
    app.run(debug=True)
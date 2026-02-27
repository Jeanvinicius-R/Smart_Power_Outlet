from flask import Flask, render_template, jsonify
from services.tuya_service import ligar, desligar, get_status

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ligar', methods=['POST'])
def rota_ligar():
    resultado = ligar()
    return jsonify(resultado)

@app.route('/api/desligar', methods=['POST'])
def rota_desligar():
    resultado = desligar()
    return jsonify(resultado)

@app.route('/api/status', methods=['GET'])
def rota_status():
    resultado = get_status()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
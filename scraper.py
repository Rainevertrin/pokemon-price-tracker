from flask import Flask, jsonify
import os
from auth_gsheet import auth_gsheet

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running"})

@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Połącz z arkuszem
        client = auth_gsheet()
        # Tutaj logika pracy z arkuszem
        return jsonify({"status": "success", "data": "dane z arkusza"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

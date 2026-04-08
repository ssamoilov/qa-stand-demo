from flask import Flask, jsonify, request
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

@app.route('/health')
def health():
    return {"status": "ok", "timestamp": str(datetime.now())}

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, email FROM users ORDER BY id')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id',
        (data['name'], data['email'])
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": user_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
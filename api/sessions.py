from flask import request, jsonify
from .database import connection
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
import json
import re

def encrypt_message(message):
    key = b'secretbloxsecretbloxsecretblox12'
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    encrypted_data = json.dumps({'iv':iv, 'data':ct})
    return encrypted_data

def filter_session_id(session_id):
    return session_id


def validate_session():
    raw_session_id = request.form.get('sessionid', '')
    filtered_session_id = filter_session_id(raw_session_id)
    response_data = {}
    try:
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            delete_sql = "DELETE FROM session WHERE TIMESTAMPDIFF(MINUTE, created_at, NOW()) > 5"
            cursor.execute(delete_sql)
            connection.commit()
            if filtered_session_id:
                select_sql = "SELECT * FROM session WHERE session_id = %s AND TIMESTAMPDIFF(MINUTE, created_at, NOW()) <= 5"
                cursor.execute(select_sql, [filtered_session_id])
                result = cursor.fetchone()
                if result:
                    response_data = {"status": "Valid"}
                else:
                    response_data = {"status": "Expired"}
            else:
                response_data = {"status": "Expired"}
    except Exception as e:
        response_data = {"status": "Error", "message": str(e)}
    
    encrypted_response = encrypt_message(json.dumps(response_data))
    return jsonify({"secret-blox-data": encrypted_response})

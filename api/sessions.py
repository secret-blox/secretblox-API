import json, os
from flask import request, jsonify
from .database import connection
from .hashing.AES import AES
from dotenv import load_dotenv
import re

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'sb.env'))

def validate_session():
    encoded_session_id = request.form.get('sessionid', '').strip()
    if not re.match(r'^[A-Za-z0-9+/=]+$', encoded_session_id):
        encrypted_response = AES(json.dumps({"status": "Error", "message": "Invalid session ID"})).__str__()
        return jsonify({"secret-blox-data": encrypted_response})

    session_time = os.getenv('SECRET_BLOX_SESSION_TIME', '5')
    response_data = {}
    try:
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM session WHERE TIMESTAMPDIFF(MINUTE, created_at, NOW()) > %s", [session_time])
            connection.commit()

            if encoded_session_id:
                cursor.execute("SELECT * FROM session WHERE session_id = %s AND TIMESTAMPDIFF(MINUTE, created_at, NOW()) <= %s", [encoded_session_id, session_time])
                result = cursor.fetchone()
                response_data = {"status": "Valid" if result else "Expired"}
            else:
                response_data = {"status": "Expired"}
    except Exception as e:
        response_data = {"status": "Error", "message": str(e)}
    
    encrypted_response = AES(json.dumps(response_data)).__str__()
    return jsonify({"secret-blox-data": encrypted_response})

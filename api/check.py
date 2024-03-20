import re
import os
import json
import time
from flask import request, jsonify
from .database import connection
from base64 import b64encode
from .hashing.AES import AES
from .discord.notfy import Notfy

def check_token():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT sb_update FROM info LIMIT 1")
            sb_update_result = cursor.fetchone()
            
            if sb_update_result['sb_update'] == "true":
                response = {"status": "no", "reason": "updating"}
                encrypted_response = AES(json.dumps(response)).__str__()
                return jsonify({"secret-blox-data": json.loads(encrypted_response)})
    except Exception as e:
        response = {"status": "no", "reason": "Error via SB DB"}
        encrypted_response = AES(json.dumps(response)).__str__()
        return jsonify({"secret-blox-data": json.loads(encrypted_response)})
    

    raw_token = request.form.get('token', '')
    token = re.sub(r'[^a-zA-Z0-9]', '', raw_token)
    if not token:
        response = {"status": "no", "reason": "No token"}
        encrypted_response = AES(json.dumps(response)).__str__()
        return jsonify({"secret-blox-data": json.loads(encrypted_response)})
    
    try:
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            sql = "SELECT * FROM clients WHERE `key` = %s"
            cursor.execute(sql, [token])
            result = cursor.fetchone()
            if not result:
                response = {"status": "no", "reason": "Invalid token"}
                encrypted_response = AES(json.dumps(response)).__str__()
                return jsonify({"secret-blox-data": json.loads(encrypted_response)})
            
            session_id = b64encode((f"{token}-{int(time.time())}-{os.urandom(10).hex()}").encode()).decode()
            insert_sql = "INSERT INTO session (session_id, client_key) VALUES (%s, %s)"
            cursor.execute(insert_sql, [session_id, token])
            connection.commit()
            response = {"status": "ok", "sessionid": session_id}
            Notfy(f"Session ID: `{session_id}`\nClient Token: `{token}`")
    except Exception as e:
        response = {"status": "no", "reason": str(e)}
    
    aes_instance = AES(json.dumps(response))
    encrypted_response = aes_instance.__str__()
    return jsonify({"secret-blox-data": json.loads(encrypted_response)})


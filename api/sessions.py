import json, os
from flask import request, jsonify
from .database import connection
from .hashing.AES import AES
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'sb.env'))

def validate_session():
    session_id = request.form.get('sessionid', '').strip()
    session_time = os.getenv('SECRET_BLOX_SESSION_TIME', '5')
    response_data = {}
    try:
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:

            cursor.execute(f"DELETE FROM session WHERE TIMESTAMPDIFF(MINUTE, created_at, NOW()) > {session_time}")
            connection.commit()

            if session_id:
                cursor.execute(f"SELECT * FROM session WHERE session_id = %s AND TIMESTAMPDIFF(MINUTE, created_at, NOW()) <= {session_time}", [session_id])
                result = cursor.fetchone()
                response_data = {"status": "Valid" if result else "Expired"}
            else:
                response_data = {"status": "Expired"}
    except Exception as e:
        response_data = {"status": "Error", "message": str(e)}
    
    encrypted_response = AES(json.dumps(response_data)).__str__()
    return jsonify({"secret-blox-data": encrypted_response})

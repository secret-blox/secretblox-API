# function for our clients as they check the active user count
import re

from flask import request, jsonify
from .database import connection

def sanitize_token(raw_token):
    return re.sub(r'[^a-zA-Z0-9]', '', raw_token)

def get_session_count(token):
    sanitized_token = sanitize_token(token)
    try:
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:

            sql = "SELECT COUNT(*) AS session_count FROM session WHERE client_key = %s"
            cursor.execute(sql, [sanitized_token])
            result = cursor.fetchone()
            if result:
                return result['session_count']
            else:
                return 0
    except Exception as e:
        print(f"Error getting session count: {e}")
        return 0
    

def get_active_user_count():
    token = request.args.get('token', None)
    if not token:
        return jsonify({"error": "Token is required"}), 400
    return jsonify({"active_sessions": get_session_count(token)})

    

# Removed the code that was causing the RuntimeError due to working outside of request context.
# The functionality to get the token and respond should be moved to a route handler in the Flask app.


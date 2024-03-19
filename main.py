from flask import Flask, request, jsonify
import threading, os
import time
from api.database import connection
from api.check import check_token
from api.sessions import validate_session
from api.version import secret_blox_bootstrapper
from api.user_cout import get_active_user_count
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'sb.env'))

session_time = os.getenv('SECRET_BLOX_SESSION_TIME', '5')


limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"],
    headers_enabled=True,
    key_prefix="limiter:",
    strategy="fixed-window",
    storage_uri="memory://",
    swallow_errors=True,
    in_memory_fallback_enabled=True,
    on_breach=lambda *args, **kwargs: jsonify({"status": "no", "reason": "ratelimited"}),
)

def cleanup_sessions():
    while True:
        try:
            connection.ping(reconnect=True)
            with connection.cursor() as cursor:
                delete_sql = f"DELETE FROM session WHERE TIMESTAMPDIFF(MINUTE, created_at, NOW()) > {session_time}"
                cursor.execute(delete_sql)
                connection.commit()
               
        except Exception as e:
            print(f"Error cleaning up sessions: {e}")
        time.sleep(30)

cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
cleanup_thread.start()

@app.route('/version', methods=['GET'])
@limiter.limit("10 per minute")
def get_sb_version():
    return secret_blox_bootstrapper()

@app.route('/total_active', methods=['GET'])
@limiter.limit("20 per minute")
def get_total_active_users():
    return get_active_user_count()

@app.route('/session', methods=["POST", "GET"])
@limiter.limit("100 per minute")
def check_session():
    if request.method == 'GET':
        return "<h1>Not Found </h1> The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.", 404
    
    return validate_session()

@app.route('/check', methods=['POST', 'GET'])
@limiter.limit("100 per minute")
def check():
    if request.method == 'GET':
        return "<h1>Not Found </h1> The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.", 404
    
    user_agent = request.headers.get('User-Agent')
    if user_agent == 'secretblox':
        return check_token()
    else:
        return jsonify({"status": "no", "reason": "Something went wrong"}), 403

if __name__ == '__main__':
    app.run(debug=True)


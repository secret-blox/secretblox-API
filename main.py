from flask import Flask, request, jsonify
import threading, os
import time
from api.database import connection
from api.check import check_token
from api.sessions import validate_session
from api.version import secret_blox_bootstrapper
from api.user_cout import get_active_user_count
from api.discord.roblox import compare_and_notify_client_version_upload
from api.admin.controller import update_version, update_sb_branch, update_sb_update_status
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv


app = Flask(__name__)

def load_environment_variables():
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'sb.env'))

load_environment_variables()

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
    on_breach=lambda *args, **kwargs: jsonify({"status": "no", "reason": "please wait a little before trying to access this endpoint again [ratelimited]"}),
)


def cleanup_sessions():
    while True:
        try:
            load_environment_variables()
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

roblox_update_thread = threading.Thread(target=compare_and_notify_client_version_upload, daemon=True)
roblox_update_thread.start()

@app.route('/version', methods=['GET'])
@limiter.limit("10 per minute")
def get_sb_version():
    
    load_environment_variables() 
    print(os.getenv('SECRET_BLOX_FORCE_UPDATE'))
    response = secret_blox_bootstrapper()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0'
    return response

@app.route('/total_active', methods=['GET'])
@limiter.limit("20 per minute")
def get_total_active_users():
    return get_active_user_count()

@app.route('sb_control/edit/update', methods=['GET'])
def admin_controler_updating():
    return update_sb_update_status()

@app.route('/sb_control/edit/version', methods=['GET'])
def admin_controller_version():
    return update_version()

@app.route('sb_control/edit/branch', methods=['GET'])
def admin_controller_branch():
    return update_sb_branch()

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


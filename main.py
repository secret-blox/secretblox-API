from flask import Flask, request, jsonify
app = Flask(__name__)
from api.check import check_token
from api.sessions import validate_session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "100 per hour"],
    default_limits_exempt_when=lambda: False,
    headers_enabled=True,
    key_prefix="limiter:",
    strategy="fixed-window",
    storage_uri="memory://",
    application_limits=["1000 per day", "100 per hour"],
    swallow_errors=True,
    in_memory_fallback_enabled=True,
    on_breach=lambda *args, **kwargs: jsonify({"status": "no", "reason": "ratelimited"}),
)


@app.route('/version', methods=['GET'])
def get_sb_version():
    return jsonify({"version": 1.0, "client": "Secretblox_main"}) # Probs gonna need to read from a file for this etc


@app.route('/total_active', methods=['GET'])
def get_total_active_users():
    return '0'


@app.route('/session', methods=["POST"])
def check_session():
    return validate_session()


@app.route('/check', methods=['POST'])
def check():
    user_agent = request.headers.get('User-Agent')
    if user_agent == 'secretblox':
        return check_token()
    else:
        return jsonify({"status": "no", "reason": "Something went wrong"}), 403
if __name__ == '__main__':
    app.run(debug=True)



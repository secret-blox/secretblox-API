from flask import jsonify
from .database import connection

def secret_blox_bootstrapper():
    try:
        connection.ping(reconnect=True)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM info")
            result = cursor.fetchone()
            if result:
                sb_version = result.get('sb_version', "None")
                sb_branch = result.get('sb_branch', "None")
                sb_update = result.get('sb_update', "None")
            else:
                sb_version = "None"
                sb_branch = "None"
                sb_update = "None"
    except Exception as e:
        print(f"Error fetching version info: {e}")
        sb_version = "Error"
        sb_branch = "Error"
        sb_update = "Error"
    
    return jsonify({"version": sb_version, "branch": sb_branch, "updating": sb_update})

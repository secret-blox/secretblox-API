from flask import request, jsonify
import requests
from .database import connection
import re, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
import json
import datetime
import time

def encrypt_message(message):
    key = b'secretbloxsecretbloxsecretblox12'
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    encrypted_data = json.dumps({'iv':iv, 'data':ct})
    return encrypted_data

def check_token():
    raw_token = request.form.get('token', '')
    token = re.sub(r'[^a-zA-Z0-9]', '', raw_token)
    if token:
        try:
            connection.ping(reconnect=True) 
            with connection.cursor() as cursor:
                sql = "SELECT * FROM clients WHERE `key` = %s"
                cursor.execute(sql, [token])  
                result = cursor.fetchone()
                if result:
                    session_id = b64encode((token + "-" + str(int(time.time())) + "-" + os.urandom(10).hex()).encode()).decode()
                    insert_sql = "INSERT INTO session (session_id, client_key) VALUES (%s, %s)"
                    cursor.execute(insert_sql, [session_id, token])  
                    connection.commit()
                    response = {"status": "ok", "sessionid": session_id}
                    notify_endpoint(f"Session ID: `{session_id}`\nClient Token: `{token}`")
                else:
                    response = {"status": "no", "reason": "Invalid token"}
        except Exception as e:
            response = {"status": "no", "reason": str(e)}
    else:
        response = {"status": "no", "reason": "No token"}
    
    encrypted_response = encrypt_message(json.dumps(response))
    return jsonify({"secret-blox-data": encrypted_response})



def notify_endpoint(session):
    discord_endpoint = "https://discord.com/api/webhooks/1219045348891430972/an8H19iGEk7l5_o2h12nT_db-Ti1HJO-sKw8DK8o9KNSQ5RnfAHT_Tf_Rf-4WmSMW-1A"
    headers = {"Content-Type": "application/json"}
    data = {
        "embeds": [
            {
                "description": session,
                "color": 3447003,  
                "footer": {
                        "text": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                }
            ]
        }
    response = requests.post(discord_endpoint, json=data, headers=headers)

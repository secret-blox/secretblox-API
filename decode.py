import requests
from Crypto.Cipher import AES
from base64 import b64decode
import json
from Crypto.Util.Padding import unpad

def decrypt_message(encrypted_message):
    key = b'secretbloxsecretbloxsecretblox12'
    try:
        encrypted_data = encrypted_message['secret-blox-data']
        encrypted_data = json.loads(encrypted_data) if isinstance(encrypted_data, str) else encrypted_data
        iv, ct = b64decode(encrypted_data['iv']), b64decode(encrypted_data['data'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        return json.loads(pt) if pt.strip().startswith('{') else pt
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        print(e)
        return None

def get_encrypted_message():
    headers = {'User-Agent': 'secretblox'}
    response = requests.post("http://127.0.0.1:5000/check", headers=headers, data={'token': 'test'})
    return response.json() if response.status_code == 200 else "Failed"

def process_decrypted_message(decrypted_message):
    if isinstance(decrypted_message, dict) and "sessionid" in decrypted_message:
        print(decrypted_message)
        session_response = requests.post("http://127.0.0.1:5000/session", data={'sessionid': decrypted_message["sessionid"]})
        session_response_data = json.loads(session_response.text)
        if 'secret-blox-data' in session_response_data:
            session_data = decrypt_message({'secret-blox-data': session_response_data['secret-blox-data']})
            print(session_data)
    else:
        print(decrypted_message if isinstance(decrypted_message, str) else json.dumps(decrypted_message))

encrypted_message = get_encrypted_message()
if encrypted_message != "Failed":
    decrypted_message = decrypt_message(encrypted_message)
    process_decrypted_message(decrypted_message)
else:
    print(encrypted_message)

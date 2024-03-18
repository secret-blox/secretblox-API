import requests
from Crypto.Cipher import AES
from base64 import b64decode
import json
def decrypt_message(encrypted_message):
    key = b'secretbloxsecretbloxsecretblox12'
    try:
        encrypted_message_dict = json.loads(encrypted_message)
        encrypted_data_str = encrypted_message_dict['secret-blox-data']
        encrypted_data_dict = json.loads(encrypted_data_str)
        iv = b64decode(encrypted_data_dict['iv'])
        ct = b64decode(encrypted_data_dict['data'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = cipher.decrypt(ct)
        from Crypto.Util.Padding import unpad
        pt = unpad(pt, AES.block_size)
        cleaned_pt = pt.decode('utf-8')
        try:
            return json.loads(cleaned_pt)
        except json.JSONDecodeError:
            return cleaned_pt
    except (ValueError, KeyError) as e:
        print(e)
def get_encrypted_message():
    headers = {'User-Agent': 'secretblox'}
    response = requests.post("http://127.0.0.1:5000/check", headers=headers, data={'token': 'test'})
   
    if response.status_code == 200:
        encrypted_message = response.json()
        return encrypted_message
encrypted_message = get_encrypted_message()
if encrypted_message != "Failed":
    decrypted_message = decrypt_message(json.dumps(encrypted_message))
    if isinstance(decrypted_message, dict):
        if "sessionid" in decrypted_message:
            print(decrypted_message["sessionid"])
            session_response = requests.post("http://127.0.0.1:5000/session", data={'sessionid': decrypted_message["sessionid"]})
            decrypted_session_response = decrypt_message(session_response.text)
            print(decrypted_session_response)
    else:
        try:
            decrypted_message_dict = json.loads(decrypted_message)
            print(decrypted_message_dict)
       

        except json.JSONDecodeError:
            print(decrypted_message)
else:
    print(encrypted_message)

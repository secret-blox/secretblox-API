import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'sb.env'))
roblox_update_notfy_url = os.getenv('SB_ROBLOX_UPDATE_NOTFY')

def fetch_roblox_client_version_upload():
    url = "https://clientsettingscdn.roblox.com/v2/client-version/WindowsPlayer/channel/LIVE"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['clientVersionUpload']
    else:
        return None

def send_discord_webhook(message):
    data = {
        "embeds": [{
            "title": "Roblox Client Version Update",
            "description": message,
            "color": 16711680
        }]
    }
    response = requests.post(roblox_update_notfy_url, json=data)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification.")

def save_previous_version(version):
    with open("previous_client_version_upload.txt", "w") as file:
        file.write(version)

def read_previous_version():
    try:
        with open("previous_client_version_upload.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None

def compare_and_notify_client_version_upload():
    previous_client_version_upload = read_previous_version()
    while True:
        current_client_version_upload = fetch_roblox_client_version_upload()
        if current_client_version_upload and current_client_version_upload != previous_client_version_upload:
            if previous_client_version_upload is not None: 
                message = f"[**LIVE**] `{previous_client_version_upload}` ➜ `{current_client_version_upload}`"
                send_discord_webhook(message)
            previous_client_version_upload = current_client_version_upload
            save_previous_version(current_client_version_upload)
        time.sleep(60)  






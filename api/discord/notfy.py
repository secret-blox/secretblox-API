import requests, os
import datetime
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', 'sb.env'))


class Notfy:
    def __init__(self, session) -> None:
        discord_endpoint = os.getenv('SB_DISCORD_NOTFY').encode()
        headers = {"Content-Type": "application/json"}
        data = {
            "embeds": [
                {
                    "title": "SecretBlox API",
                    "description": session,
                    "color": 16711680,  
                    "footer": {
                            "text": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                ]
            }
        response = requests.post(discord_endpoint, json=data, headers=headers)

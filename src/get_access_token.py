from dotenv import load_dotenv
import os
import base64
import requests

load_dotenv()

def get_base64_value(s):
    b64_bytes_encoded=base64.b64encode(s.encode())
    b64_string=b64_bytes_encoded.decode()
    return b64_string

def get_access_token():
    token_url="https://accounts.spotify.com/api/token"
    payload={
        "grant_type":"client_credentials"
    }
    headers={
        "Authorization":f"Basic {get_base64_value(os.environ.get('client_id')+':'+os.environ.get('client_secret'))}",
        "Content-Type":"application/x-www-form-urlencoded"
        
    }

    response=requests.post(token_url,headers=headers,data=payload).json()
    return response


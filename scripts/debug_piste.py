import requests
import os
from dotenv import load_dotenv
import base64

# Charger .env
load_dotenv()

CLIENT_ID = os.getenv("LEGIFRANCE_CLIENT_ID")
CLIENT_SECRET = os.getenv("LEGIFRANCE_CLIENT_SECRET")
TOKEN_URL = "https://oauth.piste.gouv.fr/api/oauth/token"

print(f"🔹 Client ID: {CLIENT_ID}")
print(f"🔹 Client Secret: {CLIENT_SECRET[:4]}...{CLIENT_SECRET[-4:]} (masqué)")

def test_auth_header():
    print("\n🚀 TEST 1: Basic Auth Header")
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "scope": "openid"
    }
    
    try:
        resp = requests.post(TOKEN_URL, headers=headers, data=data)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_auth_body():
    print("\n🚀 TEST 2: Credentials in Body")
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "openid"
    }
    
    try:
        resp = requests.post(TOKEN_URL, data=data)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if not CLIENT_ID or not CLIENT_SECRET:
        print("❌ Erreur: Identifiants manquants dans .env")
    else:
        test_auth_header()
        test_auth_body()

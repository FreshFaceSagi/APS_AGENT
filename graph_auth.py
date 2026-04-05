import requests
from config import TENANT_ID, CLIENT_ID, CLIENT_SECRET, GRAPH_SCOPE

_token_cache = {"access_token": None, "expires_in": 0}

def get_graph_token():
    # Simple client_credentials flow; in prod add caching with expiry
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": GRAPH_SCOPE,
        "grant_type": "client_credentials",
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    token = resp.json()["access_token"]
    _token_cache["access_token"] = token
    return token

def graph_headers():
    return {
        "Authorization": f"Bearer {get_graph_token()}",
        "Content-Type": "application/json",
    }
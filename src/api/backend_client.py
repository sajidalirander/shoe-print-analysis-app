import requests


API_BASE = "http://127.0.0.1:8000/api"

def get_probe_files():
    try:
        response = requests.get(f"{API_BASE}/shoeprints")
        return response.json().get("files", [])
    except Exception as e:
        print(f"[ERROR] Could not fetch probe list: {e}")
        return []

def get_match_results(filename):
    try:
        response = requests.get(f"{API_BASE}/match/{filename}")
        return response.json().get("top_matches", [])
    except Exception as e:
        print(f"[ERROR] Failed to get matches: {e}")
        return []

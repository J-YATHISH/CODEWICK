import requests

def has_internet(url="https://www.google.com", timeout=3):
    try:
        response = requests.get(url, timeout=timeout)
        return True
    except requests.RequestException:
        return False
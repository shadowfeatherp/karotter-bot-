import requests

r = requests.get("https://karotter.com")
print(r.status_code)

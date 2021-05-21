import requests

payload = {
    "first_name": "Afjal"
}

print(requests.request("POST", "http://127.0.0.1:5000/addClient", headers=None, data=payload,
                       verify=False).text)

import requests

response = requests.post("http://127.0.0.1:8000/predict", json={"text": ["I am quite happy today", "I am quite sad today"]}, verify=False)
print(f"Status: {response.status_code}\nResponse:\n {response.text}")
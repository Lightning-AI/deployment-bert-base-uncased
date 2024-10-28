from lightning_sdk.deployment import Deployment

deployment = Deployment(name="[DEPLOYMENT_NAME]")
resp = deployment.post("/predict", json={"text": ["I am quite happy today", "I am quite sad today"]})
print(resp.text)
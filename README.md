# deployment-bert-base-uncased

## Structure

### Open Models

End-to-end example on how to deploy bert-base-uncased on Lightning.AI

```python
# open_models/server.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from litserve import LitAPI, LitServer
from lightning_sdk import Teamspace

class BERTLitAPI(LitAPI):
    def setup(self, device):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
        self.model.to(device).eval()

    def decode_request(self, request):
        return self.tokenizer(request["text"], return_tensors="pt", padding=True, truncation=True, max_length=512)

    def predict(self, inputs):
        with torch.no_grad():
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            outputs = self.model(**inputs)
        return outputs.logits

    def encode_response(self, logits):
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        responses = {i: "negative" if v < 0.5 else "positive" for i, v in enumerate(probabilities[0, :].tolist())}
        return responses

if __name__ == "__main__":
    api = BERTLitAPI()
    server = LitServer(api, accelerator='auto', devices='auto', workers_per_device=2)
    server.run(port=8000)
```

The script `open_models/bash.sh` builds and push a docker image to ECR ready to use in Deployments. 

###  Private Models

End-to-end example on how to deploy bert-base-uncased on Lightning.AI where the weights are stored on Lightning.AI

```python
# private_models/upload.py
import os

folder = "./cache"
os.environ["HF_HUB_CACHE"] = folder

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from lightning_sdk import Teamspace

model_name = "bert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

from lightning_sdk import Teamspace

Teamspace().upload_model(folder, name=model_name)
```

This shows how to persist an hugging face model to Lightning.AI platform

```diff
index e60f1a9..9dd02c2 100755
-      
+      from lightning_sdk import Teamspace
 
 class BERTLitAPI(LitAPI):
     def setup(self, device):
+       Teamspace().download_model("bert-base-uncased", download_dir=".")
+        path = "./cache/models--bert-base-uncased/snapshots/86b5e0934494bd15c9632b12f734a8a67f723594"
+
+        self.tokenizer = AutoTokenizer.from_pretrained(path)
+        self.model = AutoModelForSequenceClassification.from_pretrained(path)
-        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
-        self.model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
         self.model.to(device).eval()
 
     def decode_request(self, request):
```
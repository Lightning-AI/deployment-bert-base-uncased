from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from litserve import LitAPI, LitServer
from lightning_sdk import Teamspace

class BERTLitAPI(LitAPI):
    def setup(self, device):
        Teamspace().download_model("bert-base-uncased", download_dir=".")
        path = "./cache/models--bert-base-uncased/snapshots/86b5e0934494bd15c9632b12f734a8a67f723594"

        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.model = AutoModelForSequenceClassification.from_pretrained(path)
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
  
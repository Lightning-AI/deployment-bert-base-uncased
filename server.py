from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from litserve import LitAPI, LitServer

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
  
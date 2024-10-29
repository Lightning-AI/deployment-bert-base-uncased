import os

folder = "./cache"
os.environ["HF_HUB_CACHE"] = folder

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from lightning_sdk import Teamspace

Teamspace().download_model("bert-base-uncased", download_dir=folder)
path = "./cache/models--bert-base-uncased/snapshots/86b5e0934494bd15c9632b12f734a8a67f723594"

tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(path, local_files_only=True)

text = "I am very happy"
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)
print(output)
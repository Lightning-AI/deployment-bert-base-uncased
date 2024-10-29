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
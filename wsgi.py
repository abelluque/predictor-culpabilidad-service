from flask import Flask, request
from transformers import AutoTokenizer
import requests
import logging
import json
import torch
import math
import os
import sys



# Model config
pretrained_model = "distilbert-base-uncased"
infer_url = "https://predictor-culpabilidad-predictor-culpabilidad.apps.cluster-pool-gcp-rgmtb.ocp.gcplasegunda.com.ar/v2/models/predictor-culpabilidad/infer"
id2label = {'0': 'DEL ASEGURADO', '1': 'DEL TERCERO', '2': 'DUDOSA', '3': 'NO SE EVALUA'}



application = Flask(__name__)

@application.route('/', methods=['POST'])
def webhook():
    # Tomamos el request
    print("request completo: ")
    print(request.data)
    data = json.loads(request.data)
    print("request json: ")
    print(data)

    # Tomamos el node "text"
    text = data['text']
  


    # Set model tokenizer
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model)
    inputs = tokenizer(text, return_tensors="pt")

    body = payload(inputs)

    # Call the model from endpoint
    response = requests.post(infer_url, json=body, verify=False)
    response = response.json()

    print('Respose')
    print(response)

    # Convert response to prediction
    raw_logits = torch.tensor(response["outputs"][0]["data"])
    probs = raw_logits.softmax(dim=0)
    label_idx = torch.argmax(probs).item()
    score = math.trunc(probs[probs.argmax(dim=0)].item() * 100)

    return {"label": id2label[str(label_idx)], "score": score}
    
def payload( tquery):
        
        ids = tquery.input_ids
        print('IDS')
        print(ids)
        am = tquery.attention_mask
        print('AM')
        print(am)
        body = {
            "inputs": [
                {
                    "name": "input_ids",
                    "shape": list(ids.shape),
                    "datatype": "INT64",
                    "data": ids.tolist(),
                },
                {
                    "name": "attention_mask",
                    "shape": list(am.shape),
                    "datatype": "INT64",
                    "data": am.tolist(),
                },
            ]
        }
        return body

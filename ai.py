import requests

def ask_ai(question):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"

    headers = {
        "Authorization": "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"
    }

    payload = {
        "inputs": question
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json()[0]["generated_text"]
    except:
        return "AI غير متاح حالياً"

def summarize_text(text):
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    headers = {
        "Authorization": "Bearer YOUR_HF_TOKEN"
    }

    payload = {
        "inputs": text[:4000]
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        return res.json()[0]["summary_text"]
    except:
        return "فشل التلخيص"

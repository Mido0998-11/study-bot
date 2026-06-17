import requests
import os

# 🔑 خذ التوكن من Environment Variables (Render / GitHub / etc)
HF_TOKEN = os.environ.get("HF_TOKEN")

# ================== AI ANSWER ==================
def ask_ai(question):
    url = "https://api-inference.huggingface.co/models/google/flan-t5-base"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": f"اشرح هذا بطريقة بسيطة للطلاب: {question}"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        data = response.json()

        # في بعض الحالات يرجع dict فيه error
        if isinstance(data, dict) and "error" in data:
            return f"❌ خطأ: {data['error']}"

        return data[0]["generated_text"]

    except Exception as e:
        return f"❌ AI غير متاح حالياً: {str(e)}"


# ================== SUMMARIZE PDF ==================
def summarize_text(text):
    url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    payload = {
        "inputs": text[:4000]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        data = response.json()

        if isinstance(data, dict) and "error" in data:
            return f"❌ خطأ: {data['error']}"

        return data[0]["summary_text"]

    except Exception as e:
        return f"❌ فشل التلخيص: {str(e)}"

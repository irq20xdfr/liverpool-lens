import os
import base64
import requests
import whisper

from utils.logging_utils import log_error

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def convert_image_to_text(image_path):
    text = ""
    try:
        base64_image = encode_image(image_path)

        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "Regresa una descripción de la imagen, para ser usada en un campo de búsqueda en una tienda en línea."
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        res_j = response.json()
        text = res_j["choices"][0]["message"]["content"]
    except Exception as e:
        log_error(e)

    return text


def convert_audio_to_text(audio_path):
    text = ""
    try:
        model = whisper.load_model("turbo")
        result = model.transcribe(audio_path)
        text = result["text"]
    except Exception as e:
        log_error(e)

    return text

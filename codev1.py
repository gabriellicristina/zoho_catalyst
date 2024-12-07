import openai
import json
import requests

def transcribe_audio(request):
    # Definir a chave da API da OpenAI
    openai.api_key = "SUA_CHAVE_API_OPENAI"

    # Obter o áudio do corpo da requisição
    audio_file = request.files['audio']

    try:
        # Transcrição com Whisper
        transcription = openai.Audio.transcribe("whisper-1", audio_file)

        # Enviar a transcrição para o Langflow
        langflow_response = send_to_langflow(transcription["text"])

        # Retornar a resposta do Langflow
        return {
            "status": 200,
            "body": json.dumps({
                "transcription": transcription["text"],
                "langflow_response": langflow_response
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    except Exception as e:
        return {
            "status": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

def send_to_langflow(transcription):
    # API do Langflow
    langflow_api_url = "URL_DO_LANGFLOW"
    payload = {"input_text": transcription}
    headers = {"Content-Type": "application/json"}

    # Enviar a transcrição para Langflow
    response = requests.post(langflow_api_url, json=payload, headers=headers)
    return response.json()

import openai
import requests
from zoho.catalyst import function
from flask import jsonify

# Defina a chave de API da OpenAI para transcrição
openai.api_key = "SUA_CHAVE_OPENAI"

# Função para transcrição de áudio usando Whisper
def transcribe_audio(request):
    if 'audio' not in request.files:
        return jsonify({"error": "Arquivo de áudio não encontrado"}), 400

    audio_file = request.files['audio']

    try:
        # Transcrevendo o áudio com Whisper
        transcription = openai.Audio.transcribe("whisper-1", audio_file)

        # Enviar a transcrição para o Langflow
        langflow_response = send_to_langflow(transcription["text"])

        # Retornar a resposta processada
        return jsonify({"transcription": transcription["text"], "langflow_output": langflow_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def send_to_langflow(transcription):
    langflow_api_url = "URL_DO_LANGFLOW"
    payload = {"input_text": transcription}
    headers = {"Content-Type": "application/json"}

    response = requests.post(langflow_api_url, json=payload, headers=headers)
    return response.json()

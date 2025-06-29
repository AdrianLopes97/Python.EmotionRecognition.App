import cv2
import requests
from deepface import DeepFace
import os
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
EMOCOES_NEGATIVAS = ["sad" , "fear" , "angry"]
TRADUCAO_EMOCOES = {
    "sad": "Tristeza",
    "angry": "Raiva",
    "disgust": "Nojo",
    "fear": "Medo",
    "happy": "Felicidade",
    "surprise": "Surpresa",
    "neutral": "Neutro"
}

def enviar_alerta_slack(emocao):
    mensagem = f":rotating_light: Alerta de Emoção Negativa Detectada: *{emocao.upper()}* em uma criança!"
    payload = {"text": mensagem}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
        print("Alerta enviado para o Slack!")
    except Exception as e:
        print("Erro ao enviar alerta para o Slack:", e)

def analisar_emocao_imagem(caminho):
    if not os.path.exists(caminho):
        print("Arquivo não encontrado.")
        return

    try:
        resultado = DeepFace.analyze(img_path=caminho, actions=['emotion'], enforce_detection=False)
        emocao = resultado[0]['dominant_emotion']
        emocao_traduzida = TRADUCAO_EMOCOES.get(emocao, emocao)
        print(f"Emoção detectada: {emocao_traduzida}")

        if emocao in EMOCOES_NEGATIVAS:
            enviar_alerta_slack(emocao_traduzida)

    except Exception as e:
        print("Erro na análise:", e)

def menu():
    print("Reconhecimento de Emoções")
    caminho = input("Digite o caminho da imagem: ")
    analisar_emocao_imagem(caminho)

if __name__ == "__main__":
    while True:
        menu()
        continuar = input("Deseja analisar outra imagem? (s/n): ").lower()
        if continuar != 's':
            print("Encerrando o programa.")
            break
        print("-" * 30)

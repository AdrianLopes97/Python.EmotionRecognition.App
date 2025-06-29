import cv2
import requests
from deepface import DeepFace
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações Globais ---
# URL do webhook do Slack para enviar os alertas. Carregada do arquivo .env.
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# Lista de emoções consideradas negativas para acionar o alerta.
EMOCOES_NEGATIVAS = ["sad" , "fear" , "angry"]

# Dicionário para traduzir as emoções retornadas pela API para o português.
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
    """Envia uma mensagem de alerta para o Slack.

    Args:
        emocao (str): A emoção detectada (já traduzida) para incluir na mensagem.
    """
    # Verifica se a URL do webhook está configurada antes de tentar enviar
    if not SLACK_WEBHOOK_URL:
        print("Erro: A variável de ambiente SLACK_WEBHOOK_URL não está configurada.")
        return

    mensagem = f":rotating_light: Alerta de Emoção Negativa Detectada: *{emocao.upper()}* em uma criança!"
    payload = {"text": mensagem}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
        print("Alerta enviado para o Slack!")
    except Exception as e:
        print("Erro ao enviar alerta para o Slack:", e)

def analisar_emocao_imagem(caminho):
    """Analisa uma imagem para detectar a emoção facial predominante.

    Utiliza a biblioteca DeepFace para a análise. Se uma emoção negativa for
    detectada, aciona a função de alerta para o Slack.

    Args:
        caminho (str): O caminho do arquivo da imagem a ser analisada.
    """
    # Verifica se o arquivo de imagem realmente existe antes de prosseguir
    if not os.path.exists(caminho):
        print("Arquivo não encontrado.")
        return

    try:
        resultado = DeepFace.analyze(img_path=caminho, actions=['emotion'], enforce_detection=False)
        emocao = resultado[0]['dominant_emotion']
        # Traduz a emoção para português para exibição e para o alerta
        emocao_traduzida = TRADUCAO_EMOCOES.get(emocao, emocao)
        print(f"Emoção detectada: {emocao_traduzida}")

        # Se a emoção original (em inglês) estiver na lista de negativas, envia o alerta
        if emocao in EMOCOES_NEGATIVAS:
            enviar_alerta_slack(emocao_traduzida)

    except Exception as e:
        print(f"Erro na análise da imagem: {e}")

def menu():
    """Exibe o menu principal e solicita a entrada do usuário.

    Pede o caminho da imagem e chama a função de análise.
    """
    print("\n--- Reconhecimento de Emoções ---")
    caminho = input("Digite o caminho da imagem: ")
    analisar_emocao_imagem(caminho)

# Bloco de execução principal
if __name__ == "__main__":
    # Loop infinito para permitir que o usuário analise várias imagens
    while True:
        menu()
        # Pergunta ao usuário se deseja continuar após cada análise
        continuar = input("Deseja analisar outra imagem? (s/n): ").lower()
        if continuar != 's':
            print("Encerrando o programa.")
            break
        print("-" * 30)

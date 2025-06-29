# Reconhecimento de Emoções em Crianças

Este projeto utiliza a biblioteca `deepface` para analisar imagens de crianças e detectar suas emoções. Caso uma emoção negativa (como tristeza, raiva ou medo) seja identificada, um alerta é enviado para um canal específico no Slack.

## Funcionalidades

- Análise de emoções a partir de arquivos de imagem.
- Tradução das emoções detectadas para o português.
- Envio de alertas para o Slack quando emoções negativas são detectadas.
- Loop de execução que permite analisar múltiplas imagens sem reiniciar o script.

## Pré-requisitos

- Python 3.11

## Configuração do Ambiente

1.  **Abra o PowerShell** na pasta raiz do projeto.

2.  **Execute o comando para instalar as dependencias**:

    ```powershell
    pip install -r requirements.txt
    ```

## Como Executar o Projeto

1.  **Execute o script principal**:

    ```powershell
    python main.py
    ```

2.  O programa solicitará que você **digite o caminho para a imagem** que deseja analisar.

3.  Após a análise, o programa perguntará se você deseja **analisar outra imagem**. Digite `s` para continuar ou qualquer outra tecla para sair.

## Estrutura do Projeto

- `main.py`: O script principal que contém toda a lógica da aplicação.
- `requirements.txt`: Lista de todas as dependências Python do projeto.
- `images/`: Pasta para armazenar imagens para análise (ex: `images/sad/`).

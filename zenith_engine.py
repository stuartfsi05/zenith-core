"""
Módulo Principal do Zenith-Core (O Motor)

Este arquivo define a lógica central para interagir com a API do Gemini,
carregando as instruções de sistema e os prompts do módulo 'prompts.py'.

Ele é projetado para ser importado por outros scripts (como o main.py).
"""

import os
import google.generativeai as genai
from google.genai import types
from dotenv import load_dotenv

# --- 1. Importação dos Prompts ---
# Importa as constantes de string do arquivo prompts.py
from prompts import ZENITH_SYSTEM_INSTRUCTION, RAG_USER_PROMPT

# --- 2. Configuração ---

# Carrega variáveis de ambiente do arquivo .env (ex: GOOGLE_API_KEY)
load_dotenv()

# Configura a API key do Google a partir da variável de ambiente
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# --- 3. Lógica Principal da Aplicação ---

def generate():
    """
    Configura e executa uma chamada para a API Generativa do Google.
    
    Esta função inicializa o modelo generativo com as instruções de sistema
    e a configuração de temperatura, e então chama o modelo com o 
    prompt do usuário (que inclui o RAG manual).
    """
    
    try:
        # 1. Configura a geração de configuração (temperatura)
        generation_config = genai.GenerationConfig(
            temperature=0
        )

        # 2. Inicializa o Modelo Generativo com o nome do modelo,
        #    as instruções de sistema (Zenith) e a config de geração.
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            system_instruction=ZENITH_SYSTEM_INSTRUCTION,
            generation_config=generation_config
        )

        # 3. Monta o payload de 'contents' com o prompt do usuário (que inclui o RAG)
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=RAG_USER_PROMPT),
                ],
            ),
        ]

        # 4. Executa a chamada da API (não-stream) e obtém a resposta
        print("--- Enviando solicitação para o Zenith (Fase 3 - Motor) ---")
        
        # Usamos generate_content em vez de stream para obter a resposta completa
        response = model.generate_content(
            contents=contents
        )

        # 5. Imprime a resposta completa
        print("--- Resposta do Zenith Recebida ---")
        print(response.text)

    except Exception as e:
        print(f"\n--- OCORREU UM ERRO DURANTE A EXECUÇÃO ---")
        print(f"Tipo do Erro: {type(e).__name__}")
        print(f"Mensagem: {e}")
    finally:
        print("\n--- Fim da Execução ---")
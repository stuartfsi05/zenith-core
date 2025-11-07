"""
Módulo Principal do Zenith-Core (O Motor)

Este arquivo define a lógica central para interagir com a API do Gemini.
Ele lê dinamicamente da 'knowledge_base' para construir prompts de RAG.
"""

# --- 1. Importações ---

# Bibliotecas padrão
import os

# Bibliotecas de terceiros
import google.generativeai as genai
from dotenv import load_dotenv

# Importações locais
from prompts import ZENITH_SYSTEM_INSTRUCTION

# --- 2. Configuração ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Constante para o caminho da base de conhecimento
KNOWLEDGE_BASE_PATH = "knowledge_base"


# --- 3. Funções Auxiliares (Lógica RAG) ---

def _load_knowledge_from_file(filepath):
    """Lê o conteúdo de um arquivo de texto da base de conhecimento."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"--- ERRO no Motor: Arquivo não encontrado: {filepath} ---")
        return None
    except Exception as e:
        print(f"--- ERRO no Motor: Falha ao ler o arquivo {filepath}: {e} ---")
        return None

def _find_relevant_knowledge(user_task):
    """
    Fase 4 (Início): O nosso primeiro "Buscador" (Retriever) simples.
    Ele decide qual arquivo ler com base em palavras-chave na tarefa.
    """
    print("--- [Motor] Buscador ativado. Analisando a tarefa...")
    
    # Converte a tarefa para minúsculas para busca
    task_lower = user_task.lower()
    
    # Lógica de busca simples (vamos torná-la inteligente depois)
    if "instrução negativa" in task_lower or "não mencione" in task_lower:
        print("--- [Motor] Conhecimento relevante encontrado: 'antipattern_instrucao_negativa.txt'")
        filepath = os.path.join(KNOWLEDGE_BASE_PATH, "antipattern_instrucao_negativa.txt")
        return _load_knowledge_from_file(filepath)
        
    elif "self-critique" in task_lower or "autocrítica" in task_lower:
        print("--- [Motor] Conhecimento relevante encontrado: 'tecnica_self_critique.txt'")
        filepath = os.path.join(KNOWLEDGE_BASE_PATH, "tecnica_self_critique.txt")
        return _load_knowledge_from_file(filepath)
    
    else:
        # Se nenhum conhecimento for encontrado, retorna None
        print("--- [Motor] Nenhum conhecimento local relevante encontrado para esta tarefa.")
        return None

def _build_rag_prompt(knowledge_context, user_task):
    """Constrói o prompt final combinando o RAG e a tarefa."""
    
    # Se não houver contexto, apenas envia a tarefa
    if knowledge_context is None:
        return user_task

    # Se houver contexto, constrói o prompt de RAG completo
    return f"""### CONHECIMENTO CANÔNICO (RAG) ###
{knowledge_context}

### TAREFA DO USUÁRIO ###
{user_task}
"""


# --- 4. Lógica Principal da Aplicação ---

def generate(user_task):
    """
    Configura e executa uma chamada para a API Generativa do Google.
    Esta função agora recebe uma 'user_task' dinâmica.
    """
    
    try:
        # --- Início da Lógica RAG Dinâmica ---
        
        # 1. Encontra o conhecimento relevante baseado na tarefa
        knowledge_context = _find_relevant_knowledge(user_task)
        
        # 2. Constrói o prompt final (seja com RAG ou não)
        dynamic_rag_prompt = _build_rag_prompt(knowledge_context, user_task)
        
        # --- Fim da Lógica RAG Dinâmica ---

        # 3. Define os parâmetros de geração (ex: temperatura)
        generation_config = genai.GenerationConfig(
            temperature=0
        )

        # 4. Inicializa o Modelo Generativo
        model = genai.GenerativeModel(
            model_name="gemini-2.5-pro",
            system_instruction=ZENITH_SYSTEM_INSTRUCTION,
            generation_config=generation_config
        )

        # 5. Monta o payload de 'contents' (Usando seu formato de dicionário)
        contents = [
            {
                "role": "user",
                "parts": [
                    {"text": dynamic_rag_prompt}
                ]
            }
        ]

        # 6. Executa a chamada da API
        print("--- [Motor] Enviando solicitação para o Zenith (Fase 4)...")
        response = model.generate_content(contents)

        # 7. Imprime a resposta
        print("--- [Motor] Resposta do Zenith Recebida ---")
        print(response.text)

    except Exception as e:
        print(f"\n--- OCORREU UM ERRO DURANTE A EXECUÇÃO ---")
        print(f"Tipo do Erro: {type(e).__name__}")
        print(f"Mensagem: {e}")
    finally:
        print("\n--- [Motor] Fim da Execução ---")


# --- 5. Ponto de Entrada ---

# (Removido o 'if __name__ == "__main__":' pois este arquivo é um módulo)
# (A execução agora é controlada 100% pelo main.py)
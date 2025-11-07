"""
Ponto de Entrada Principal (Botão de Ignição) do Zenith-Core.

Este script define a(s) tarefa(s) do usuário e as envia 
para o 'zenith_engine.py' para processamento.
"""

# 1. Importa a função 'generate' (o motor) do nosso arquivo 'zenith_engine.py'
from zenith_engine import generate

# 2. Ponto de Entrada Padrão do Python
if __name__ == "__main__":
    
    print("--- [main.py] Iniciando o Zenith-Core ---")
    
    # --- DEFINA SUA TAREFA AQUI ---
    # Esta é a tarefa que o usuário final irá fornecer.
    minha_tarefa = """Com base no Conhecimento Canônico fornecido acima e em suas Instruções de Sistema (Zenith), otimize o seguinte prompt:

"Eu preciso criar um plano, mas quero que ele seja revisado. Use self-critique."
"""
    
    # Chama a função 'generate' e passa a tarefa para ela
    generate(minha_tarefa)
    
    print("--- [main.py] Execução concluída ---")
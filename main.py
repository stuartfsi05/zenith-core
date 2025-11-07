"""
Ponto de Entrada Principal (Botão de Ignição) do Zenith-Core.

Este script é o "botão de ignição" do projeto.
Sua única responsabilidade é importar e executar a lógica principal
definida no módulo 'zenith_engine.py'.
"""

# 1. Importa a função 'generate' (o motor) do nosso arquivo 'zenith_engine.py'
from zenith_engine import generate

# 2. Ponto de Entrada Padrão do Python
if __name__ == "__main__":
    # Este é o bloco de código que roda quando você executa: python main.py
    print("--- [main.py] Iniciando o Zenith-Core ---")
    
    # Chama a função 'generate' que está no 'zenith_engine'
    generate()
    
    print("--- [main.py] Execução concluída ---")
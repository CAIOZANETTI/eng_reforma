import re
import random
import os
from pathlib import Path

def selecionar_prompt_aleatorio():
    # Caminho do arquivo de exemplos
    base_dir = Path(__file__).parent.parent
    examples_file = base_dir / "examples" / "prompts_exemplo.md"
    
    if not examples_file.exists():
        print("Erro: Arquivo de exemplos não encontrado.")
        return

    with open(examples_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex para encontrar blocos de código com prompts
    # Procura por ```\n(conteudo)\n```
    prompts = re.findall(r'```\s*\n(.*?)\n```', content, re.DOTALL)
    
    # Filtrar blocos que não parecem prompts (ex: bash, python)
    prompts_validos = [p for p in prompts if not p.startswith('python') and not p.startswith('bash') and len(p) > 20]

    if not prompts_validos:
        print("Nenhum prompt válido encontrado.")
        return

    prompt_escolhido = random.choice(prompts_validos)
    
    # Limpar quebras de linha extras
    prompt_limpo = " ".join(prompt_escolhido.split())
    
    print(prompt_limpo)

if __name__ == "__main__":
    selecionar_prompt_aleatorio()

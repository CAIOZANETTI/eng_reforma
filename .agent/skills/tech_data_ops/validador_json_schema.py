"""
Skill: Validador de Schema JSON (Obra Ninja)
Descrição: Verifica se os arquivos JSON de projeto seguem a estrutura estrita exigida pelo sistema, prevenindo erros no orçamentação.
"""

import json
import os

REQUIRED_STRUCTURE = {
    "project": ["name", "total_area"],
    "spaces": ["_name", "area", "services"],
    "service_item": ["service_id", "_name", "quantity", "material_categories", "labor_categories"],
    "material_category": ["material_category_id", "materials"],
    "material": ["material_id", "_name"],
    "labor": ["labor_id", "_name"]
}

def validar_arquivo_projeto(filepath):
    """
    Valida um único arquivo JSON.
    Retorna (True, []) se válido, ou (False, list_of_errors) se inválido.
    """
    erros = []
    
    if not os.path.exists(filepath):
        return False, ["Arquivo não encontrado."]
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Erro de Sintaxe JSON: {str(e)}"]
        
    # 1. Validar Project Info
    if "project" not in data:
        erros.append("Campo 'project' ausente na raiz.")
    else:
        for field in REQUIRED_STRUCTURE["project"]:
            if field not in data["project"]:
                erros.append(f"Campo 'project.{field}' obrigatório.")
                
    # 2. Validar Spaces
    if "spaces" not in data or not isinstance(data["spaces"], list):
        erros.append("Lista 'spaces' ausente ou inválida.")
    else:
        for i, space in enumerate(data["spaces"]):
            # Validar campos do Space
            for field in REQUIRED_STRUCTURE["spaces"]:
                if field not in space:
                    erros.append(f"Space[{i}]: Campo '{field}' ausente.")
            
            # Validar Services
            services = space.get("services", [])
            for j, svc in enumerate(services):
                for field in REQUIRED_STRUCTURE["service_item"]:
                    if field not in svc:
                        erros.append(f"Space[{i}].Service[{j}]: Campo '{field}' ausente.")
                
                # Validar Materiais
                mats_cats = svc.get("material_categories", [])
                for k, cat in enumerate(mats_cats):
                    if "materials" not in cat:
                        erros.append(f"Space[{i}].Service[{j}].MatCat[{k}]: Lista 'materials' ausente.")
                    
                    for l, mat in enumerate(cat.get("materials", [])):
                         if "material_id" not in mat:
                             erros.append(f"Space[{i}].Service[{j}].MatCat[{k}].Mat[{l}]: 'material_id' ausente.")

    if len(erros) > 0:
        return False, erros
        
    return True, ["Arquivo Válido."]

if __name__ == "__main__":
    # Teste rápido
    print("--- Teste de Validação JSON ---")
    # path_teste = "caminho/para/arquivo.json"
    # valido, msgs = validar_arquivo_projeto(path_teste)
    # print(msgs)

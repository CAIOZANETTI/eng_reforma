import json
import argparse
import os
import re
import uuid
from datetime import datetime

def convert_to_json(input_file, output_dir):
    if not os.path.exists(input_file):
        print(f"Erro: {input_file} não encontrado.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Regex to find table row: | ID | Desc | Qtd | Unit |
    table_regex = re.compile(r"\|\s*`?([^`|]+)`?\s*\|\s*([^|]+)\s*\|\s*([\d\.]+)\s*\|\s*([^|]+)\s*\|")
    
    # Extract Title
    title = "Reforma Ninja"
    for line in lines:
        if line.startswith("# Orçamento Preliminar:"):
            title = line.replace("# Orçamento Preliminar:", "").strip()
            break
            
    services_list = []
    
    for line in lines:
        match = table_regex.search(line)
        if match:
            svc_id = match.group(1).strip()
            desc = match.group(2).strip()
            qtd_str = match.group(3).strip()
            unit = match.group(4).strip()
            
            if "ID" in svc_id or "---" in line:
                continue
                
            try:
                qtd = float(qtd_str)
            except:
                qtd = 1.0
                
            services_list.append({
                "service_id": svc_id,
                "_name": desc,
                "quantity": qtd,
                "material_categories": [], # Populating this would require composition lookup
                "labor_categories": []
            })
            
    # Build JSON structure
    space_id = str(uuid.uuid4())
    project_id = str(uuid.uuid4())
    
    output_json = {
        "version": "1.0",
        "exportedAt": datetime.now().isoformat() + "Z", # Approximating Z format
        "template": {
            "title": title,
            "description": f"Gerado a partir de: {title}",
            "language_code": "pt-BR",
            "property_type": "apartamento", # Default
            "status": "ready"
        },
        "project": {
            "name": title,
            "total_area": 0 # Default
        },
        "spaces": [
            {
                "space_id": space_id,
                "_name": "Ambiente Principal",
                "area": 0,
                "height": 2.6,
                "services": services_list
            }
        ]
    }
    
    os.makedirs(output_dir, exist_ok=True)
    filename = f"reforma_{project_id}.json"
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)
        
    print(f"JSON gerado com sucesso: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Converter Orcamento MD para JSON")
    parser.add_argument("--input", required=True, help="Arquivo MD de entrada")
    parser.add_argument("--output_dir", required=True, help="Diretório de saída")
    
    args = parser.parse_args()
    
    convert_to_json(args.input, args.output_dir)

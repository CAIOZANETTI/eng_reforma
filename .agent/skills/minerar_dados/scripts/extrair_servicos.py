import json
import csv
import os
import argparse
from glob import glob

def extract_services(input_dir, output_dir):
    services = {}
    compositions = []

    json_files = glob(os.path.join(input_dir, "*.json"))
    print(f"Encontrados {len(json_files)} arquivos JSON em {input_dir}")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            spaces = data.get("spaces", [])
            for space in spaces:
                for service in space.get("services", []):
                    svc_id = service.get("service_id")
                    svc_name = service.get("_name")
                    
                    if svc_id:
                        if svc_id not in services:
                            services[svc_id] = {"id": svc_id, "name": svc_name}
                            
                            # Extract compositions (only once per unique service ID found)
                            # Material Categories
                            for cat in service.get("material_categories", []):
                                compositions.append({
                                    "service_id": svc_id,
                                    "type": "material",
                                    "category_id": cat.get("material_category_id"),
                                    "base_qtd": cat.get("base_qtd"),
                                    "base_unit": cat.get("base_unit")
                                })
                            
                            # Labor Categories
                            for cat in service.get("labor_categories", []):
                                compositions.append({
                                    "service_id": svc_id,
                                    "type": "labor",
                                    "category_id": cat.get("labor_category_id"),
                                    "base_qtd": cat.get("base_qtd"),
                                    "base_unit": cat.get("base_unit")
                                })

        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")

    # Write CSVs
    os.makedirs(output_dir, exist_ok=True)
    
    # Services
    with open(os.path.join(output_dir, "services.csv"), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name"])
        writer.writeheader()
        for s in services.values():
            writer.writerow(s)
            
    # Compositions
    with open(os.path.join(output_dir, "compositions.csv"), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["service_id", "type", "category_id", "base_qtd", "base_unit"])
        writer.writeheader()
        for c in compositions:
            writer.writerow(c)

    print(f"Extração de serviços concluída. Arquivos salvos em {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrair serviços de JSONs Obra Ninja")
    parser.add_argument("--input_dir", required=True, help="Diretório com JSONs")
    parser.add_argument("--output_dir", required=True, help="Diretório de saída para CSVs")
    args = parser.parse_args()
    
    extract_services(args.input_dir, args.output_dir)

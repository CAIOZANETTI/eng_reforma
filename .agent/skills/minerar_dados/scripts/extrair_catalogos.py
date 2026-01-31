import json
import csv
import os
import argparse
from glob import glob

def extract_catalogs(input_dir, output_dir):
    materials = {}
    labors = {}
    categories = {}

    json_files = glob(os.path.join(input_dir, "*.json"))
    print(f"Encontrados {len(json_files)} arquivos JSON em {input_dir}")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            spaces = data.get("spaces", [])
            for space in spaces:
                services = space.get("services", [])
                for service in services:
                    # Extract Material Categories and Materials
                    for cat in service.get("material_categories", []):
                        cat_id = cat.get("material_category_id")
                        cat_name = cat.get("_name")
                        if cat_id:
                            categories[cat_id] = {"id": cat_id, "name": cat_name, "type": "material"}
                            
                        for mat in cat.get("materials", []):
                            mat_id = mat.get("material_id")
                            if mat_id:
                                materials[mat_id] = {
                                    "id": mat_id,
                                    "name": mat.get("_name"),
                                    "category_id": cat_id,
                                    # Base unit info is usually on the category level in the JSON example
                                    "base_unit": cat.get("base_unit") 
                                }

                    # Extract Labor Categories and Labors
                    for cat in service.get("labor_categories", []):
                        cat_id = cat.get("labor_category_id")
                        cat_name = cat.get("_name")
                        if cat_id:
                            categories[cat_id] = {"id": cat_id, "name": cat_name, "type": "labor"}
                            
                        for lab in cat.get("labors", []):
                            lab_id = lab.get("labor_id")
                            if lab_id:
                                labors[lab_id] = {
                                    "id": lab_id,
                                    "name": lab.get("_name"),
                                    "category_id": cat_id,
                                    "base_unit": cat.get("base_unit")
                                }

        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")

    # Write CSVs
    os.makedirs(output_dir, exist_ok=True)
    
    # Categories
    with open(os.path.join(output_dir, "categories.csv"), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "type"])
        writer.writeheader()
        for c in categories.values():
            writer.writerow(c)
            
    # Materials
    with open(os.path.join(output_dir, "materials.csv"), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "category_id", "base_unit"])
        writer.writeheader()
        for m in materials.values():
            writer.writerow(m)

    # Labor
    with open(os.path.join(output_dir, "labor.csv"), 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "category_id", "base_unit"])
        writer.writeheader()
        for l in labors.values():
            writer.writerow(l)

    print(f"Extração concluída. Arquivos salvos em {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrair catálogos de JSONs Obra Ninja")
    parser.add_argument("--input_dir", required=True, help="Diretório com JSONs")
    parser.add_argument("--output_dir", required=True, help="Diretório de saída para CSVs")
    args = parser.parse_args()
    
    extract_catalogs(args.input_dir, args.output_dir)

import json
import csv
import os
import argparse
from glob import glob

def extract_knowledge(input_dir, output_dir):
    # Dictionaries to store unique values
    property_types = set()
    services = {}
    material_categories = {}
    labor_categories = {}
    materials = {}
    base_units = set()

    json_files = glob(os.path.join(input_dir, "*.json"))
    print(f"Encontrados {len(json_files)} arquivos JSON em {input_dir}")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 1. Property Type
            pt = data.get("template", {}).get("property_type")
            if pt:
                property_types.add(pt)

            spaces = data.get("spaces", [])
            for space in spaces:
                for service in space.get("services", []):
                    # 2. Services
                    svc_id = service.get("service_id")
                    svc_name = service.get("_name")
                    if svc_id:
                        services[svc_id] = {"id": svc_id, "name": svc_name}

                    # 3. Material Categories & Materials
                    for cat in service.get("material_categories", []):
                        mc_id = cat.get("material_category_id")
                        mc_name = cat.get("_name")
                        mc_unit = cat.get("base_unit")
                        
                        if mc_id:
                            material_categories[mc_id] = {"id": mc_id, "name": mc_name}
                        if mc_unit:
                            base_units.add(mc_unit)

                        for mat in cat.get("materials", []):
                            mat_id = mat.get("material_id")
                            mat_name = mat.get("_name")
                            if mat_id:
                                materials[mat_id] = {
                                    "id": mat_id, 
                                    "name": mat_name, 
                                    "category_id": mc_id
                                }

                    # 4. Labor Categories & Labors
                    for cat in service.get("labor_categories", []):
                        lc_id = cat.get("labor_category_id")
                        lc_name = cat.get("_name")
                        lc_unit = cat.get("base_unit")

                        if lc_id:
                            labor_categories[lc_id] = {"id": lc_id, "name": lc_name}
                        if lc_unit:
                            base_units.add(lc_unit)

        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")

    # Write CSVs
    os.makedirs(output_dir, exist_ok=True)

    def write_csv(filename, fieldnames, data):
        path = os.path.join(output_dir, filename)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            if isinstance(data, list):
                for row in data:
                    writer.writerow(row) # Expecting list of dicts
            elif isinstance(data, dict):
                 for row in data.values():
                    writer.writerow(row)
            elif isinstance(data, set):
                for item in data:
                    writer.writerow({fieldnames[0]: item})

    # property_type.csv
    write_csv("property_type.csv", ["name"], property_types)

    # services.csv
    write_csv("services.csv", ["id", "name"], services)

    # material_category_id.csv
    write_csv("material_category_id.csv", ["id", "name"], material_categories)

    # labor_categories.csv
    write_csv("labor_categories.csv", ["id", "name"], labor_categories)

    # materials.csv
    write_csv("materials.csv", ["id", "name", "category_id"], materials)

    # base_unit.csv
    write_csv("base_unit.csv", ["unit"], base_units)
    
    # Also generate compositions for richer data usage (though requested specifically the CSVs above, compositions are vital)
    # I will skip compositions.csv for now as it wasn't explicitly requested in the latest "refactoring" list, 
    # but strictly follow the list: property_type, services, material_category_id, labor_categories, materials, base_unit.

    print(f"Extração concluída. Arquivos salvos em {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minerar dados de JSONs Obra Ninja")
    parser.add_argument("--input_dir", required=True, help="Diretório com JSONs")
    parser.add_argument("--output_dir", required=True, help="Diretório de saída para CSVs")
    args = parser.parse_args()
    
    extract_knowledge(args.input_dir, args.output_dir)

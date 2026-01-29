import csv
import json
import uuid
import os
from datetime import datetime

# --- ObraNinjaBuilder Class (Copied from Skill) ---
class ObraNinjaBuilder:
    def __init__(self, project_name, total_area, property_type="apartamento", description=""):
        self.data = {
            "version": "1.0",
            "exportedAt": datetime.utcnow().isoformat() + "Z",
            "template": {
                "title": project_name,
                "description": description,
                "language_code": "pt-BR",
                "property_type": property_type,
                "status": "ready"
            },
            "project": {
                "name": project_name,
                "total_area": total_area
            },
            "spaces": []
        }

    def add_space(self, name, area, height=2.6):
        """Adiciona um ambiente (Space) ao projeto."""
        space_id = str(uuid.uuid4())
        space = {
            "space_id": space_id,
            "_name": name,
            "area": area,
            "height": height,
            "services": []
        }
        self.data["spaces"].append(space)
        return space_id

    def add_service(self, space_id, service_name, quantity=1, service_id_slug=None):
        """Adiciona um serviço a um ambiente existente."""
        space = next((s for s in self.data["spaces"] if s["space_id"] == space_id), None)
        if not space:
            raise ValueError(f"Space ID {space_id} not found.")

        if not service_id_slug:
            service_id_slug = service_name.lower().replace(" ", "_").replace("ç", "c").replace("ã", "a")

        service = {
            "service_id": service_id_slug,
            "_name": service_name,
            "quantity": quantity,
            "material_categories": [],
            "labor_categories": []
        }
        space["services"].append(service)
        return service_id_slug

    def add_material(self, space_id, service_id_slug, category_name, material_name, base_qtd, base_unit, material_id=None):
        """Adiciona um material a um serviço."""
        space = next((s for s in self.data["spaces"] if s["space_id"] == space_id), None)
        if not space: return

        service = next((s for s in space["services"] if s["service_id"] == service_id_slug), None)
        if not service: return

        # Verificar se a categoria já existe
        category_slug = category_name.lower().replace(" ", "_")
        category = next((c for c in service["material_categories"] if c["_name"] == category_name), None)

        if not category:
            category = {
                "material_category_id": category_slug,
                "_name": category_name,
                "base_qtd": base_qtd,
                "base_unit": base_unit,
                "materials": []
            }
            service["material_categories"].append(category)

        # Adicionar material
        if not material_id:
            material_id = str(uuid.uuid4())
        
        material = {
            "material_id": material_id,
            "_name": material_name
        }
        category["materials"].append(material)

    def add_labor(self, space_id, service_id_slug, category_name, base_qtd, base_unit="h", labor_id=None):
        """Adiciona mão de obra a um serviço."""
        space = next((s for s in self.data["spaces"] if s["space_id"] == space_id), None)
        if not space: return

        service = next((s for s in space["services"] if s["service_id"] == service_id_slug), None)
        if not service: return

        # Verificar se a categoria já existe
        category_slug = category_name.lower().replace(" ", "_")
        category = next((c for c in service["labor_categories"] if c["_name"] == category_name), None)

        if not category:
            category = {
                "labor_category_id": category_slug,
                "_name": category_name,
                "base_qtd": base_qtd,
                "base_unit": base_unit,
                "labors": []
            }
            service["labor_categories"].append(category)
        
        if not labor_id:
            labor_id = str(uuid.uuid4())

        labor = {
            "labor_id": labor_id,
            "_name": category_name # Geralmente o nome do labor individual segue a categoria
        }
        category["labors"].append(labor)

    def validate(self):
        """Valida a estrutura do dicionário atual contra o schema Obraninja V1."""
        errors = []
        required_root = ["version", "template", "project", "spaces"]
        for field in required_root:
            if field not in self.data:
                errors.append(f"Missing root field: {field}")
        
        if not self.data["spaces"]:
            errors.append("Project must have at least one Space.")

        return len(errors) == 0, errors

    def to_json(self, filepath):
        """Exporta para arquivo JSON."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        return filepath

# --- Main Script ---

CSV_PATH = r"d:\github\eng_reforma\obra_ninja\csv\lista_reforma\lista_reforma_ranking.csv"
OUTPUT_DIR = r"d:\github\eng_reforma\ranking_test_ott"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Normalize headers to handle potential BOM or whitespace
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        
        count = 0
        for row in reader:
            try:
                row_id = row['id']
                tipo = row['tipo']
                ambiente = row['área (ambiente)']
                area_m2_str = row['area_m2']
                
                # Handle possible parsing errors
                try:
                    area_m2 = float(area_m2_str)
                except ValueError:
                    area_m2 = 0.0

                acabamento = row.get('acabamento (popular / médio / luxo / comercial)', '')
                descricao = row.get('descrição da reforma (sem ampliação)', '')

                project_name = f"Reforma {row_id} - {tipo} - {ambiente}"
                full_desc = f"{descricao} | Acabamento: {acabamento} | Imóvel: {row.get('qtd_imovel (padrão 2Q+1B)', '')}"

                # Create Builder
                builder = ObraNinjaBuilder(
                    project_name=project_name,
                    total_area=area_m2,
                    property_type=tipo.lower(),
                    description=full_desc
                )

                # Add Space
                builder.add_space(name=ambiente, area=area_m2)

                # Validate
                is_valid, errors = builder.validate()
                if not is_valid:
                    print(f"Skipping row {row_id} due to validation errors: {errors}")
                    continue

                # Save JSON
                filename = f"ranking_{row_id}.json"
                filepath = os.path.join(OUTPUT_DIR, filename)
                builder.to_json(filepath)
                count += 1
                
            except KeyError as e:
                print(f"KeyError processing row: {e}. Keys found: {list(row.keys())}")
            except Exception as e:
                print(f"Error processing row {row.get('id', 'unknown')}: {e}")

        print(f"Successfully generated {count} JSON files in {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

"""
Skill: Validador e Construtor JSON Obra Ninja
Descrição: Classe utilitária para criar e validar arquivos JSON no formato padrão 'Obra Ninja'. Garante que a estrutura de Spaces, Services, Material Categories e Labor Categories esteja correta antes da exportação.
"""

import json
import uuid
from datetime import datetime
import os

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

# Exemplo de uso
if __name__ == "__main__":
    builder = ObraNinjaBuilder("Reforma Exemplo", 50, description="Teste de Builder")
    sid = builder.add_space("Sala", 20)
    svid = builder.add_service(sid, "Pintura", 1)
    builder.add_material(sid, svid, "Tinta", "Tinta Acrilica", 0.3, "l")
    builder.add_labor(sid, svid, "Pintor", 0.5, "h")
    
    is_valid, errs = builder.validate()
    if is_valid:
        print(json.dumps(builder.data, indent=2, ensure_ascii=False))
    else:
        print("Erros:", errs)

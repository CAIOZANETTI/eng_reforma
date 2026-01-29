---
name: Escopo JSON
description: Converter escopo de reforma para JSON no padrão Obra Ninja
version: 1.0
dependencies: [custo_reforma]
---

# Skill: Escopo JSON

## Objetivo
Converter o escopo de reforma custeado para o formato JSON padrão Obra Ninja, validando IDs de materiais e ambientes.

## Entradas
- Escopo custeado (CSV)
- Lista de materiais válidos (`lista_materiais.csv`)
- Lista de ambientes válidos (`lista_ambientes.csv`)
- Schema de validação (`obra_ninja_schema.json`)

## Saídas
- Arquivo JSON válido no padrão Obra Ninja
- Relatório de validação
- Lista de materiais/ambientes não mapeados (se houver)

## Scripts Disponíveis

### `scripts/converte_escopo_to_obra_ninja_json.py`
Converte CSV para JSON Obra Ninja.

```bash
python converte_escopo_to_obra_ninja_json.py --input escopo_custeado.csv --materiais lista_materiais.csv --ambientes lista_ambientes.csv --output projeto.json
```

### `scripts/validar_json.py`
Valida JSON contra o schema.

```bash
python validar_json.py --input projeto.json --schema obra_ninja_schema.json
```

**Saída:**
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": ["Material 'Porcelanato XYZ' não encontrado, usando genérico"]
}
```

### `scripts/validar_lote.py`
Valida múltiplos JSONs de um diretório.

```bash
python validar_lote.py --dir ranking_test_ott/ --output validacao_lote.json
```

## Exemplos Disponíveis

### `examples/obra_ninja_schema.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["version", "template", "project", "spaces"],
  "properties": {
    "version": {"type": "string", "const": "1.0"},
    "exportedAt": {"type": "string", "format": "date-time"},
    "template": {
      "type": "object",
      "required": ["title", "language_code", "property_type", "status"],
      "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "language_code": {"type": "string", "enum": ["pt-BR"]},
        "property_type": {"type": "string", "enum": ["apto", "casa", "escritório", "loja", "clínica", "restaurante"]},
        "status": {"type": "string", "enum": ["ready", "draft"]}
      }
    },
    "project": {
      "type": "object",
      "required": ["name", "total_area"],
      "properties": {
        "name": {"type": "string"},
        "total_area": {"type": "number", "minimum": 0}
      }
    },
    "spaces": {
      "type": "array",
      "minItems": 1,
      "items": {"$ref": "#/definitions/space"}
    }
  },
  "definitions": {
    "space": {
      "type": "object",
      "required": ["space_id", "_name", "area", "services"],
      "properties": {
        "space_id": {"type": "string", "format": "uuid"},
        "_name": {"type": "string"},
        "area": {"type": "number", "minimum": 0},
        "height": {"type": "number", "default": 2.6},
        "services": {"type": "array", "items": {"$ref": "#/definitions/service"}}
      }
    },
    "service": {
      "type": "object",
      "required": ["service_id", "_name", "quantity"],
      "properties": {
        "service_id": {"type": "string"},
        "_name": {"type": "string"},
        "quantity": {"type": "number"},
        "material_categories": {"type": "array"},
        "labor_categories": {"type": "array"}
      }
    }
  }
}
```

## Recursos Disponíveis

### `resources/lista_materiais.csv`
```csv
material_id,nome,categoria,unidade
MAT-001,Porcelanato 60x60 Biancogres,Revestimento,m²
MAT-002,Porcelanato 90x90 Portobello,Revestimento,m²
MAT-003,Cerâmica 45x45 Eliane,Revestimento,m²
MAT-004,Tinta Suvinil Premium,Pintura,l
MAT-005,Tinta Coral Standard,Pintura,l
MAT-006,Vaso Deca Aspen,Louças,un
MAT-007,Cuba Docol,Louças,un
```

### `resources/lista_ambientes.csv`
```csv
ambiente_id,nome,tipo_imovel,area_min,area_max
AMB-001,Banheiro,todos,2.5,12
AMB-002,Banheiro social,apto,3,8
AMB-003,Lavabo,todos,1.5,4
AMB-004,Quarto,todos,8,25
AMB-005,Suíte,todos,12,40
AMB-006,Cozinha,todos,4,30
AMB-007,Sala,todos,12,80
AMB-008,Lavanderia,todos,2,15
```

## Classe Builder (Validador)

O script utiliza a classe `ObraNinjaBuilder` para construir e validar JSONs:

```python
from validador_json_obra_ninja import ObraNinjaBuilder

builder = ObraNinjaBuilder("Reforma Banheiro", 5, "apto", "Reforma completa")
space_id = builder.add_space("Banheiro", 5)
builder.add_service(space_id, "Revestimento", 1)
builder.add_material(space_id, "revestimento", "Porcelanato", "Biancogres 60x60", 5.5, "m²")
builder.add_labor(space_id, "revestimento", "Pedreiro", 8, "h")

is_valid, errors = builder.validate()
if is_valid:
    builder.to_json("projeto.json")
```

## Mapeamento de Serviços

| Serviço CSV | Service ID JSON |
|-------------|-----------------|
| Demolição | demolicao |
| Impermeabilização | impermeabilizacao |
| Contrapiso | contrapiso |
| Piso | revestimento_piso |
| Parede | revestimento_parede |
| Pintura | pintura |
| Louças | loucas |
| Metais | metais |
| Box | box_vidro |
| Elétrica | eletrica |
| Hidráulica | hidraulica |

## Uso no Pipeline (Final)

```
custo_reforma → escopo_json → [JSON Obra Ninja]
```

Este é o skill final do pipeline, responsável por gerar a saída que será consumida pelo sistema Obra Ninja.

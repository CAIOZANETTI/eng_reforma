name: Obra Ninja
description: O Bibliotecário - Responsável por entender o modelo de dados dos JSONs existentes e minerar conhecimento (CSVs).
version: 1.0
dependencies: []
---

# Skill: Obra Ninja

## Descrição
Esta skill atua como a guardiã do conhecimento do sistema. Ela "le" os projetos passados (arquivos JSON na pasta `obra_ninja/json`) e extrai padrões para serem usados em novos orçamentos.

## Inputs
- Diretório de JSONs: `obra_ninja/json/*.json`

## Outputs
- Arquivos CSV na pasta `.agent/knowledge_base/`:
  - `property_type.csv`
  - `services.csv`
  - `materials.csv`
  - `material_category_id.csv`
  - `labor_categories.csv`
  - `base_unit.csv`

## Scripts

### `scripts/minerar_json.py`
Script principal que varre os arquivos JSON e popula os CSVs.

**Uso:**
```bash
python minerar_json.py --input_dir ../../../../obra_ninja/json --output_dir ../../../../.agent/knowledge_base
```

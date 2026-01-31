name: Validador Schema
description: O Programador - Valida estrutura JSON e Integridade Referencial SQL.
version: 1.0
dependencies: ["minerador_relacional"]
---

# Skill: Validador Schema

## Descrição
Garante que o JSON gerado seja válido e, principalmente, que **todos** os IDs relacionais (Serviços, Materiais) existam na Whitelist.

## Inputs
- `projeto.json`
- `whitelist.json` (Gerado pelo minerador)

## Outputs
- `report_schema.txt` (Validation Status)

## Scripts

### `scripts/validate_schema.py`
Carrega a whitelist e cruza com o projeto.

**Uso:**
```bash
python validate_schema.py --input_file ../../../../.agent/output/projeto.json --whitelist ../../../../.agent/knowledge_base/whitelist.json
```

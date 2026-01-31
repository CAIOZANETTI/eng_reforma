name: Minerador Relacional
description: O Auditor - Mapeia e valida IDs existentes para garantir integridade referencial SQL.
version: 1.0
dependencies: []
---

# Skill: Minerador Relacional

## Descrição
Analisa todos os projetos JSON legados e constrói uma "lista branca" (whitelist) de todos os IDs relacionais permitidos. Isso é crucial para que o Gerador não invente dados que quebrariam o banco SQL.

## Inputs
- `obra_ninja/json/*.json`

## Outputs
- `.agent/knowledge_base/whitelist.json`: Arquivo contendo conjuntos de IDs válidos para Services, Materials, Categories (Material/Labor).

## Scripts

### `scripts/map_relational_ids.py`
Script que varre os diretórios e consolida os IDs únicos.

**Uso:**
```bash
python map_relational_ids.py --input_dir ../../../../obra_ninja/json --output_file ../../../../.agent/knowledge_base/whitelist.json
```

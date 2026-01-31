name: Gerador JSON
description: O Projetista - Clona projetos existentes variando métricas geometricas.
version: 1.0
dependencies: ["minerador_relacional"]
---

# Skill: Gerador JSON

## Descrição
Responsável por criar novos projetos JSON a partir de um template real. Aplica fator de escala nas áreas e quantidades sem tocar nos IDs.

## Inputs
- `template_json`: Caminho para o JSON base.
- `scale_factor`: Multiplicador de área (ex: 1.5 para 50% maior).

## Outputs
- Arquivo JSON na pasta `.agent/output/` com novo UUID de projeto e space.

## Scripts

### `scripts/generate_variation.py`
Carrega o template, multiplica áreas e quantidades pelo fator de escala, gera novos UUIDs para o container (Projeto/Space) mas MANTÉM os IDs relacionais.

**Uso:**
```bash
python generate_variation.py --template ../../../../obra_ninja/json/exemplo.json --scale 1.2 --output_dir ../../../../.agent/output
```

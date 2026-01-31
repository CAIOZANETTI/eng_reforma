name: Orçamento Obra Ninja
description: O Integrador - Converte o relatório de orçamento validado para o formato JSON final do sistema Obra Ninja.
version: 1.0
dependencies: ["cria_orcamento", "valida_orcamento"]
---

# Skill: Orçamento Obra Ninja

## Descrição
Responsável pela etapa final de formalização. Pega o "rascunho" em Markdown (validado) e serializa para um arquivo JSON compatível com o schema do Obra Ninja.

## Inputs
- `orcamento_validado.md`

## Outputs
- Arquivo JSON na pasta `output/` (ex: `reforma_uuid.json`)

## Scripts

### `scripts/converter_json.py`
Faz o parsing do MD e monta o JSON final gerando UUIDs e estruturando os dados.

**Uso:**
```bash
python converter_json.py --input orcamento.md --output_dir ../../../../output
```

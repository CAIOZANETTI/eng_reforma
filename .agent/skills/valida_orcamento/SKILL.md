name: Valida Orçamento
description: O Engenheiro - Responsável por validar as estimativas, unidades e preços do orçamento.
version: 1.0
dependencies: ["obra_ninja"]
---

# Skill: Valida Orçamento

## Descrição
Lê o arquivo Markdown de orçamento preliminar e valida consistência de dados (unidades, existência de serviços na base, etc.).

## Inputs
- `orcamento.md` (Markdown Draft)
- Knowledge Base CSVs

## Outputs
- `orcamento_validado.md` (Markdown corrigido/anotado)
- Logs de erro se houver inconsistências.

## Scripts

### `scripts/validar_dados.py`
Verifica se as unidades informadas batem com `base_unit.csv` e se os serviços existem.

**Uso:**
```bash
python validar_dados.py --input orcamento_draft.md --kb_dir ../../../../.agent/knowledge_base
```

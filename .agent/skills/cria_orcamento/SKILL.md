name: Cria Orçamento
description: O Arquiteto - Responsável por transformar o pedido do cliente em uma proposta inicial de orçamento em Markdown.
version: 1.0
dependencies: ["obra_ninja"]
---

# Skill: Cria Orçamento

## Descrição
Recebe um prompt de reforma (ex: "Quero reformar meu banheiro") e gera um orçamento preliminar consultando os serviços minerados na Base de Conhecimento.

## Inputs
- Prompt do usuário (texto)
- CSVs da Knowledge Base

## Outputs
- Arquivo Markdown (`orcamento.md`) contendo:
  - Título do Projeto
  - Lista de Ambientes e Serviços Sugeridos
  - Estimativa de Quantidades

## Scripts

### `scripts/gerar_orcamento.py`
Analisa o texto e sugere serviços baseados em palavras-chave.

**Uso:**
```bash
python gerar_orcamento.py --prompt "reforma de banheiro e cozinha" --output orcamento_draft.md
```

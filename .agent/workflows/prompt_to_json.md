---
description: Workflow para criar um JSON de reforma válido no padrão Obra Ninja a partir de um prompt do empreiteiro
---

# Workflow: Prompt to JSON

## Objetivo
Transformar um pedido de reforma em linguagem natural (prompt) em um arquivo JSON validado e orçado.

## Saídas Finais
- `.agent/output/{nome_projeto}.json` - JSON Obra Ninja
- `.agent/output/{nome_projeto}.md` - Orçamento Sintético

## Skills Utilizadas (Pipeline)

| # | Skill | Diretório | Função |
|---|-------|-----------|--------|
| 1 | Empreiteiro | `.agent/skills/01_empreiteiro` | Interpretar prompt |
| 2 | IBGE | `.agent/skills/02_ibge` | Validar dados |
| 3 | Projeto | `.agent/skills/03_projeto` | Sugerir opções |
| 4 | Quantificar | `.agent/skills/04_quantificar` | Calcular áreas |
| 5 | Escopo | `.agent/skills/05_escopo` | Gerar serviços |
| 6 | Custo | `.agent/skills/06_custo` | Precificar (SINAPI) |
| 7 | JSON | `.agent/skills/07_json` | Exportar/Validar |

## Passos

### 1. Preparação
// turbo
```bash
$uuid = [guid]::NewGuid().ToString().Substring(0,8)
New-Item -ItemType Directory -Force -Path ".agent/.temp/$uuid"
```

### 2. Interpretar Prompt (01_empreiteiro)
// turbo
```bash
python .agent/skills/01_empreiteiro/scripts/prompt_tabela.py \
  --prompt "{PROMPT_DO_CLIENTE}" \
  --output .agent/.temp/$uuid/imovel_input.json
```

### 3. Calcular Quantidades (04_quantificar)
// turbo
```bash
python .agent/skills/04_quantificar/scripts/quantificar.py \
  --input .agent/.temp/$uuid/imovel_input.json \
  --output .agent/.temp/$uuid/quantidades.csv
```

### 4. Gerar Escopo (05_escopo)
// turbo
```bash
python .agent/skills/05_escopo/scripts/gerar_escopo.py \
  --input .agent/.temp/$uuid/quantidades.csv \
  --output .agent/.temp/$uuid/escopo.csv
```

### 5. Custear Reforma (06_custo)
// turbo
```bash
python .agent/skills/06_custo/scripts/custear_reforma.py \
  --input .agent/.temp/$uuid/escopo.csv \
  --output .agent/.temp/$uuid/escopo_custeado.csv \
  --sintetico .agent/output/{nome_projeto}.md
```

### 6. Converter para JSON (07_json)
// turbo
```bash
python .agent/skills/07_json/scripts/converte_escopo_to_obra_ninja_json.py \
  --input .agent/.temp/$uuid/escopo_custeado.csv \
  --output .agent/output/{nome_projeto}.json \
  --nome "{nome_projeto_humano}" \
  --descricao "{descricao_projeto}"
```

### 7. Validar Resultado (07_json)
// turbo
```bash
python .agent/skills/07_json/scripts/validar_json.py \
  --input .agent/output/{nome_projeto}.json
```

### 8. Limpeza
// turbo
```bash
Remove-Item -Recurse -Force ".agent/.temp/$uuid"
```

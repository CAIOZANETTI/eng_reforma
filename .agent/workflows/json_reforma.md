---
description: Workflow para criar um JSON de reforma válido no padrão Obra Ninja
---

# Workflow: JSON Reforma

## Objetivo
Gerar um arquivo JSON válido seguindo o padrão Obra Ninja a partir de um prompt do empreiteiro.

## Saídas Finais
Apenas dois arquivos são gerados como output final:
- `{nome_projeto}.json` - JSON no padrão Obra Ninja
- `{nome_projeto}.md` - Relatório sintético do orçamento

## Skills Utilizadas (em ordem)

| # | Skill | Diretório | Função |
|---|-------|-----------|--------|
| 01 | Empreiteiro | `.agent/skills/01_empreiteiro` | Receber e interpretar prompt do cliente |
| 02 | IBGE | `.agent/skills/02_ibge` | Validar dados e referências |
| 03 | Projeto | `.agent/skills/03_projeto` | Sugerir opções de reforma |
| 04 | Quantificar | `.agent/skills/04_quantificar` | Calcular áreas e quantidades |
| 05 | Escopo | `.agent/skills/05_escopo` | Gerar escopo detalhado |
| 06 | Custo | `.agent/skills/06_custo` | Custear com SINAPI |
| 07 | JSON | `.agent/skills/07_json` | Converter para Obra Ninja |

## Passos

### 0. Receber Prompt do Empreiteiro
O empreiteiro envia um prompt em linguagem natural descrevendo a reforma.

**Exemplos de prompts:** Ver `.agent/skills/01_empreiteiro/examples/prompts_exemplo.md`

**Exemplo:**
```
Preciso reformar o banheiro de um apto pequeno de 45m², 1 quarto. 
Banheiro tem uns 3m². Quero trocar o piso e azulejo, colocar um vaso novo 
e uma pia simples. Orçamento apertado, pode ser material mais barato.
```

### 1. Criar diretório temporário
// turbo
```bash
New-Item -ItemType Directory -Force -Path ".agent/.temp/{uuid}"
```

### 2. Executar Skill: 01_empreiteiro (interpretar prompt)
// turbo
```bash
python .agent/skills/01_empreiteiro/scripts/prompt_tabela.py \
  --prompt "{texto do cliente}" \
  --output .agent/.temp/{uuid}/imovel_input.json
```

**Saída esperada:**
```json
{
  "tipo": "apto",
  "area_total": 45,
  "acabamento": "Popular",
  "ambientes": [
    {"nome": "Banheiro", "area": 3}
  ],
  "descricao": "Reforma básica de banheiro"
}
```

### 3. Executar Skill: 02_ibge (validar dados)
```python
# Validar se o tipo de imóvel está na lista válida
tipos_validos = ["apto", "casa", "escritório", "loja", "clínica", "restaurante"]

# Validar áreas mínimas por ambiente (dados IBGE)
areas_minimas = {
    "Banheiro": 2.5,
    "Quarto": 8,
    "Sala": 12,
    "Cozinha": 4
}
```

### 4. Executar Skill: 03_projeto (sugerir opções)
```python
# Baseado no tipo de imóvel e acabamento, sugerir:
# - Materiais adequados ao padrão (Popular/Médio/Luxo)
# - Acabamentos recomendados
# - Paleta de cores

# Exemplo padrão Popular:
materiais = {
    "piso": "Cerâmica 45x45",
    "parede": "Tinta acrílica",
    "bancada": "Granito cinza",
    "metais": "Docol básico"
}
```

### 5. Executar Skill: 04_quantificar
// turbo
```bash
python .agent/skills/04_quantificar/scripts/quantificar.py \
  --input .agent/.temp/{uuid}/imovel_input.json \
  --output .agent/.temp/{uuid}/quantidades.csv
```

### 6. Executar Skill: 05_escopo
// turbo
```bash
python .agent/skills/05_escopo/scripts/gerar_escopo.py \
  --input .agent/.temp/{uuid}/quantidades.csv \
  --acabamento {Popular|Médio|Luxo} \
  --output .agent/.temp/{uuid}/escopo.csv
```

### 7. Executar Skill: 06_custo
// turbo
```bash
python .agent/skills/06_custo/scripts/custear_reforma.py \
  --input .agent/.temp/{uuid}/escopo.csv \
  --output .agent/.temp/{uuid}/escopo_custeado.csv \
  --sintetico .agent/output/{nome_projeto}.md
```

### 8. Executar Skill: 07_json
// turbo
```bash
python .agent/skills/07_json/scripts/converte_escopo_to_obra_ninja_json.py \
  --input .agent/.temp/{uuid}/escopo_custeado.csv \
  --output .agent/output/{nome_projeto}.json \
  --nome "{Título do Projeto}" \
  --descricao "{Descrição}"
```

### 9. Validar JSON
// turbo
```bash
python .agent/skills/07_json/scripts/validar_json.py \
  --input .agent/output/{nome_projeto}.json
```

### 10. Limpar arquivos temporários (opcional)
// turbo
```bash
Remove-Item -Recurse -Force ".agent/.temp/{uuid}"
```

### 11. Retornar Resultado
- Se válido: 
  - `.agent/output/{nome_projeto}.json`
  - `.agent/output/{nome_projeto}.md`
- Se inválido: retornar lista de erros

## Estrutura de Diretórios

```
.agent/
├── output/                    # Saídas finais (apenas .json e .md)
│   ├── reforma_banheiro.json
│   └── reforma_banheiro.md
│
└── .temp/                     # Arquivos intermediários (não versionados)
    └── {uuid_execucao}/
        ├── imovel_input.json      ← Saída do 01_empreiteiro
        ├── quantidades.csv        ← Saída do 04_quantificar
        ├── escopo.csv             ← Saída do 05_escopo
        └── escopo_custeado.csv    ← Saída do 06_custo
```

## Fluxo Visual

```
[PROMPT DO EMPREITEIRO]
         │
         ▼
┌─────────────────┐
│ 01_empreiteiro  │  → Interpreta prompt → imovel_input.json
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    02_ibge      │  → Valida tipo, áreas, padrões
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   03_projeto    │  → Sugere materiais, acabamentos
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 04_quantificar  │  → Calcula m² piso, parede, teto
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   05_escopo     │  → Gera lista de serviços
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   06_custo      │  → Adiciona preços SINAPI
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    07_json      │  → Converte para Obra Ninja
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     SAÍDA       │
│ (.json + .md)   │
└─────────────────┘
```

## Tratamento de Erros
| Erro | Ação |
|------|------|
| Prompt incompreensível | Pedir mais detalhes |
| Tipo de imóvel inválido | Sugerir tipo similar |
| Ambiente não encontrado | Sugerir ambiente similar |
| Área inválida | Solicitar correção |
| JSON inválido | Manter arquivos temp para debug |

## Nomenclatura de Arquivos

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Reforma específica | `reforma_{ambiente}_{tipo}.json` | `reforma_banheiro_apto.json` |
| Pintura | `pintura_{tipo}_{area}m2.json` | `pintura_apto_65m2.json` |
| Completa | `reforma_completa_{tipo}.json` | `reforma_completa_casa.json` |

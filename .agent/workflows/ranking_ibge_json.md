---
description: Workflow para gerar JSONs em lote a partir do ranking IBGE de reformas
---

# Workflow: Ranking IBGE JSON

## Objetivo
Para cada linha do arquivo `reforma_ibge_ranking_XX.csv`, gerar um arquivo JSON válido utilizando o workflow `json_reforma.md`.

## Skills Utilizadas

| Skill | Diretório | Função |
|-------|-----------|--------|
| IBGE | `.agent/skills/ibge` | Gerar ranking de reformas |
| JSON | `.agent/skills/json` | Converter e validar JSONs |

## Pré-requisitos
- Arquivo CSV de ranking (ex: `reforma_ibge_ranking_50.csv`)
- Estrutura de diretórios `.agent/skills/` configurada
- Listas de materiais e ambientes atualizadas

## Entrada
```
.agent/skills/ibge/examples/reforma_ibge_ranking_50.csv
```

## Saída
```
ranking_test_ott/
├── ranking_1.json
├── ranking_2.json
...
└── ranking_N.json
```

## Passos

### 1. Carregar CSV de Ranking
// turbo
```bash
python -c "
import csv
with open('.agent/skills/ibge/examples/reforma_ibge_ranking_50.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f\"ID: {row['id']} - {row['tipo']} - {row['área (ambiente)']}\")
"
```

### 2. Para cada linha do CSV, executar Workflow json_reforma

```python
# Pseudocódigo do loop
for row in ranking_csv:
    dados_imovel = {
        "id": row["id"],
        "tipo": row["tipo"],
        "ambiente": row["área (ambiente)"],
        "area_m2": float(row["area_m2"]),
        "acabamento": row["acabamento"],
        "descricao": row["descrição da reforma"]
    }
    
    # Executar workflow json_reforma
    resultado = executar_workflow("json_reforma", dados_imovel)
    
    # Salvar resultado
    salvar_json(f"ranking_{row['id']}.json", resultado)
```

### 3. Executar Script de Geração em Lote
// turbo
```bash
python .agent/skills/ibge/scripts/gerar_ranking_jsons.py --input reforma_ibge_ranking_50.csv --output ranking_test_ott/
```

### 4. Validar Todos os JSONs Gerados
// turbo
```bash
python .agent/skills/json/scripts/validar_json.py --dir ranking_test_ott/
```

### 5. Gerar Relatório de Processamento
// turbo
```bash
python .agent/skills/ibge/scripts/gerar_relatorio.py --dir ranking_test_ott/ --output relatorio_geracao.md
```

## Parâmetros de Execução

| Parâmetro | Valores | Descrição |
|-----------|---------|-----------|
| `--ranking` | 50, 100, 200, 500, 1000, 5000 | Quantidade de itens do ranking |
| `--output` | path | Diretório de saída |
| `--validate` | true/false | Validar JSONs após geração |
| `--report` | true/false | Gerar relatório MD |

## Exemplo de Execução Completa

```bash
# Gerar ranking de 50 itens com validação e relatório
python .agent/skills/ibge/scripts/gerar_ranking_jsons.py \
  --ranking 50 \
  --output ranking_test_ott/ \
  --validate true \
  --report true
```

## Métricas Esperadas

| Ranking | Arquivos | Tempo Estimado |
|---------|----------|----------------|
| 50 | 50 JSONs | ~30 segundos |
| 100 | 100 JSONs | ~1 minuto |
| 500 | 500 JSONs | ~5 minutos |
| 1000 | 1000 JSONs | ~10 minutos |
| 5000 | 5000 JSONs | ~50 minutos |

## Tratamento de Erros

| Erro | Ação |
|------|------|
| CSV não encontrado | Criar CSV padrão |
| Linha inválida | Pular e logar |
| JSON inválido | Salvar em `errors/` |
| Diretório inexistente | Criar automaticamente |

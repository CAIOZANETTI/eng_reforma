---
description: Workflow para criar um JSON de reforma válido no padrão Obra Ninja
---

# Workflow: JSON Reforma

## Objetivo
Gerar um arquivo JSON válido seguindo o padrão Obra Ninja a partir de um escopo de reforma.

## Saídas Finais
Apenas dois arquivos são gerados como output final:
- `{nome_projeto}.json` - JSON no padrão Obra Ninja
- `{nome_projeto}.md` - Relatório sintético do orçamento

## Estrutura de Diretórios

```
.agent/
├── output/                    # Saídas finais (apenas .json e .md)
│   ├── reforma_banheiro.json
│   └── reforma_banheiro.md
│
└── .temp/                     # Arquivos intermediários (não versionados)
    └── {uuid_execucao}/
        ├── imovel_input.json
        ├── quantidades.csv
        ├── escopo.csv
        └── escopo_custeado.csv
```

## Skills Utilizadas

| Skill | Diretório | Função |
|-------|-----------|--------|
| Quantificar | `.agent/skills/quantificar` | Calcular áreas e quantidades |
| Escopo | `.agent/skills/escopo` | Gerar escopo detalhado |
| Custo Reforma | `.agent/skills/custo_reforma` | Custear com SINAPI |
| JSON | `.agent/skills/json` | Converter para Obra Ninja |

## Pré-requisitos
- Dados do imóvel (tipo, área, acabamento)
- Escopo de reforma definido (ambientes e serviços)
- Acesso às listas de materiais e ambientes válidos

## Passos

### 1. Criar diretório temporário
// turbo
```bash
New-Item -ItemType Directory -Force -Path ".agent/.temp/{uuid}"
```

### 2. Validar Entrada
```python
# Verificar se o tipo de imóvel está na lista válida
tipos_validos = ["apto", "casa", "escritório", "loja", "clínica", "restaurante"]
```

### 3. Executar Skill: Quantificar
// turbo
```bash
python .agent/skills/quantificar/scripts/quantificar.py \
  --input .agent/.temp/{uuid}/imovel_input.json \
  --output .agent/.temp/{uuid}/quantidades.csv
```

### 4. Executar Skill: Escopo
// turbo
```bash
python .agent/skills/escopo/scripts/gerar_escopo.py \
  --input .agent/.temp/{uuid}/quantidades.csv \
  --output .agent/.temp/{uuid}/escopo.csv
```

### 5. Executar Skill: Custo Reforma
// turbo
```bash
python .agent/skills/custo_reforma/scripts/custear_reforma.py \
  --input .agent/.temp/{uuid}/escopo.csv \
  --output .agent/.temp/{uuid}/escopo_custeado.csv \
  --sintetico .agent/output/{nome_projeto}.md
```

### 6. Executar Skill: JSON
// turbo
```bash
python .agent/skills/json/scripts/converte_escopo_to_obra_ninja_json.py \
  --input .agent/.temp/{uuid}/escopo_custeado.csv \
  --output .agent/output/{nome_projeto}.json \
  --nome "{Título do Projeto}" \
  --descricao "{Descrição}"
```

### 7. Validar JSON
// turbo
```bash
python .agent/skills/json/scripts/validar_json.py \
  --input .agent/output/{nome_projeto}.json
```

### 8. Limpar arquivos temporários (opcional)
// turbo
```bash
Remove-Item -Recurse -Force ".agent/.temp/{uuid}"
```

### 9. Retornar Resultado
- Se válido: 
  - `.agent/output/{nome_projeto}.json`
  - `.agent/output/{nome_projeto}.md`
- Se inválido: retornar lista de erros

## Saída Esperada

```
.agent/output/
├── {nome_projeto}.json    ← JSON Obra Ninja válido
└── {nome_projeto}.md      ← Orçamento sintético
```

Exemplo:
```json
{
  "status": "success",
  "files": {
    "json": ".agent/output/reforma_banheiro.json",
    "md": ".agent/output/reforma_banheiro.md"
  },
  "validation": {
    "is_valid": true,
    "errors": [],
    "warnings": 0
  }
}
```

## Tratamento de Erros
| Erro | Ação |
|------|------|
| Ambiente não encontrado | Sugerir ambiente similar |
| Material não encontrado | Usar material genérico |
| Área inválida | Solicitar correção |
| JSON inválido | Manter arquivos temp para debug |

## Nomenclatura de Arquivos

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Reforma específica | `reforma_{ambiente}_{tipo}.json` | `reforma_banheiro_apto.json` |
| Pintura | `pintura_{tipo}_{area}m2.json` | `pintura_apto_65m2.json` |
| Completa | `reforma_completa_{tipo}.json` | `reforma_completa_casa.json` |

## Observações
- Arquivos intermediários são salvos em `.agent/.temp/` e podem ser deletados após execução
- Apenas `.json` e `.md` devem ser mantidos em `.agent/output/`
- Use nomes descritivos em snake_case para os arquivos de saída

# Plano de Implementação - Estrutura de Agentes Obra Ninja

> **Data**: 2026-01-29  
> **Versão**: 2.0  
> **Status**: Implementado

---

## 📋 Estrutura Final

```
.agent/
├── rules/
│   ├── reforma_sem_ampliacao.md
│   ├── uso_python_obrigatorio.md
│   └── seguir_template_obra_ninja.md
│
├── workflows/
│   ├── json_reforma.md
│   └── ranking_ibge_json.md
│
├── output/                    # Saídas finais (.json e .md apenas)
│
├── .temp/                     # Arquivos intermediários (não versionado)
│
└── skills/
    ├── ibge/                  # Dados de imóveis brasileiros
    ├── empreiteiro/           # Interface de prompts
    ├── projeto/               # Sugestões de projeto
    ├── quantificar/           # Cálculo de quantidades
    ├── escopo/                # Geração de escopo
    ├── custo_reforma/         # Custeio SINAPI
    ├── json/                  # Conversão e validação JSON
    └── variedades/            # Catálogo de possibilidades
```

---

## 🔄 Pipeline de Execução

```
┌─────────────────┐
│   ENTRADA       │
│  (Prompt User)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   empreiteiro   │  → Converte prompt em tabela estruturada
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      ibge       │  → Valida tipo de imóvel e consulta dados
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    projeto      │  → Sugere opções de reforma por padrão
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  quantificar    │  → Calcula áreas (piso, parede, etc.)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    escopo       │  → Gera escopo detalhado (CSV)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ custo_reforma   │  → Adiciona preços SINAPI
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│      json       │  → Converte para JSON Obra Ninja + Valida
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     SAÍDA       │
│ (.json + .md)   │
└─────────────────┘
```

---

## ✅ Checklist de Implementação

### Rules (3 arquivos) ✅ COMPLETO
- [x] `reforma_sem_ampliacao.md`
- [x] `uso_python_obrigatorio.md`
- [x] `seguir_template_obra_ninja.md`

### Workflows (2 arquivos) ✅ COMPLETO
- [x] `json_reforma.md`
- [x] `ranking_ibge_json.md`

### Skills - SKILL.md (8 módulos) ✅ COMPLETO
| Skill | Diretório | Status |
|-------|-----------|--------|
| Imóveis Brasil | `ibge/` | ✅ |
| Empreiteiro | `empreiteiro/` | ✅ |
| Projeto | `projeto/` | ✅ |
| Quantificar | `quantificar/` | ✅ |
| Escopo | `escopo/` | ✅ |
| Custo Reforma | `custo_reforma/` | ✅ |
| JSON | `json/` | ✅ |
| Variedades | `variedades/` | ✅ |

### Scripts - Implementação ✅ COMPLETO
| Script | Diretório | Status |
|--------|-----------|--------|
| `gerar_ranking.py` | `ibge/scripts/` | ✅ |
| `prompt_tabela.py` | `empreiteiro/scripts/` | ✅ |
| `quantificar.py` | `quantificar/scripts/` | ✅ |
| `gerar_escopo.py` | `escopo/scripts/` | ✅ |
| `custear_reforma.py` | `custo_reforma/scripts/` | ✅ |
| `converte_escopo_to_obra_ninja_json.py` | `json/scripts/` | ✅ |
| `validar_json.py` | `json/scripts/` | ✅ |
| `expandir_base.py` | `variedades/scripts/` | ✅ |
| `query_catalogo.py` | `variedades/scripts/` | ✅ |
| `validar_combinacao.py` | `variedades/scripts/` | ✅ |

### Resources - Arquivos de Dados ✅ COMPLETO
| Arquivo | Diretório | Status |
|---------|-----------|--------|
| `ambientes-29012026.csv` | `json/resources/` | ✅ |
| `materials-29012026.csv` | `json/resources/` | ✅ |
| `sinapi_2025.csv` | `custo_reforma/resources/` | ✅ |
| `faixas_area.json` | `variedades/resources/` | ✅ |
| `matriz_compatibilidade.csv` | `variedades/resources/` | ✅ |

---

## 📁 Mapeamento de Nomes (v1 → v2)

| Nome Antigo | Nome Novo |
|-------------|-----------|
| `imoveis_brasil/` | `ibge/` |
| `projeto_reformas/` | `projeto/` |
| `quantificar_reforma/` | `quantificar/` |
| `escopo_reforma/` | `escopo/` |
| `escopo_json/` | `json/` |
| `catalogo_reforma/` | `variedades/` |

---

## 🚀 Comandos de Uso

### Workflow JSON Reforma
```bash
# Quantificar
python .agent/skills/quantificar/scripts/quantificar.py \
  --input input.json --output quantidades.csv

# Gerar escopo
python .agent/skills/escopo/scripts/gerar_escopo.py \
  --input quantidades.csv --output escopo.csv

# Custear
python .agent/skills/custo_reforma/scripts/custear_reforma.py \
  --input escopo.csv --output custeado.csv --sintetico relatorio.md

# Converter para JSON
python .agent/skills/json/scripts/converte_escopo_to_obra_ninja_json.py \
  --input custeado.csv --output projeto.json

# Validar
python .agent/skills/json/scripts/validar_json.py \
  --input projeto.json
```

### Variedades (Catálogo)
```bash
# Gerar catálogos progressivos
python .agent/skills/variedades/scripts/expandir_base.py \
  --input ranking.csv --all

# Query no catálogo
python .agent/skills/variedades/scripts/query_catalogo.py \
  --tipo Casa --ambiente Cozinha --stats

# Validar combinação
python .agent/skills/variedades/scripts/validar_combinacao.py \
  --tipo Apto --ambiente Banheiro --area 5
```

---

## 📝 Notas

- Usar Python 3.10+ para todos os scripts
- Encoding UTF-8 em todos os arquivos
- Output final: apenas `.json` e `.md` em `.agent/output/`
- Arquivos intermediários em `.agent/.temp/` (ignorado pelo git)

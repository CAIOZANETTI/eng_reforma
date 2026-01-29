# Plano de Implementação - Estrutura de Agentes Obra Ninja

> **Data**: 2026-01-29  
> **Versão**: 2.1  
> **Status**: Implementado

---

## 📋 Estrutura Final (Numerada)

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
    ├── 01_empreiteiro/        # Entrada: prompt do cliente
    ├── 02_ibge/               # Dados de referência
    ├── 03_projeto/            # Sugestões de projeto
    ├── 04_quantificar/        # Cálculo de quantidades
    ├── 05_escopo/             # Geração de escopo
    ├── 06_custo/              # Custeio SINAPI
    ├── 07_json/               # Conversão e validação JSON
    └── aux_variedades/        # Catálogo de possibilidades (auxiliar)
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
│ 01_empreiteiro  │  → Converte prompt em tabela estruturada
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    02_ibge      │  → Valida tipo de imóvel e consulta dados
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   03_projeto    │  → Sugere opções de reforma por padrão
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 04_quantificar  │  → Calcula áreas (piso, parede, etc.)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   05_escopo     │  → Gera escopo detalhado (CSV)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   06_custo      │  → Adiciona preços SINAPI
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    07_json      │  → Converte para JSON Obra Ninja + Valida
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
| # | Skill | Diretório | Status |
|---|-------|-----------|--------|
| 01 | Empreiteiro | `01_empreiteiro/` | ✅ |
| 02 | IBGE | `02_ibge/` | ✅ |
| 03 | Projeto | `03_projeto/` | ✅ |
| 04 | Quantificar | `04_quantificar/` | ✅ |
| 05 | Escopo | `05_escopo/` | ✅ |
| 06 | Custo | `06_custo/` | ✅ |
| 07 | JSON | `07_json/` | ✅ |
| aux | Variedades | `aux_variedades/` | ✅ |

### Scripts - Implementação ✅ COMPLETO
| Script | Diretório | Status |
|--------|-----------|--------|
| `prompt_tabela.py` | `01_empreiteiro/scripts/` | ✅ |
| `gerar_ranking.py` | `02_ibge/scripts/` | ✅ |
| `quantificar.py` | `04_quantificar/scripts/` | ✅ |
| `gerar_escopo.py` | `05_escopo/scripts/` | ✅ |
| `custear_reforma.py` | `06_custo/scripts/` | ✅ |
| `converte_escopo_to_obra_ninja_json.py` | `07_json/scripts/` | ✅ |
| `validar_json.py` | `07_json/scripts/` | ✅ |
| `expandir_base.py` | `aux_variedades/scripts/` | ✅ |
| `query_catalogo.py` | `aux_variedades/scripts/` | ✅ |
| `validar_combinacao.py` | `aux_variedades/scripts/` | ✅ |

### Resources - Arquivos de Dados ✅ COMPLETO
| Arquivo | Diretório | Status |
|---------|-----------|--------|
| `ambientes-29012026.csv` | `07_json/resources/` | ✅ |
| `materials-29012026.csv` | `07_json/resources/` | ✅ |
| `sinapi_2025.csv` | `06_custo/resources/` | ✅ |
| `faixas_area.json` | `aux_variedades/resources/` | ✅ |
| `matriz_compatibilidade.csv` | `aux_variedades/resources/` | ✅ |

### Examples ✅ NOVO
| Arquivo | Diretório | Descrição |
|---------|-----------|-----------|
| `prompts_exemplo.md` | `01_empreiteiro/examples/` | 30+ prompts de exemplo |

---

## 🚀 Comandos de Uso

### Workflow JSON Reforma
```bash
# Quantificar
python .agent/skills/04_quantificar/scripts/quantificar.py \
  --input input.json --output quantidades.csv

# Gerar escopo
python .agent/skills/05_escopo/scripts/gerar_escopo.py \
  --input quantidades.csv --output escopo.csv

# Custear
python .agent/skills/06_custo/scripts/custear_reforma.py \
  --input escopo.csv --output custeado.csv --sintetico relatorio.md

# Converter para JSON
python .agent/skills/07_json/scripts/converte_escopo_to_obra_ninja_json.py \
  --input custeado.csv --output projeto.json

# Validar
python .agent/skills/07_json/scripts/validar_json.py \
  --input projeto.json
```

### Variedades (Catálogo)
```bash
# Gerar catálogos progressivos
python .agent/skills/aux_variedades/scripts/expandir_base.py \
  --input ranking.csv --all

# Query no catálogo
python .agent/skills/aux_variedades/scripts/query_catalogo.py \
  --tipo Casa --ambiente Cozinha --stats

# Validar combinação
python .agent/skills/aux_variedades/scripts/validar_combinacao.py \
  --tipo Apto --ambiente Banheiro --area 5
```

---

## 📝 Notas

- Usar Python 3.10+ para todos os scripts
- Encoding UTF-8 em todos os arquivos
- Output final: apenas `.json` e `.md` em `.agent/output/`
- Arquivos intermediários em `.agent/.temp/` (ignorado pelo git)
- Numeração das skills facilita entender a ordem do pipeline

# Plano de Implementação - Estrutura de Agentes Obra Ninja

> **Data**: 2026-01-31
> **Versão**: 3.0
> **Status**: Atualizado

---

## 📋 Estrutura de Diretórios

```
.agent/
├── rules/
│   ├── reforma_sem_ampliacao.md
│   ├── uso_python_obrigatorio.md
│   └── seguir_template_obra_ninja.md
│
├── workflows/
│   ├── json_reforma.md
│   ├── ranking_ibge_json.md
│   └── uma_reforma_aleatoria_json_obra_ninja.md
│
├── output/                    # Saídas finais (.json e .md apenas)
│
├── .temp/                     # Arquivos intermediários (não versionado)
│
└── skills/
    ├── empreitar/             # Entrada: prompt do cliente
    ├── mapear_imoveis/        # Dados de referência demográfica
    ├── projetar/              # Sugestões de projeto
    ├── quantificar/           # Cálculo de quantidades
    ├── detalhar/              # Geração de escopo
    ├── custear/               # Custeio SINAPI
    ├── exportar/              # Conversão e validação JSON
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
│    empreitar    │  → Converte prompt em tabela estruturada
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ mapear_imoveis  │  → Valida tipo de imóvel e consulta dados
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    projetar     │  → Sugere opções de reforma por padrão
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   quantificar   │  → Calcula áreas (piso, parede, etc.)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    detalhar     │  → Gera escopo detalhado (CSV)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     custear     │  → Adiciona preços SINAPI
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    exportar     │  → Converte para JSON Obra Ninja + Valida
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

### Workflows (3 arquivos) ✅ COMPLETO
- [x] `json_reforma.md`
- [x] `ranking_ibge_json.md`
- [x] `uma_reforma_aleatoria_json_obra_ninja.md`

### Skills - SKILL.md (8 módulos) ✅ COMPLETO
| Skill | Diretório | Status |
|-------|-----------|--------|
| Empreitar | `empreitar/` | ✅ |
| Mapeamento Imobiliário | `mapear_imoveis/` | ✅ |
| Projetar | `projetar/` | ✅ |
| Quantificar | `quantificar/` | ✅ |
| Detalhar | `detalhar/` | ✅ |
| Custear | `custear/` | ✅ |
| Exportar | `exportar/` | ✅ |
| Variedades | `aux_variedades/` | ✅ |

### Scripts - Implementação ✅ COMPLETO
| Script | Diretório | Status |
|--------|-----------|--------|
| `prompt_tabela.py` | `empreitar/scripts/` | ✅ |
| `gerar_ranking.py` | `mapear_imoveis/scripts/` | ✅ |
| `quantificar.py` | `quantificar/scripts/` | ✅ |
| `gerar_escopo.py` | `detalhar/scripts/` | ✅ |
| `custear_reforma.py` | `custear/scripts/` | ✅ |
| `converte_escopo_to_obra_ninja_json.py` | `exportar/scripts/` | ✅ |
| `validar_json.py` | `exportar/scripts/` | ✅ |
| `expandir_base.py` | `aux_variedades/scripts/` | ✅ |

### Resources - Arquivos de Dados ✅ COMPLETO
| Arquivo | Diretório | Status |
|---------|-----------|--------|
| `ambientes-29012026.csv` | `exportar/resources/` | ✅ |
| `materials-29012026.csv` | `exportar/resources/` | ✅ |
| `sinapi_2025.csv` | `custear/resources/` | ✅ |

---

## 🚀 Comandos de Uso

### Workflow Completo (Obra Ninja)
```bash
# Executar via workflow agent
/uma_reforma_aleatoria_json_obra_ninja
```

### Comandos Individuais
```bash
# Quantificar
python .agent/skills/quantificar/scripts/quantificar.py \
  --input input.json --output quantidades.csv

# Gerar escopo
python .agent/skills/detalhar/scripts/gerar_escopo.py \
  --input quantidades.csv --output escopo.csv

# Custear
python .agent/skills/custear/scripts/custear_reforma.py \
  --input escopo.csv --output custeado.csv --sintetico relatorio.md

# Converter para JSON
python .agent/skills/exportar/scripts/converte_escopo_to_obra_ninja_json.py \
  --input custeado.csv --output projeto.json
```

---

## 📝 Notas

- Skills renomeadas para verbos para indicar ação.
- Removida numeração de pastas para maior flexibilidade.
- Pipeline foca na geração de reformas a partir de tipos de imóveis reais (IBGE).

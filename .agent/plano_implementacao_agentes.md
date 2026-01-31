# Plano de Implementação - Estrutura de Agentes Obra Ninja

> **Data**: 2026-01-31
> **Versão**: 3.1
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
│   ├── uma_reforma_aleatoria_json_obra_ninja.md
│   └── minerar_base_conhecimento.md
│
├── knowledge_base/            # CSVs de conhecimento extraído
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
    ├── minerar_dados/         # Extração de padrões (Reverse Engineering)
    └── aux_variedades/        # Catálogo de possibilidades (auxiliar)
```

---

## 🔄 Pipeline de Mineração de Dados

```
┌─────────────────────────┐
│  OBRA NINJA JSONs       │
│  (Projetos Anteriores)  │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│     minerar_dados       │ → Lê JSONs e extrai:
│                         │   - materials.csv
│                         │   - labor.csv
│                         │   - services.csv
│                         │   - compositions.csv
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   KNOWLEDGE BASE (CSV)  │ → Base de consulta para
│                         │   novos projetos
└─────────────────────────┘
```

---

## ✅ Checklist de Implementação

### Rules (3 arquivos) ✅ COMPLETO
- [x] `reforma_sem_ampliacao.md`
- [x] `uso_python_obrigatorio.md`
- [x] `seguir_template_obra_ninja.md`

### Workflows (4 arquivos) ✅ COMPLETO
- [x] `json_reforma.md`
- [x] `ranking_ibge_json.md`
- [x] `uma_reforma_aleatoria_json_obra_ninja.md`
- [x] `minerar_base_conhecimento.md`

### Skills - SKILL.md (9 módulos) ✅ COMPLETO
| Skill | Diretório | Status |
|-------|-----------|--------|
| Empreitar | `empreitar/` | ✅ |
| Mapeamento Imobiliário | `mapear_imoveis/` | ✅ |
| Projetar | `projetar/` | ✅ |
| Quantificar | `quantificar/` | ✅ |
| Detalhar | `detalhar/` | ✅ |
| Custear | `custear/` | ✅ |
| Exportar | `exportar/` | ✅ |
| Minerar Dados | `minerar_dados/` | ✅ |
| Variedades | `aux_variedades/` | ✅ |

### Scripts - Implementação ✅ COMPLETO
| Script | Diretório | Status |
|--------|-----------|--------|
| `extrair_catalogos.py` | `minerar_dados/scripts/` | ✅ |
| `extrair_servicos.py` | `minerar_dados/scripts/` | ✅ |
| ... | ... | ✅ |

---

## 🚀 Comandos de Uso

### Minerar Base de Conhecimento
```bash
/minerar_base_conhecimento
```

---

## 📝 Notas

- O skill `minerar_dados` é essencial para popular a base inicial do sistema com dados reais de outros projetos.
- A pasta `.agent/knowledge_base` deve ser versionada pois contém o "cérebro" material do sistema.

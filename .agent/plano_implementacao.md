# Plano de Implementação - Estrutura de Agentes Obra Ninja

> **Data**: 2026-01-31
> **Versão**: 5.0
> **Status**: Em Refatoração

---

## 📋 Estrutura de Diretórios Reformulada

A estrutura foi simplificada para refletir exatamente os passos de negócio do Obra Ninja.

```
.agent/
├── rules/
│   ├── reforma_sem_ampliacao.md
│   ├── uso_python_obrigatorio.md
│   └── seguir_template_obra_ninja.md
│
├── workflows/
│   ├── criar_csv_base_conhecimento.md     # Baseado no modelo obra_ninja (mineração)
│   ├── uma_reforma_aleatoria.md           # Prompt -> Tabela -> Estimativa (MD)
│   └── converter_md_reforma_ninja_em_json.md # MD -> JSON Final
│
├── knowledge_base/                        # Extraído de obra_ninja/json
│   ├── property_type.csv                  # Tipos de imóvel (apartamento, casa...)
│   ├── services.csv                       # IDs de serviços (pintura_teto_branco...)
│   ├── material_category_id.csv           # Categorias de materiais (tinta-latex...)
│   ├── labor_categories.csv               # Categorias de mão de obra (pintor...)
│   ├── materials.csv                      # Materiais específicos
│   └── base_unit.csv                      # Unidades de medida (l, m², h...)
│
└── skills/
    ├── obra_ninja/            # "O Bibliotecário": Entende o modelo JSON e CSV, minera dados.
    ├── cria_orcamento/        # "O Arquiteto": Cria o orçamento em Markdown a partir de pedidos.
    ├── valida_orcamento/      # "O Engenheiro": Valida quantidades, preços e unidades.
    └── orcamento_obra_ninja/  # "O Integrador": Converte o orçamento validado para JSON final.
```

---

## 🔄 Fluxos de Trabalho (Workflows)

### 1. Criar Base de Conhecimento (`criar_csv_base_conhecimento.md`)
Responsável por ler a pasta `obra_ninja/json` e popular a `knowledge_base`.
- **Input**: `obra_ninja/json/*.json`
- **Skill**: `obra_ninja`
- **Output**: CSVs em `.agent/knowledge_base/`

### 2. Uma Reforma Aleatória (`uma_reforma_aleatoria.md`)
Simula o fluxo de um cliente pedindo uma reforma.
- **Input**: Prompt aleatório ou selecionado.
- **Skill**: `cria_orcamento` -> `valida_orcamento`
- **Output**: Relatório de Orçamento em Markdown (.md) com estimativa de valor.

### 3. Converter para JSON (`converter_md_reforma_ninja_em_json.md`)
Pega o relatório em Markdown e gera o JSON final para o sistema.
- **Input**: Orçamento (.md)
- **Skill**: `orcamento_obra_ninja`
- **Output**: JSON validado na pasta `output/`

---

## 📚 Dicionário de Dados (Mapeamento JSON -> CSV)

A base de conhecimento reflete a estrutura exata encontrada nos arquivos JSON:

### `property_type.csv`
Extraído de `template.property_type`.
- Ex: `apartamento`, `casa`, `sobrado`.

### `services.csv`
Extraído de `spaces[].services[].service_id` e `_name`.
- Ex: `pintura_teto_branco`, `demolicao_piso_ceramico`.

### `material_category_id.csv`
Extraído de `services[].material_categories[].material_category_id`.
- Define grupos de materiais intercambiáveis (ex: `tinta-latex-branca`).

### `labor_categories.csv`
Extraído de `services[].labor_categories[].labor_category_id`.
- Define tipos de profissionais (ex: `pintor`, `servente`).

### `base_unit.csv`
Extraído de todos os campos `base_unit`.
- Garante consistência nas unidades (ex: usar `l` e não `litros`).

---

## ✅ Checklist de Refatoração

### 1. Skill: Obra Ninja (`skills/obra_ninja`)
- [ ] Criar script `minerar_json.py`: Varrer JSONs e gerar os 6 CSVs principais.
- [ ] Validar se os CSVs batem com o schema do arquivo `banheiro_empregada_em_lavabo...json`.

### 2. Skill: Cria Orçamento (`skills/cria_orcamento`)
- [ ] Script `gerar_md_orcamento.py`: Usar `property_type.csv` e `services.csv` para montar um orçamento estruturado em Markdown.

### 3. Skill: Valida Orçamento (`skills/valida_orcamento`)
- [ ] Script `checar_unidades.py`: Verificar se as unidades do MD batem com `base_unit.csv`.

### 4. Skill: Orçamento Obra Ninja (`skills/orcamento_obra_ninja`)
- [ ] Script `md_to_json.py`: Converter a estrutura MD para o JSON final, preenchendo UUIDs se necessário.

---

## 🚀 Como Usar

```bash
# 1. Atualizar a inteligência do agente
/criar_csv_base_conhecimento

# 2. Gerar uma ideia de reforma
/uma_reforma_aleatoria

# 3. Exportar para o sistema
/converter_md_reforma_ninja_em_json
```

# Plano de Implementação - Estrutura de Agentes Obra Ninja

> **Data**: 2026-01-29  
> **Versão**: 1.0  
> **Status**: Em Planejamento

---

## 📋 Análise da Estrutura Proposta

### ✅ Pontos Positivos
1. **Modularidade**: Cada skill tem responsabilidade única e bem definida
2. **Padronização**: Estrutura consistente (skill.md, scripts/, exemplos/, resource/)
3. **Fluxo Lógico**: Pipeline claro do prompt até o JSON final
4. **Separação de Concerns**: Rules, Workflows e Skills bem separados

### ⚠️ Ajustes Recomendados
1. Renomear pastas para inglês (convenção): `exemplos` → `examples`, `resource` → `resources`
2. Adicionar skill de **validação** como etapa final do pipeline
3. Incluir **testes automatizados** para cada script
4. Criar **documentação de integração** entre skills

---

## 🏗️ Estrutura Final Proposta

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
└── skills/
    ├── imoveis_brasil/
    ├── empreiteiro/
    ├── projeto_reformas/
    ├── quantificar_reforma/
    ├── escopo_reforma/
    ├── custo_reforma/
    └── escopo_json/
```

---

## 📅 Cronograma de Implementação

### **FASE 1: Fundação (Dias 1-2)**
> Criar estrutura base e regras fundamentais

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 1.1 | Criar estrutura de diretórios | Todos os folders | 🔴 Alta |
| 1.2 | Implementar `reforma_sem_ampliacao.md` | rules/ | 🔴 Alta |
| 1.3 | Implementar `uso_python_obrigatorio.md` | rules/ | 🔴 Alta |
| 1.4 | Implementar `seguir_template_obra_ninja.md` | rules/ | 🔴 Alta |

---

### **FASE 2: Skills de Dados (Dias 3-5)**
> Criar base de dados e referências

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 2.1 | Skill `imoveis_brasil/SKILL.md` | skill.md | 🔴 Alta |
| 2.2 | Script ranking IBGE | scripts/gerar_ranking.py | 🔴 Alta |
| 2.3 | Tabelas de áreas | examples/areas_moradias.csv | 🟡 Média |
| 2.4 | Rankings CSV (50, 100, 200, 500, 1000, 5000) | examples/*.csv | 🟡 Média |
| 2.5 | Dados IBGE e SECOVI | resources/*.csv | 🟡 Média |

---

### **FASE 3: Skills de Interface (Dias 6-8)**
> Entrada de dados do usuário

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 3.1 | Skill `empreiteiro/SKILL.md` | skill.md | 🔴 Alta |
| 3.2 | Script `prompt_tabela.py` | scripts/ | 🔴 Alta |
| 3.3 | Exemplos de prompts | examples/prompts.md | 🟡 Média |
| 3.4 | Dicionário de linguagem | resources/linguagem_empreiteiro.md | 🟢 Baixa |

---

### **FASE 4: Skills de Projeto (Dias 9-12)**
> Lógica de projeto e opções de reforma

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 4.1 | Skill `projeto_reformas/SKILL.md` | skill.md | 🔴 Alta |
| 4.2 | Script área por classe social | scripts/area_classe.py | 🟡 Média |
| 4.3 | Lista de revestimentos e cores | examples/revestimentos.csv | 🟡 Média |
| 4.4 | Tendências (Pinterest, Airbnb, Retrofit) | examples/tendencias.md | 🟢 Baixa |
| 4.5 | Normas de acessibilidade | resources/acessibilidade.md | 🟡 Média |
| 4.6 | Paleta de cores e conforto | resources/design_interiores.md | 🟢 Baixa |
| 4.7 | Padrões de acabamento | resources/acabamentos.csv | 🔴 Alta |

---

### **FASE 5: Skills de Quantificação (Dias 13-16)**
> Cálculos e métricas

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 5.1 | Skill `quantificar_reforma/SKILL.md` | skill.md | 🔴 Alta |
| 5.2 | Script de quantificação | scripts/quantificar.py | 🔴 Alta |
| 5.3 | Exemplo de planilha output | examples/planilha_quantidades.csv | 🟡 Média |
| 5.4 | Normas de áreas e pé-direito | resources/normas_areas.md | 🟡 Média |

---

### **FASE 6: Skills de Escopo (Dias 17-19)**
> Definição do escopo da reforma

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 6.1 | Skill `escopo_reforma/SKILL.md` | skill.md | 🔴 Alta |
| 6.2 | Script de escopo | scripts/gerar_escopo.py | 🔴 Alta |
| 6.3 | Exemplo de escopo | examples/escopo_exemplo.csv | 🟡 Média |
| 6.4 | Conceitos e normas | resources/conceitos_escopo.md | 🟢 Baixa |

---

### **FASE 7: Skills de Custo (Dias 20-23)**
> Precificação baseada em SINAPI

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 7.1 | Skill `custo_reforma/SKILL.md` | skill.md | 🔴 Alta |
| 7.2 | Script de custeio | scripts/custear_reforma.py | 🔴 Alta |
| 7.3 | Tabela SINAPI atualizada | resources/sinapi_2025.csv | 🔴 Alta |
| 7.4 | Exemplo de orçamento | examples/orcamento_teste.csv | 🟡 Média |

---

### **FASE 8: Skills de Exportação JSON (Dias 24-27)**
> Conversão final para formato Obra Ninja

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 8.1 | Skill `escopo_json/SKILL.md` | skill.md | 🔴 Alta |
| 8.2 | Script conversor CSV→JSON | scripts/converte_escopo_to_obra_ninja_json.py | 🔴 Alta |
| 8.3 | Script validador JSON | scripts/validar_json.py | 🔴 Alta |
| 8.4 | Schema JSON | examples/obra_ninja_schema.json | 🔴 Alta |
| 8.5 | Lista de materiais válidos | resources/lista_materiais.csv | 🔴 Alta |
| 8.6 | Lista de ambientes válidos | resources/lista_ambientes.csv | 🔴 Alta |

---

### **FASE 9: Workflows (Dias 28-30)**
> Orquestração dos skills

| # | Tarefa | Arquivos | Prioridade |
|---|--------|----------|------------|
| 9.1 | Workflow `json_reforma.md` | workflows/ | 🔴 Alta |
| 9.2 | Workflow `ranking_ibge_json.md` | workflows/ | 🔴 Alta |
| 9.3 | Testes de integração | tests/ | 🟡 Média |

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
│  empreiteiro    │  → Converte prompt em tabela estruturada
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ imoveis_brasil  │  → Valida tipo de imóvel e consulta dados IBGE
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│projeto_reformas │  → Sugere opções de reforma por padrão
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│quantificar_     │  → Calcula áreas (piso, parede, etc.)
│reforma          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ escopo_reforma  │  → Gera escopo detalhado (CSV)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ custo_reforma   │  → Adiciona preços SINAPI
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  escopo_json    │  → Converte para JSON Obra Ninja + Valida
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     SAÍDA       │
│  (JSON válido)  │
└─────────────────┘
```

---

## 📁 Estrutura Detalhada de Cada Skill

### Template Padrão para SKILL.md

```yaml
---
name: [Nome do Skill]
description: [Descrição curta]
version: 1.0
dependencies: [Lista de outros skills necessários]
---

# [Nome do Skill]

## Objetivo
[Descrição do propósito]

## Entradas
- [Lista de inputs esperados]

## Saídas
- [Lista de outputs produzidos]

## Scripts Disponíveis
- `script_name.py`: [Descrição]

## Exemplos de Uso
[Código ou comandos de exemplo]

## Recursos Disponíveis
- [Lista de arquivos em resources/]
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

### Skills - SKILL.md (7 módulos) ✅ COMPLETO
- [x] `imoveis_brasil/SKILL.md`
- [x] `empreiteiro/SKILL.md`
- [x] `projeto_reformas/SKILL.md`
- [x] `quantificar_reforma/SKILL.md`
- [x] `escopo_reforma/SKILL.md`
- [x] `custo_reforma/SKILL.md`
- [x] `escopo_json/SKILL.md`

### Resources - Arquivos de Dados ✅ PARCIAL
- [x] `escopo_json/resources/lista_ambientes.csv` (78 ambientes)
- [x] `escopo_json/resources/lista_materiais.csv` (100 materiais)
- [x] `custo_reforma/resources/sinapi_2025.csv` (85 composições)
- [ ] `imoveis_brasil/resources/dados_ibge.csv`
- [ ] `projeto_reformas/resources/acabamentos.csv`

### Scripts - Implementação ⏳ PENDENTE
- [ ] `imoveis_brasil/scripts/gerar_ranking.py`
- [ ] `empreiteiro/scripts/prompt_tabela.py`
- [ ] `projeto_reformas/scripts/area_classe.py`
- [ ] `quantificar_reforma/scripts/quantificar.py`
- [ ] `escopo_reforma/scripts/gerar_escopo.py`
- [ ] `custo_reforma/scripts/custear_reforma.py`
- [ ] `escopo_json/scripts/converte_escopo_to_obra_ninja_json.py`
- [ ] `escopo_json/scripts/validar_json.py`

### Examples - Exemplos ⏳ PENDENTE
- [ ] Exemplos para cada skill

### Total Implementado: 15/40 arquivos (~38%)

---

## 🚀 Próximos Passos Imediatos

1. **Criar estrutura de diretórios** (FASE 1.1)
2. **Implementar as 3 regras** (FASE 1.2-1.4)
3. **Começar pelo skill `escopo_json`** (já temos o validador)
4. **Migrar código existente** para nova estrutura

---

## 📝 Notas

- Usar Python 3.10+ para todos os scripts
- Encoding UTF-8 em todos os arquivos
- Validação de JSON antes de salvar
- Logs detalhados para debug
- Testes unitários para cada script crítico

# Plano de Geração de Possibilidades de Reforma
## Universo de Reformas Residenciais no Brasil

---

## 📊 1. Análise Combinatória do Universo de Reformas

### 1.1 Dimensões do Espaço de Possibilidades

| Dimensão | Opções | Descrição |
|----------|--------|-----------|
| **Tipo de Imóvel** | 7 | Apto, Casa, Escritório, Loja, Clínica, Restaurante, Comercial genérico |
| **Configuração** | 10 | 1Q+1B, 2Q+1B, 2Q+2B, 3Q+2B, 3Q+3B, 4Q+3B, 0Q+1B, 0Q+2B, 0Q+4B, Especial |
| **Ambientes** | 78 | Conforme lista_ambientes.csv (banheiro, cozinha, sala, etc.) |
| **Áreas (faixas)** | 15 | 1-5m², 5-10m², 10-15m², 15-20m², 20-30m², 30-50m², 50-80m², 80-120m², 120-200m², 200-300m², etc. |
| **Padrão Acabamento** | 4 | Popular, Médio, Luxo, Comercial |
| **Escopo da Reforma** | 5 | Só Banheiro, Só Cozinha, Área Molhada, Áreas Sociais, Completa |

### 1.2 Cálculo do Universo Total

```
Combinações Teóricas = Tipos × Configs × Ambientes × Áreas × Acabamentos × Escopos
                     = 7 × 10 × 78 × 15 × 4 × 5
                     = 1.638.000 combinações brutas
```

**Porém, nem todas são válidas!** Filtros de realidade:
- Casa não tem "varanda gourmet de 2m²"
- Apto não tem "piscina"
- Escritório não tem "suíte master"
- Área mínima/máxima por ambiente

### 1.3 Combinações Válidas Estimadas

Após filtros de compatibilidade:

| Cenário | Combinações | % do Bruto |
|---------|-------------|------------|
| Extremamente restritivo | ~15.000 | 0.9% |
| Restritivo | ~45.000 | 2.7% |
| Moderado | ~120.000 | 7.3% |
| Permissivo | ~350.000 | 21% |

**Estimativa realista: 45.000 a 120.000 combinações válidas**

---

## 📈 2. Estratégia de Cobertura Progressiva

### 2.1 Metas de Cobertura

| Meta | Combinações | Descrição |
|------|-------------|-----------|
| **70%** | ~30-80 | Top ambientes × Top configurações × Acabamentos principais |
| **80%** | ~150-400 | + Variantes de área + Escopos adicionais |
| **90%** | ~500-2000 | + Comercial + Casos especiais |
| **95%** | ~3000-8000 | + Faixas de área detalhadas |
| **99%** | ~15000-50000 | + Todos os casos de nicho |
| **99.9%** | ~100.000+ | Cobertura quase total |

### 2.2 Priorização por Frequência Real (Dados IBGE/Mercado)

| Ranking | Categoria | % do Mercado |
|---------|-----------|--------------|
| 1 | Banheiro Apto | 18% |
| 2 | Cozinha Apto | 15% |
| 3 | Pintura Geral | 12% |
| 4 | Banheiro Casa | 10% |
| 5 | Cozinha Casa | 8% |
| 6 | Sala + Quartos | 7% |
| 7 | Área Molhada Completa | 6% |
| 8 | Elétrica/Hidráulica | 5% |
| 9 | Reforma Completa | 5% |
| 10 | Comercial | 5% |
| 11+ | Outros | 9% |

**Conclusão: 50 combinações bem escolhidas cobrem ~70% do mercado!**

---

## 🏗️ 3. Três Opções de Implementação

### OPÇÃO A: Skill `possibilidade_reforma`
**Abordagem: Gerador Combinatório Dinâmico**

```
.agent/skills/possibilidade_reforma/
├── SKILL.md
├── scripts/
│   ├── gerar_combinacoes.py      # Gera combinações válidas
│   ├── validar_combinacao.py     # Valida se combinação faz sentido
│   ├── ranquear_frequencia.py    # Ordena por probabilidade de mercado
│   └── exportar_catalogo.py      # Exporta para CSV/JSON
├── resources/
│   ├── matriz_compatibilidade.csv   # O que pode combinar com o quê
│   ├── frequencia_mercado.csv       # Pesos de frequência
│   └── restricoes_fisicas.json      # Limites de área por ambiente
└── examples/
    ├── catalogo_70pct.csv           # 50 combinações top
    ├── catalogo_80pct.csv           # 200 combinações
    └── catalogo_95pct.csv           # 5000 combinações
```

**Prós:**
- Máxima flexibilidade
- Pode gerar sob demanda
- Fácil manutenção de regras

**Contras:**
- Mais complexo de implementar
- Precisa validação cuidadosa

---

### OPÇÃO B: Workflow `catalogo_reformas`
**Abordagem: Curadoria Manual + Expansão Algorítmica**

```
.agent/workflows/catalogo_reformas.md

Etapas:
1. Curar manualmente 50 combinações "ouro" (baseado no ranking atual)
2. Para cada combinação "ouro", gerar variantes:
   - 3 faixas de área (pequeno, médio, grande)
   - 3 acabamentos (popular, médio, luxo)
   = 50 × 3 × 3 = 450 combinações
3. Adicionar comercial (20 tipos × 3 áreas × 1 acabamento = 60)
4. Total: ~510 combinações = ~80% cobertura

Para atingir 90%+:
5. Expandir lista base para 100 combinações "ouro"
6. Adicionar variantes: 100 × 9 = 900 + comercial = ~1000

Para 99%:
7. Mapear TODOS os ambientes vs TODAS as configurações válidas
8. Usar matriz de compatibilidade
```

**Prós:**
- Controle total sobre qualidade
- Combinações sempre fazem sentido
- Mais fácil de revisar

**Contras:**
- Trabalho manual inicial maior
- Menos escalável infinitamente

---

### OPÇÃO C: Híbrido com Regras de Negócio
**Abordagem: Base Curada + Geração Controlada por Regras**

```
Sistema em 3 camadas:

CAMADA 1 - Base Curada (50-200 combinações)
├── Criadas manualmente
├── Validadas por especialista
├── Representam 70-80% do mercado
└── Arquivo: catalogo_base.csv

CAMADA 2 - Expansão por Regras (200-2000 combinações)
├── Script aplica variações sobre base
├── Regras: acabamento, área, escopo
├── Filtra por matriz de compatibilidade
└── Arquivo: catalogo_expandido.csv

CAMADA 3 - Geração Dinâmica (2000+ combinações)
├── Para casos não cobertos
├── Gera sob demanda via API
├── Valida antes de retornar
└── Função: gerar_combinacao_custom()
```

**Prós:**
- Melhor custo-benefício
- Cobertura garantida para maioria
- Flexível para exceções

**Contras:**
- Complexidade média
- 3 sistemas a manter

---

## 🎯 4. Recomendação

### Recomendação: **OPÇÃO C (Híbrido)** com implementação em fases:

| Fase | Meta | Entregáveis | Esforço |
|------|------|-------------|---------|
| **Fase 1** | 70% | 50 combinações curadas (já existe no ranking!) | 1 dia |
| **Fase 2** | 80% | Script de expansão = 200 combinações | 2 dias |
| **Fase 3** | 90% | + Comercial + casos especiais = 1000 | 3 dias |
| **Fase 4** | 95% | Matriz completa + gerador = 5000 | 5 dias |
| **Fase 5** | 99%+ | API de geração dinâmica | 8 dias |

### Estrutura Proposta

```
.agent/skills/catalogo_reforma/
├── SKILL.md
├── scripts/
│   ├── expandir_base.py           # Fase 2: gera variantes
│   ├── gerar_matriz.py            # Fase 4: matriz completa
│   ├── validar_combinacao.py      # Valida qualquer combinação
│   └── query_catalogo.py          # Busca no catálogo
├── resources/
│   ├── base_curada.csv            # 175 linhas existentes!
│   ├── matriz_tipo_ambiente.csv   # Compatibilidade
│   ├── faixas_area.json           # Áreas válidas por ambiente
│   └── frequencia_ibge.csv        # Pesos de mercado
└── catalogo/
    ├── 70pct_top50.csv
    ├── 80pct_200.csv
    ├── 90pct_1000.csv
    └── full_catalogo.csv
```

---

## 📋 5. Quantificação Final

### Estimativa de Combinações por Meta

| Meta | Lógica | Quantidade |
|------|--------|------------|
| **70%** | 6 ambientes principais × 5 configs × 2 acabamentos | **~60** |
| **80%** | + 4 áreas × 2 escopos = 60 × 8 | **~200** |
| **90%** | + 10 ambientes secundários × variantes | **~1.000** |
| **95%** | + Todos ambientes × acabamentos válidos | **~5.000** |
| **99%** | + Todas faixas de área × combinações válidas | **~25.000** |
| **99.9%** | + Exceções e casos raros | **~100.000** |

### O Ranking Atual Já Cobre:

```
Arquivo: lista_reforma_ranking.csv
Linhas: 175 combinações curadas
Cobertura estimada: 75-80% do mercado brasileiro
```

**Você já está na meta de 80%!** O próximo passo é expandir algoritmicamente.

---

## ✅ 6. Próximos Passos Recomendados

1. **Validar o ranking atual** (175 linhas) como "base curada"
2. **Criar skill `catalogo_reforma`** com estrutura proposta
3. **Implementar `expandir_base.py`** para gerar variantes
4. **Criar matriz de compatibilidade** tipo_imovel × ambiente
5. **Gerar catálogo de 1000 combinações** para meta de 90%
6. **Testar pipeline completo** com as novas combinações

---

## 📊 Resumo das 3 Opções

| Critério | Opção A: Skill | Opção B: Workflow | Opção C: Híbrido |
|----------|----------------|-------------------|------------------|
| Complexidade | Alta | Média | Média |
| Manutenibilidade | Média | Alta | Alta |
| Escalabilidade | Alta | Baixa | Alta |
| Tempo inicial | 5 dias | 3 dias | 2 dias |
| Cobertura 99%+ | Sim | Difícil | Sim |
| **Recomendação** | Para futuro | Não ideal | ✅ **Recomendado** |


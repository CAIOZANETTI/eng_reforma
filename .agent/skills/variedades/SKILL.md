---
name: Catálogo de Reformas
description: Gerar e gerenciar catálogo de possibilidades de reforma com cobertura progressiva
---

# Skill: Catálogo de Reformas

## Objetivo
Gerar, expandir e consultar um catálogo completo de possibilidades de reforma residencial e comercial no Brasil, com metas de cobertura progressiva (70%, 80%, 90%, 95%, 99%).

## Arquitetura em 3 Camadas

### Camada 1 - Base Curada
- **Fonte**: `obra_ninja/csv/lista_reforma/lista_reforma_ranking.csv`
- **Linhas**: 175 combinações validadas manualmente
- **Cobertura**: ~75-80% do mercado

### Camada 2 - Expansão por Regras
- **Script**: `expandir_base.py`
- **Lógica**: Aplica variações de área, acabamento e escopo
- **Output**: 500-2000 combinações
- **Cobertura**: ~90%

### Camada 3 - Geração Dinâmica
- **Script**: `gerar_combinacao.py`
- **Lógica**: Valida e gera combinações sob demanda
- **Output**: Qualquer combinação válida
- **Cobertura**: ~99%+

## Inputs

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `--meta` | 70/80/90/95/99 | Meta de cobertura desejada |
| `--tipo` | apto/casa/comercial | Filtro por tipo de imóvel |
| `--ambiente` | string | Filtro por ambiente específico |
| `--acabamento` | popular/medio/luxo | Filtro por acabamento |
| `--area_min` | float | Área mínima em m² |
| `--area_max` | float | Área máxima em m² |

## Outputs

| Arquivo | Descrição |
|---------|-----------|
| `catalogo/catalogo_70pct.csv` | Top 50 combinações |
| `catalogo/catalogo_80pct.csv` | 200 combinações |
| `catalogo/catalogo_90pct.csv` | 1000 combinações |
| `catalogo/catalogo_95pct.csv` | 5000 combinações |
| `catalogo/catalogo_full.csv` | Todas as combinações válidas |

## Scripts Disponíveis

### 1. expandir_base.py
Expande a base curada aplicando variações.

```bash
python .agent/skills/catalogo_reforma/scripts/expandir_base.py \
  --input obra_ninja/csv/lista_reforma/lista_reforma_ranking.csv \
  --output .agent/skills/catalogo_reforma/catalogo/catalogo_90pct.csv \
  --meta 90
```

### 2. validar_combinacao.py
Valida se uma combinação é fisicamente possível.

```bash
python .agent/skills/catalogo_reforma/scripts/validar_combinacao.py \
  --tipo apto \
  --ambiente "Banheiro" \
  --area 5 \
  --acabamento Luxo
```

### 3. query_catalogo.py
Busca combinações no catálogo.

```bash
python .agent/skills/catalogo_reforma/scripts/query_catalogo.py \
  --tipo casa \
  --ambiente "Cozinha" \
  --acabamento Medio \
  --limit 10
```

### 4. gerar_combinacao.py
Gera combinação válida sob demanda.

```bash
python .agent/skills/catalogo_reforma/scripts/gerar_combinacao.py \
  --tipo apto \
  --config "2Q+1B" \
  --ambientes "Banheiro,Cozinha" \
  --acabamento Luxo
```

## Resources

| Arquivo | Descrição |
|---------|-----------|
| `matriz_compatibilidade.csv` | Tipo × Ambiente válidos |
| `faixas_area.json` | Áreas min/max por ambiente |
| `frequencia_mercado.csv` | Peso de frequência por combinação |
| `restricoes.json` | Regras de incompatibilidade |

## Matriz de Compatibilidade

```
           | Banheiro | Cozinha | Sala | Suíte | Varanda | Piscina | Telhado |
-----------|----------|---------|------|-------|---------|---------|---------|
Apto       |    ✓     |    ✓    |  ✓   |   ✓   |    ✓    |    ✗    |    ✗    |
Casa       |    ✓     |    ✓    |  ✓   |   ✓   |    ✓    |    ✓    |    ✓    |
Escritório |    ✓     |    ✓    |  ✗   |   ✗   |    ✗    |    ✗    |    ✗    |
Loja       |    ✓     |    ✗    |  ✗   |   ✗   |    ✗    |    ✗    |    ✗    |
```

## Metas de Cobertura

| Meta | Combinações | Estratégia |
|------|-------------|------------|
| 70% | 50 | Top 6 ambientes × configs principais |
| 80% | 200 | + variantes de área e acabamento |
| 90% | 1000 | + comercial + casos especiais |
| 95% | 5000 | + matriz completa de compatibilidade |
| 99% | 25000 | + todas faixas de área |

## Exemplo de Uso no Pipeline

```python
from catalogo_reforma import CatalogoReforma

catalogo = CatalogoReforma()

# Carregar base curada
catalogo.carregar_base("lista_reforma_ranking.csv")

# Expandir para meta de 90%
catalogo.expandir(meta=90)

# Exportar catálogo
catalogo.exportar("catalogo_90pct.csv")

# Consultar
resultados = catalogo.query(
    tipo="apto",
    ambiente="Banheiro",
    acabamento="Luxo"
)
```

## Integração com Pipeline

```
[Cliente] → [Empreiteiro] → [Catálogo Reforma] → [Quantificar] → [Escopo] → [Custo] → [JSON]
                                   ↓
                          Busca combinação
                          mais próxima ou
                          gera nova válida
```

## Regras de Negócio

1. **Área mínima**: Cada ambiente tem área mínima física
2. **Compatibilidade tipo-ambiente**: Nem todo ambiente existe em todo tipo
3. **Acabamento válido**: Comercial só aceita acabamento "Comercial"
4. **Configuração lógica**: 1Q+1B não tem suíte master

## Próximos Passos

1. ✅ Criar estrutura de diretórios
2. ⏳ Implementar `expandir_base.py`
3. ⏳ Criar matriz de compatibilidade
4. ⏳ Gerar catálogos progressivos
5. ⏳ Implementar validação e query

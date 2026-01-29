---
name: Imóveis Brasil
description: Rastrear tipos de moradia no Brasil e criar opções de reforma baseadas em ranking IBGE
version: 1.0
dependencies: []
---

# Skill: Imóveis Brasil

## Objetivo
Fornecer dados demográficos e estatísticos sobre imóveis no Brasil, permitindo a criação de opções de reforma baseadas em rankings do IBGE.

## Entradas
- Tipo de consulta (ranking por quantidade, por região, por tipo)
- Quantidade de itens desejada (50, 100, 200, 500, 1000, 5000)
- Filtros opcionais (tipo de imóvel, padrão de acabamento)

## Saídas
- Rankings de tipos de moradia em CSV
- Estatísticas de áreas por tipo de imóvel
- Dados de tendências de reforma

## Scripts Disponíveis

### `scripts/gerar_ranking.py`
Gera ranking de tipos de reforma mais comuns baseado em dados IBGE.

```bash
python gerar_ranking.py --quantidade 50 --output reforma_ibge_ranking_50.csv
```

### `scripts/gerar_ranking_jsons.py`
Processa CSV de ranking e gera JSONs para cada item.

```bash
python gerar_ranking_jsons.py --input ranking.csv --output dir/
```

### `scripts/gerar_relatorio.py`
Gera relatório MD a partir dos JSONs gerados.

```bash
python gerar_relatorio.py --dir ranking_test_ott/ --output relatorio.md
```

## Exemplos Disponíveis

| Arquivo | Descrição |
|---------|-----------|
| `examples/areas_moradias.csv` | Áreas médias por tipo de imóvel |
| `examples/reforma_ibge_ranking_50.csv` | Top 50 tipos de reforma |
| `examples/reforma_ibge_ranking_100.csv` | Top 100 tipos de reforma |
| `examples/reforma_ibge_ranking_200.csv` | Top 200 tipos de reforma |
| `examples/reforma_ibge_ranking_500.csv` | Top 500 tipos de reforma |
| `examples/reforma_ibge_ranking_1000.csv` | Top 1000 tipos de reforma |
| `examples/reforma_ibge_ranking_5000.csv` | Top 5000 tipos de reforma |

## Recursos Disponíveis

| Arquivo | Fonte | Descrição |
|---------|-------|-----------|
| `resources/dados_ibge.csv` | IBGE | Dados demográficos de moradias |
| `resources/dados_secovi.csv` | SECOVI | Dados do mercado imobiliário |
| `resources/metodologia_ibge.md` | - | Metodologia de classificação |

## Estrutura de Dados

### áreas_moradias.csv
```csv
tipo,padrao,area_media_m2,n_quartos,n_banheiros
Apto,Popular,45,1,1
Apto,Médio,65,2,1
Apto,Luxo,120,3,2
Casa,Popular,70,2,1
Casa,Médio,120,3,2
Casa,Luxo,250,4,3
```

### ranking.csv
```csv
id,tipo,área (ambiente),area_m2,qtd_imovel,acabamento,descrição
1,Apto,Banheiro,4,1Q+1B,Popular,Reforma básica...
```

## Regras de Negócio

1. **Áreas Mínimas por Ambiente**
   - Banheiro: 2.5 m²
   - Quarto: 8 m²
   - Sala: 12 m²
   - Cozinha: 4 m²

2. **Proporções Típicas**
   - Banheiro: 8-12% da área total
   - Quartos: 25-35% da área total
   - Sala: 20-30% da área total
   - Cozinha: 10-15% da área total

3. **Classificação por Padrão**
   - Popular: até R$ 1.500/m²
   - Médio: R$ 1.500 a R$ 3.000/m²
   - Luxo: acima de R$ 3.000/m²

## Uso no Pipeline

Este skill é tipicamente o primeiro a ser executado, fornecendo a base de dados para os demais skills processarem.

```
imoveis_brasil → empreiteiro → projeto_reformas → quantificar_reforma → escopo_reforma → custo_reforma → escopo_json
```

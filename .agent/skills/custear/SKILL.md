---
name: Custear
description: Custear reforma com base nos preços SINAPI
version: 1.0
dependencies: [detalhar]
---

# Skill: Custear

## Objetivo
Adicionar preços unitários (baseados na tabela SINAPI) ao escopo de reforma, calculando custo parcial e total.

## Entradas
- Escopo de reforma (CSV do escopo_reforma)
- Tabela SINAPI atualizada
- Região/Estado (para variação de preços)
- BDI opcional (default 25%)

## Saídas
- Escopo custeado (CSV)
- Resumo de custos
- Relatório sintético (MD)
- Relatório analítico (MD)

## Scripts Disponíveis

### `scripts/custear_reforma.py`
Adiciona preços ao escopo.

```bash
python custear_reforma.py --input escopo.csv --sinapi sinapi_2025.csv --bdi 0.25 --output escopo_custeado.csv
```

**Saída (escopo_custeado.csv):**
```csv
item,ambiente,servico,descricao,unidade,quantidade,preco_unitario,preco_parcial
1,Banheiro,Demolição,Demolição de revestimentos,m²,26.44,35.80,946.55
2,Banheiro,Impermeabilização,Manta asfáltica,m²,6.5,85.00,552.50
3,Banheiro,Contrapiso,Regularização,m²,5.0,42.00,210.00
...
TOTAL,,,,,,,8.500.00
```

### `scripts/gerar_relatorio_sinapi.py`
Gera relatórios em formato Markdown.

```bash
python gerar_relatorio_sinapi.py --input escopo_custeado.csv --sintetico relatorio_sintetico.md --analitico relatorio_analitico.md
```

### `scripts/atualizar_sinapi.py`
Atualiza tabela SINAPI com novos preços.

```bash
python atualizar_sinapi.py --mes 01 --ano 2025 --estado SP
```

## Exemplos Disponíveis

### `examples/orcamento_teste.csv`
Exemplo de orçamento completo de reforma de banheiro.

### `examples/relatorio_sintetico.md`
```markdown
# Orçamento Sintético

| Item | Descrição | Unid. | Qtd | Preço Unit. | Preço Total |
|------|-----------|-------|-----|-------------|-------------|
| 1 | Demolição de revestimentos | m² | 26.44 | R$ 35,80 | R$ 946,55 |
| 2 | Impermeabilização | m² | 6.50 | R$ 85,00 | R$ 552,50 |
...
| | **TOTAL** | | | | **R$ 8.500,00** |
```

### `examples/relatorio_analitico.md`
```markdown
# Orçamento Analítico

## 1. Demolição de Revestimentos
- **Código SINAPI**: 97622
- **Descrição**: Demolição de revestimento cerâmico
- **Unidade**: m²
- **Quantidade**: 26.44
- **Composição**:
  | Insumo | Unid. | Coef. | Preço | Subtotal |
  |--------|-------|-------|-------|----------|
  | Servente | h | 0.35 | 18.50 | 6.48 |
  | Energia | kWh | 0.12 | 0.85 | 0.10 |
  | Ferramenta | % | 0.02 | - | 0.71 |
- **Total Unitário**: R$ 35,80
- **Total Item**: R$ 946,55
```

## Recursos Disponíveis

### `resources/sinapi_2025.csv`
```csv
codigo,descricao,unidade,preco_material,preco_mo,preco_total,grupo
97622,Demolição de revestimento cerâmico,m²,0.00,35.80,35.80,Demolição
88309,Pedreiro,h,0.00,21.45,21.45,Mão de obra
88316,Servente,h,0.00,18.50,18.50,Mão de obra
87878,Porcelanato 60x60 assentado,m²,95.00,42.00,137.00,Revestimento
```

### `resources/bdi.md`
Explicação do BDI (Bonificação e Despesas Indiretas).

```markdown
## Composição do BDI

| Item | Percentual |
|------|------------|
| Administração Central | 4% |
| Seguros | 0.8% |
| Garantias | 0.8% |
| Riscos | 1% |
| Despesas Financeiras | 1.2% |
| Lucro | 8% |
| ISS | 5% |
| PIS | 0.65% |
| COFINS | 3% |
| CPRB | 4.5% |
| **Total BDI** | **28.95%** |

Para reformas residenciais, usa-se BDI simplificado de 20-30%.
```

## Fórmulas de Cálculo

### Preço Unitário com BDI
```python
preco_com_bdi = preco_sinapi * (1 + bdi)
```

### Preço Parcial
```python
preco_parcial = quantidade * preco_unitario
```

### Preço Total
```python
preco_total = sum(todos_precos_parciais)
```

## Uso no Pipeline

```
detalhar \u2192 custear \u2192 exportar
```

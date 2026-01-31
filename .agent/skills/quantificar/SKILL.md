---
name: Quantificar
description: Calcular quantidades de serviços baseado na área e tipo do imóvel
version: 1.0
dependencies: [projetar]
---

# Skill: Quantificar

## Objetivo
Com base na área e tipo do imóvel, calcular as quantidades de cada serviço: área de piso, parede, perímetro, janelas, portas, etc.

## Entradas
- Área do ambiente (m²)
- Tipo de ambiente (banheiro, sala, cozinha, etc.)
- Pé-direito (default 2.6m para apto, 2.8m para casa)
- Proporção de janelas/portas (opcional)

## Saídas
- Área de piso (m²)
- Área de parede bruta (m²)
- Área de parede líquida (descontando aberturas) (m²)
- Perímetro (m)
- Área de teto (m²)
- Quantidade de portas (un)
- Quantidade de janelas (un)
- Área de janelas (m²)

## Scripts Disponíveis

### `scripts/quantificar.py`
Calcula todas as quantidades de um ambiente.

```bash
python quantificar.py --ambiente banheiro --area 5 --pe_direito 2.6
```

**Saída:**
```json
{
  "ambiente": "banheiro",
  "area_piso": 5.0,
  "perimetro": 9.0,
  "area_parede_bruta": 23.4,
  "aberturas": {
    "portas": 1,
    "area_portas": 1.6,
    "janelas": 1,
    "area_janelas": 0.36
  },
  "area_parede_liquida": 21.44,
  "area_teto": 5.0
}
```

### `scripts/quantificar_imovel.py`
Processa um imóvel completo.

```bash
python quantificar_imovel.py --input imovel.json --output quantidades.csv
```

## Exemplos Disponíveis

### `examples/planilha_quantidades.csv`
```csv
ambiente,area_piso,perimetro,area_parede,area_teto,portas,janelas
Sala,22.0,18.8,42.68,22.0,2,2
Quarto 1,12.0,14.0,30.00,12.0,1,1
Banheiro,5.0,9.0,21.44,5.0,1,1
Cozinha,8.0,11.4,25.64,8.0,1,1
```

### `examples/imovel_exemplo.json`
```json
{
  "tipo": "apto",
  "area_total": 55,
  "pe_direito": 2.6,
  "ambientes": [
    {"nome": "Sala", "area": 18},
    {"nome": "Quarto", "area": 12},
    {"nome": "Cozinha", "area": 8},
    {"nome": "Banheiro", "area": 4}
  ]
}
```

## Recursos Disponíveis

### `resources/normas_areas.md`
```markdown
## Áreas Mínimas (NBR 15575)

| Ambiente | Área Mínima | Pé-Direito Mínimo |
|----------|-------------|-------------------|
| Sala | 8.0 m² | 2.50 m |
| Quarto casal | 8.0 m² | 2.50 m |
| Quarto solteiro | 6.0 m² | 2.50 m |
| Cozinha | 4.0 m² | 2.50 m |
| Banheiro | 2.4 m² | 2.30 m |
| Lavanderia | 2.0 m² | 2.30 m |

## Aberturas Típicas

| Ambiente | Portas | Janelas |
|----------|--------|---------|
| Sala | 1-2 | 1-2 |
| Quarto | 1 | 1 |
| Cozinha | 1 | 1 |
| Banheiro | 1 | 0-1 |
```

## Fórmulas de Cálculo

### Perímetro Aproximado
Para ambientes retangulares com proporção 2:3:
```python
perimetro = 2 * (largura + comprimento)
# onde: largura = sqrt(area * 2/3), comprimento = sqrt(area * 3/2)
```

### Área de Parede Bruta
```python
area_parede_bruta = perimetro * pe_direito
```

### Área de Parede Líquida
```python
area_parede_liquida = area_parede_bruta - (n_portas * 1.6) - (n_janelas * area_janela)
```

### Dimensões de Aberturas Padrão
| Tipo | Largura | Altura | Área |
|------|---------|--------|------|
| Porta interna | 0.80 m | 2.10 m | 1.68 m² |
| Porta entrada | 0.90 m | 2.10 m | 1.89 m² |
| Janela quarto | 1.20 m | 1.20 m | 1.44 m² |
| Janela banheiro | 0.60 m | 0.60 m | 0.36 m² |
| Janela cozinha | 1.00 m | 1.00 m | 1.00 m² |

## Uso no Pipeline

```
projetar \u2192 quantificar \u2192 detalhar
```

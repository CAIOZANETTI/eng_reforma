---
name: Detalhar
description: Gerar escopo detalhado de reforma com base nas quantidades calculadas
version: 1.0
dependencies: [quantificar]
---

# Skill: Detalhar

## Objetivo
Com base nas quantidades calculadas, gerar um escopo detalhado de serviços para a reforma, definindo o que será feito em cada ambiente.

## Entradas
- Quantidades calculadas (output do quantificar_reforma)
- Tipo de reforma por ambiente
- Padrão de acabamento
- Serviços selecionados

## Saídas
- Escopo detalhado em CSV
- Lista de serviços por ambiente
- Quantidades por serviço
- Unidades de medida

## Scripts Disponíveis

### `scripts/gerar_escopo.py`
Gera escopo a partir das quantidades.

```bash
python gerar_escopo.py --input quantidades.csv --reforma banheiro_completo --acabamento medio --output escopo.csv
```

**Saída (escopo.csv):**
```csv
item,ambiente,servico,descricao,unidade,quantidade
1,Banheiro,Demolição,Demolição de revestimentos,m²,26.44
2,Banheiro,Impermeabilização,Manta asfáltica,m²,5.0
3,Banheiro,Contrapiso,Regularização,m²,5.0
4,Banheiro,Piso,Porcelanato 60x60,m²,5.0
5,Banheiro,Parede,Porcelanato 60x60,m²,21.44
6,Banheiro,Rejunte,Rejunte epóxi,m²,26.44
7,Banheiro,Louças,Vaso sanitário,un,1
8,Banheiro,Louças,Cuba de apoio,un,1
9,Banheiro,Metais,Torneira monocomando,un,1
10,Banheiro,Metais,Ducha higiênica,un,1
11,Banheiro,Box,Vidro temperado 8mm,m²,2.0
12,Banheiro,Pintura,Pintura de teto,m²,5.0
```

### `scripts/templates_escopo.py`
Retorna templates de escopo por tipo de reforma.

```bash
python templates_escopo.py --tipo banheiro_completo
```

## Exemplos Disponíveis

### `examples/escopo_exemplo.csv`
Exemplo completo de escopo de reforma de banheiro.

### `examples/templates/`
```
templates/
├── banheiro_basico.json
├── banheiro_completo.json
├── banheiro_luxo.json
├── cozinha_basica.json
├── cozinha_completa.json
├── sala_pintura.json
├── sala_completa.json
└── geral_pintura.json
```

## Recursos Disponíveis

### `resources/conceitos_escopo.md`
```markdown
## Tipos de Escopo por Ambiente

### Banheiro
1. **Básico**: Pintura + troca de louças/metais
2. **Parcial**: Troca de revestimento do box + louças
3. **Completo**: Demolição total + novo revestimento + louças + metais
4. **Premium**: Completo + nicho + iluminação + aquecimento

### Cozinha
1. **Básica**: Pintura + bancada
2. **Parcial**: Revestimento área molhada + bancada
3. **Completa**: Piso + parede + marcenaria
4. **Premium**: Completa + ilha + eletros embutidos

### Sala
1. **Pintura**: Apenas pintura
2. **Piso**: Piso + rodapé
3. **Completa**: Piso + pintura + forro + iluminação
```

## Templates de Serviços

### Banheiro Completo
```json
{
  "nome": "banheiro_completo",
  "servicos": [
    {"servico": "Demolição", "formula": "area_piso + area_parede", "unidade": "m²"},
    {"servico": "Impermeabilização", "formula": "area_piso * 1.3", "unidade": "m²"},
    {"servico": "Contrapiso", "formula": "area_piso", "unidade": "m²"},
    {"servico": "Piso", "formula": "area_piso * 1.1", "unidade": "m²"},
    {"servico": "Revestimento parede", "formula": "area_parede_liquida * 1.1", "unidade": "m²"},
    {"servico": "Rejunte", "formula": "area_piso + area_parede", "unidade": "m²"},
    {"servico": "Vaso sanitário", "formula": "1", "unidade": "un"},
    {"servico": "Cuba", "formula": "1", "unidade": "un"},
    {"servico": "Torneira", "formula": "1", "unidade": "un"},
    {"servico": "Chuveiro", "formula": "1", "unidade": "un"},
    {"servico": "Box vidro", "formula": "2", "unidade": "m²"},
    {"servico": "Pintura teto", "formula": "area_teto", "unidade": "m²"}
  ]
}
```

## Fatores de Perda

| Material | Fator |
|----------|-------|
| Piso cerâmico | 1.10 (10% perda) |
| Piso porcelanato | 1.08 (8% perda) |
| Madeira | 1.15 (15% perda) |
| Tinta | 1.05 (5% perda) |
| Argamassa | 1.20 (20% perda) |

## Uso no Pipeline

```
quantificar \u2192 detalhar \u2192 custear
```

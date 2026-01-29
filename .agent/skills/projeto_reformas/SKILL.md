---
name: Projeto de Reformas
description: Sugerir opções de reforma para tipos de imóveis baseado em tendências e normas
version: 1.0
dependencies: [imoveis_brasil]
---

# Skill: Projeto de Reformas

## Objetivo
Fornecer opções de reforma personalizadas com base no tipo de imóvel, padrão de acabamento e tendências de mercado.

## Entradas
- Tipo de imóvel (apto, casa, escritório, etc.)
- Padrão de acabamento (popular, médio, luxo)
- Classe social / orçamento estimado
- Preferências do cliente (opcional)

## Saídas
- Lista de opções de reforma
- Paleta de cores sugerida
- Materiais recomendados por padrão
- Estimativa de complexidade

## Scripts Disponíveis

### `scripts/area_classe.py`
Calcula área por ambiente baseado em classe social.

```bash
python area_classe.py --classe B --tipo apto --quartos 2
```

**Saída:**
```json
{
  "area_total": 65,
  "ambientes": {
    "sala": 18,
    "cozinha": 8,
    "quarto_1": 12,
    "quarto_2": 10,
    "banheiro": 5,
    "lavanderia": 4,
    "circulacao": 8
  }
}
```

### `scripts/sugerir_reforma.py`
Sugere reformas baseado em perfil do imóvel.

```bash
python sugerir_reforma.py --tipo apto --acabamento medio --ambiente banheiro
```

## Exemplos Disponíveis

### `examples/revestimentos.csv`
```csv
tipo,nome,marca,preco_m2,padrao,indicacao
Porcelanato,Biancogres 60x60,Biancogres,85.00,Médio,Piso sala/quarto
Porcelanato,Portobello 90x90,Portobello,180.00,Luxo,Piso sala/quarto
Cerâmica,Eliane 45x45,Eliane,45.00,Popular,Piso geral
```

### `examples/tendencias.md`
```markdown
## Tendências 2025

### Pinterest
- Tons terrosos e neutros
- Madeira clara (carvalho)
- Verde musgo em banheiros
- Iluminação embutida

### Locação Airbnb
- Espaços integrados
- Cozinha prática
- Decoração clean
- Automação básica

### Retrofit Casa
- Preservar elementos originais
- Modernizar instalações
- Eficiência energética
- Jardins internos
```

## Recursos Disponíveis

### `resources/acessibilidade.md`
Normas NBR 9050 resumidas para reformas residenciais.

### `resources/design_interiores.md`
- Paletas de cores por ambiente
- Combinações harmônicas
- Tendências de materiais
- Conforto térmico e acústico

### `resources/acabamentos.csv`
```csv
padrao,piso,parede,bancada,metais,marcenaria,preco_m2
Popular,Cerâmica,Tinta acrílica,Granito cinza,Docol,MDP,1200
Médio,Porcelanato,Tinta premium,Quartzo,Deca,MDF,2200
Luxo,Madeira/Porcelanato GF,Textura/Papel,Mármore,Dornbracht,MDF Laqueado,3800
```

### `resources/iluminacao.md`
Guia de iluminação por ambiente (lux recomendado, tipos de luminárias).

## Regras de Projeto

### Áreas por Classe Social (IBGE)
| Classe | Tipo | Área Média | Quartos | Banheiros |
|--------|------|------------|---------|-----------|
| E | Casa | 40 | 1-2 | 1 |
| D | Casa | 60 | 2 | 1 |
| C | Apto | 55 | 2 | 1 |
| B | Apto | 80 | 3 | 2 |
| A | Casa | 180 | 4+ | 3+ |

### Proporção de Investimento por Ambiente
| Ambiente | Popular | Médio | Luxo |
|----------|---------|-------|------|
| Banheiro | 25% | 30% | 35% |
| Cozinha | 30% | 25% | 25% |
| Sala | 15% | 15% | 15% |
| Quartos | 20% | 20% | 15% |
| Outros | 10% | 10% | 10% |

## Uso no Pipeline

```
empreiteiro → projeto_reformas → quantificar_reforma
```

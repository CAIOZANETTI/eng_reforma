---
name: Levantamento e Cálculo de Quantidades
description: Metodologia de quantificação de serviços e materiais para orçamentação, incluindo critérios de medição por NBR 12721, índices de perda, conversões de unidades e memória de cálculo rastreável.
---

# Levantamento e Cálculo de Quantidades

> *"Lixo que entra, lixo que sai. Quantitativos errados geram orçamentos errados."*  
> — Engenheiro Sênior de Custos

---

## 1. Fundamentos do Levantamento

### 1.1 Hierarquia de Precisão

| Fonte de Dados | Precisão Típica | Quando Usar |
|----------------|-----------------|-------------|
| Projeto Executivo (CAD/BIM) | ±5% | Orçamento definitivo |
| Projeto Básico / Anteprojeto | ±15% | Estimativa preliminar |
| Visita técnica + croquis | ±20% | Orçamento emergencial |
| Fotos e descrição verbal | ±30%+ | Apenas ordem de grandeza |

### 1.2 Regra de Ouro

**Sempre documente a fonte e o método de cálculo.**

Sem memória de cálculo, o quantitativo é inauditável e não resiste a questionamentos.

---

## 2. Critérios de Medição (NBR 12721)

### 2.1 Áreas

| Tipo de Área | Definição | Uso |
|--------------|-----------|-----|
| **Área Útil Interna** | Medida entre faces internas das paredes | Piso, forro, pintura |
| **Área Construída** | Inclui projeção das paredes | CUB, IPTU |
| **Área Equivalente** | Área ponderada por padrão de acabamento | Viabilidade |

### 2.2 Vãos e Descontos

| Elemento | Critério de Desconto |
|----------|---------------------|
| Portas (< 2 m²) | **NÃO** descontar da área de parede |
| Janelas (< 2 m²) | **NÃO** descontar |
| Vãos grandes (≥ 2 m²) | **DESCONTAR** da área |
| Shafts e furos | Descontar se > 0,5 m² |

**Justificativa:** O trabalho de recorte em vãos pequenos é equivalente ou superior ao de executar a área contínua.

---

## 3. Quantificação de Demolição

### 3.1 Demolição de Pisos

| Item | Unidade | Cálculo |
|------|---------|---------|
| Área de piso | m² | Comprimento × Largura |
| Contrapiso (se remover) | m³ | Área × Espessura |
| Entulho gerado | m³ | Área × 0,08 a 0,12 (cerâmica s/ contrapiso) |
| Caçambas | un | Volume entulho ÷ 3 m³ (capacidade estacionária) ou ÷ 5 m³ (caçamba grande) |

**Índice de Entulho por Tipo:**
| Material Demolido | Fator de Geração (m³/m²) |
|-------------------|-------------------------|
| Piso cerâmico (s/ contrapiso) | 0,05 a 0,08 |
| Piso cerâmico (c/ contrapiso 5cm) | 0,10 a 0,12 |
| Alvenaria 14cm | 0,15 a 0,18 por m² de parede |
| Forro de gesso | 0,03 a 0,05 |

### 3.2 Demolição de Paredes

$$Volume_{Entulho} = Área_{Parede} \times Espessura \times Fator_{Empolamento}$$

**Fator de Empolamento:** 1,3 a 1,6 (entulho ocupa mais espaço que a parede original).

**Exemplo:** Parede 3m × 2,80m × 0,14m
- Volume sólido: 3 × 2,80 × 0,14 = 1,18 m³
- Volume entulho: 1,18 × 1,4 = **1,65 m³** → ~1 caçamba pequena

---

## 4. Quantificação de Alvenaria

### 4.1 Área de Parede

$$Área_{Parede} = Perímetro \times Pé Direito - Vãos_{>2m²}$$

### 4.2 Blocos

| Tipo de Bloco | Dimensão | Quantidade/m² |
|---------------|----------|---------------|
| Cerâmico 14×19×29 | Padrão | 13 un/m² |
| Cerâmico 9×19×29 | Vedação leve | 13 un/m² |
| Concreto 14×19×39 | Estrutural | 12,5 un/m² |
| Concreto 19×19×39 | Estrutural | 12,5 un/m² |

**Perda:** Acrescentar 5% a 10% (cortes, quebras).

### 4.3 Argamassa de Assentamento

| Espessura da Junta | Consumo Argamassa | Traço Típico |
|-------------------|-------------------|--------------|
| 10 mm | 10 a 12 kg/m² | Industrializada |
| 15 mm | 15 a 18 kg/m² | Virada em obra |

### 4.4 Exemplo Completo

**Parede de 4,00m × 2,80m com porta de 0,80m × 2,10m:**

1. Área bruta: 4,00 × 2,80 = 11,20 m²
2. Vão porta: 0,80 × 2,10 = 1,68 m² (< 2m², **não desconta**)
3. Área de execução: **11,20 m²**
4. Blocos: 11,20 × 13 × 1,10 (perda) = **160 blocos**
5. Argamassa: 11,20 × 15 kg = **168 kg** (7 sacos de 25kg)

---

## 5. Quantificação de Revestimentos

### 5.1 Pisos

| Item | Cálculo |
|------|---------|
| Área líquida | Medição do ambiente |
| Perda (assentamento reto) | +10% |
| Perda (assentamento diagonal 45°) | +15% a 20% |
| Perda (paginação complexa) | +20% a 25% |

### 5.2 Revestimento de Parede

| Item | Cálculo |
|------|---------|
| Área = Perímetro × Altura | Interna do ambiente |
| Vãos | Descontar apenas > 2 m² |
| Perda | +10% (cortes laterais e de altura) |

### 5.3 Rejunte

| Formato da Peça | Junta | Consumo Rejunte |
|-----------------|-------|-----------------|
| 60×60 cm | 2 mm | 0,3 a 0,4 kg/m² |
| 60×60 cm | 3 mm | 0,5 a 0,6 kg/m² |
| 30×60 cm | 2 mm | 0,4 a 0,5 kg/m² |
| 45×45 cm | 3 mm | 0,6 a 0,8 kg/m² |

### 5.4 Argamassa Colante

| Tipo | Consumo (piso) | Consumo (parede) |
|------|----------------|------------------|
| AC-I (interno) | 4 a 5 kg/m² | 4 a 5 kg/m² |
| AC-II (externo) | 4 a 5 kg/m² | 5 a 6 kg/m² |
| AC-III (grande formato) | 5 a 7 kg/m² | 6 a 8 kg/m² |

**Dupla colagem (peças > 60×60):** Multiplicar consumo por 1,5 a 1,8.

---

## 6. Quantificação de Pintura

### 6.1 Área de Pintura

$$Área_{Pintura} = Área_{Paredes} + Área_{Teto} - Vãos_{>2m²}$$

**Atenção:** Alguns orçamentistas NÃO descontam vãos pequenos porque o trabalho de recorte (fita, cuidado) compensa a área "perdida".

### 6.2 Rendimento de Tintas

| Tipo | Rendimento (m²/L/demão) | Demãos Típicas |
|------|-------------------------|----------------|
| Látex PVA | 10 a 12 m²/L | 2 a 3 |
| Acrílica Fosca | 10 a 12 m²/L | 2 |
| Acrílica Semi-brilho | 8 a 10 m²/L | 2 |
| Esmalte Sintético | 8 a 10 m²/L | 2 a 3 |
| Massa Corrida (preparação) | 2 a 3 m²/kg | 1 a 2 |

### 6.3 Exemplo

**Quarto 3×4m, pé-direito 2,80m:**

1. Perímetro: (3 + 4) × 2 = 14 m
2. Área paredes: 14 × 2,80 = 39,2 m²
3. Vãos: Porta 0,80×2,10 = 1,68 m² + Janela 1,20×1,20 = 1,44 m² → Total 3,12 m² (< 2m² cada, não desconta)
4. Área paredes final: **39,2 m²**
5. Área teto: 3 × 4 = **12 m²**
6. **Área total pintura: 51,2 m²**
7. Tinta acrílica (2 demãos, 10 m²/L): 51,2 ÷ 10 × 2 = **10,24 L** → 3 galões de 3,6L

---

## 7. Quantificação de Instalações

### 7.1 Pontos Elétricos

| Tipo de Ponto | O que Inclui |
|---------------|-------------|
| Ponto simples (tomada baixa) | Eletroduto, caixa 4x2, cabo 2,5mm², tomada |
| Ponto alto (interuptor/iluminação) | Eletroduto, caixa 4x2, cabo 1,5mm², interuptor |
| Ponto de força (chuveiro, ar cond.) | Eletroduto, caixa 4x4, cabo 4-6mm², disjuntor |

**Metragem Típica de Cabo por Ponto:**
- Ponto novo (subindo do quadro): 12 a 20 m de cabo
- Ponto derivado de existente: 5 a 8 m de cabo

### 7.2 Pontos Hidráulicos

| Tipo | Componentes Típicos |
|------|---------------------|
| Ponto de água fria | Tubo PVC 25mm, conexões, registro |
| Ponto de água quente | Tubo PPR ou PEX, conexões, registro |
| Ponto de esgoto | Tubo PVC 40-100mm, conexões, caixa sifonada |

**Metragem Típica por Ponto (banheiro convencional):**
- Água fria: 3 a 5 m de tubo por ponto
- Esgoto: 2 a 4 m de tubo por aparelho

---

## 8. Tabela de Conversões Úteis

| De | Para | Fator |
|----|------|-------|
| m³ de concreto | kg de cimento (traço 1:2:3) | ×350 kg |
| m³ de concreto | L de água | ×180 L |
| m³ de areia | kg | ×1.500 kg |
| m³ de brita | kg | ×1.400 kg |
| m² de contrapiso 5cm | m³ | ×0,05 |
| m² de reboco 2cm | kg de argamassa | ×35 kg |
| Lata de 18L | Galões de 3,6L | ×5 |
| Saco de cimento 50kg | L de volume | ~36 L |

---

## 9. Memória de Cálculo Padrão

**Formato Recomendado:**

```
================================================================================
MEMÓRIA DE CÁLCULO - PROJETO: [Nome]
DATA: [DD/MM/AAAA]
RESPONSÁVEL: [Nome]
================================================================================

ITEM 3.1 - PISO PORCELANATO 60×60 SALA/COZINHA
─────────────────────────────────────────────────────────────────────────────

1. LEVANTAMENTO:
   • Sala de Estar: 4,50m × 5,20m = 23,40 m²
   • Cozinha: 3,20m × 4,00m = 12,80 m²
   • Circulação: 1,20m × 3,00m = 3,60 m²
   ───────────────────────────────────────
   SUBTOTAL LÍQUIDO: 39,80 m²

2. PERDAS E AJUSTES:
   • Perda por corte (assentamento reto): +10% = 3,98 m²
   ───────────────────────────────────────
   SUBTOTAL COM PERDA: 43,78 m²

3. QUANTIDADE FINAL:
   • Arredondamento p/ caixa (1,44 m²/cx): 43,78 ÷ 1,44 = 30,4 cx → 31 caixas
   • Área total: 31 × 1,44 = 44,64 m²
   ───────────────────────────────────────
   QUANTIDADE ORÇADA: 45,00 m² (reserva técnica)

4. FONTE:
   • Medidas: Projeto [Arq_Layout_Rev02.dwg], camada "PISO"
   • Perda: TCPO 14ª ed., tabela 02.11

================================================================================
```

---

## 10. Erros Comuns e Como Evitar

| Erro | Consequência | Prevenção |
|------|-------------|-----------|
| Medir área construída em vez de útil | Superestimação de piso/forro | Definir claramente o critério |
| Esquecer a perda | Falta de material na obra | Sempre aplicar índice de perda |
| Não considerar espessura do rejunte | Subestima argamassa/rejunte | Especificar junta no orçamento |
| Contar vãos pequenos como desconto | Subestima mão de obra | Seguir regra dos 2 m² |
| Copiar quantidade de outro projeto | Erro por diferença de layout | Levantar cada projeto individualmente |
| Arredondar para baixo | Falta material | Sempre arredondar para cima |

---

## 11. Checklist de Validação

- [ ] Todas as áreas estão em m² ou unidade correta?
- [ ] As perdas foram aplicadas conforme o tipo de serviço?
- [ ] Vãos foram tratados conforme regra (< 2m² não desconta)?
- [ ] A memória de cálculo está documentada e rastreável?
- [ ] As quantidades estão arredondadas para embalagem comercial?
- [ ] O projeto de referência está identificado (nome, revisão)?
- [ ] Houve conferência cruzada (área calculada ≈ área do croqui)?

---

*Metodologia conforme NBR 12721, TCPO (PINI) e práticas de mercado.*

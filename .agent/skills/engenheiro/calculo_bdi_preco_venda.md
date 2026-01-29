---
name: Precificação - BDI e Formação de Preço de Venda
description: Metodologia completa para cálculo do BDI (Benefícios e Despesas Indiretas) e formação do Preço de Venda, incluindo fórmulas do TCU, análise de regimes tributários e estratégias de precificação por tipo de serviço.
---

# Precificação: BDI e Formação de Preço de Venda

> *"Preço não é chute. É a engenharia do equilíbrio entre competitividade e sobrevivência."*  
> — Engenheiro de Custos Sênior

---

## 1. Anatomia do Preço de Venda

### 1.1 Composição Estrutural

O Preço de Venda (PV) de um serviço de construção é composto por:

```
┌─────────────────────────────────────────────────────────────┐
│                    PREÇO DE VENDA (PV)                      │
├─────────────────────────────────────────────────────────────┤
│  CUSTO DIRETO (CD)                                          │
│  ├── Materiais                                              │
│  ├── Mão de Obra de Produção                                │
│  └── Equipamentos de Produção                               │
├─────────────────────────────────────────────────────────────┤
│  BENEFÍCIOS E DESPESAS INDIRETAS (BDI)                      │
│  ├── Custos Indiretos                                       │
│  │   ├── Administração Central (AC)                         │
│  │   ├── Despesas Financeiras (DF)                          │
│  │   ├── Seguros e Garantias (S+G)                          │
│  │   └── Riscos e Imprevistos (R)                           │
│  ├── Impostos sobre Faturamento (I)                         │
│  └── Lucro Bruto (L)                                        │
└─────────────────────────────────────────────────────────────┘
```

**Relação Fundamental:**
$$PV = CD \times (1 + BDI)$$

---

## 2. A Fórmula do BDI

### 2.1 Fórmula Padrão (TCU / Acórdão 2622/2013)

O Tribunal de Contas da União consagrou a seguinte fórmula:

$$BDI = \frac{(1 + AC + S + R + G) \times (1 + DF) \times (1 + L)}{(1 - I)} - 1$$

**Onde:**
- **AC** = Administração Central (rateio do escritório)
- **S** = Seguros (CAR, RCG, etc.)
- **R** = Riscos e Imprevistos
- **G** = Garantias (cauções, seguro garantia)
- **DF** = Despesas Financeiras (custo do capital de giro)
- **L** = Lucro Bruto Desejado
- **I** = Impostos sobre o faturamento

### 2.2 Faixas de Referência (TCU)

| Componente | Mínimo | Médio | Máximo | Observação |
|------------|--------|-------|--------|------------|
| **AC** | 3,00% | 4,00% | 5,50% | Varia com porte da empresa |
| **S** | 0,50% | 0,80% | 1,00% | Seguro Risco Engenharia |
| **R** | 0,50% | 0,97% | 1,50% | Risco técnico do projeto |
| **G** | 0,00% | 0,50% | 1,00% | Se houver retenção/caução |
| **DF** | 0,50% | 0,59% | 1,50% | Função da taxa Selic |
| **L** | 5,00% | 7,40% | 10,00% | Margem desejada |
| **I** | 8,65% | 11,50% | 16,65% | Depende do regime tributário |

### 2.3 Impostos por Regime Tributário

O componente **I** varia drasticamente:

| Regime | PIS | COFINS | ISS | CPRB/INSS | IRPJ/CSLL | **Total I** |
|--------|-----|--------|-----|-----------|-----------|-------------|
| **Simples Nacional** (Anexo IV - até R$ 4,8M) | Incluso | Incluso | Incluso | Incluso | Incluso | **11% a 16%** |
| **Lucro Presumido (s/ desoneração)** | 0,65% | 3,00% | 2-5% | 0% | ~4,5%* | **10% a 13%** |
| **Lucro Presumido (c/ desoneração)** | 0,65% | 3,00% | 2-5% | 4,5% | ~4,5%* | **14% a 18%** |
| **Lucro Real** | 1,65% | 7,60% | 2-5% | 0% ou 4,5% | Variável | **11% a 17%** |

*IRPJ/CSLL sobre lucro presumido de 8% a 32% da receita bruta.

---

## 3. Cálculo Passo a Passo

### 3.1 Exemplo: Reforma Residencial (Simples Nacional)

**Dados:**
- Custo Direto (CD): R$ 50.000,00
- Regime: Simples Nacional (Anexo IV) — Alíquota efetiva: 12%
- Empresa de pequeno porte (AC moderado)

**Parâmetros:**
| Componente | Valor |
|------------|-------|
| AC | 4,00% |
| S | 0,80% |
| R | 1,00% |
| G | 0,00% |
| DF | 0,60% |
| L | 8,00% |
| I | 12,00% |

**Cálculo:**

1. **Numerador:**
   - $(1 + AC + S + R + G) = (1 + 0,04 + 0,008 + 0,01 + 0) = 1,058$
   - $(1 + DF) = (1 + 0,006) = 1,006$
   - $(1 + L) = (1 + 0,08) = 1,08$
   - **Numerador = 1,058 × 1,006 × 1,08 = 1,1496**

2. **Denominador:**
   - $(1 - I) = (1 - 0,12) = 0,88$

3. **BDI:**
   - $BDI = \frac{1,1496}{0,88} - 1 = 1,3064 - 1 = 0,3064$
   - **BDI = 30,64%**

4. **Preço de Venda:**
   - $PV = 50.000 \times (1 + 0,3064) = 50.000 \times 1,3064$
   - **PV = R$ 65.320,00**

### 3.2 Verificação da Distribuição

| Componente | Cálculo | Valor (R$) |
|------------|---------|------------|
| Custo Direto | — | 50.000,00 |
| Administração Central | 65.320 × 4% | 2.612,80 |
| Seguros | 65.320 × 0,8% | 522,56 |
| Riscos | 65.320 × 1% | 653,20 |
| Despesas Financeiras | ~65.320 × 0,6% | 391,92 |
| Lucro Bruto | ~65.320 × 8% | 5.225,60 |
| Impostos | 65.320 × 12% | 7.838,40 |
| **Total** | | **67.244,48** |

*Nota: Há pequeno descasamento devido à interação multiplicativa da fórmula.*

---

## 4. Estratégias Avançadas de Precificação

### 4.1 BDI Diferenciado por Natureza de Serviço

Não é obrigatório usar o mesmo BDI para todos os itens:

| Tipo de Serviço | BDI Sugerido | Justificativa |
|-----------------|--------------|---------------|
| **Serviços civis (pedreiro, pintura)** | 30-35% | Alto risco operacional, gestão intensiva |
| **Instalações especializadas (elétrica, hidro)** | 25-30% | Subempreitada, menor gestão direta |
| **Fornecimento de materiais premium** | 15-20% | Apenas repasse, baixo risco |
| **Equipamentos (ar condicionado, elevador)** | 10-15% | Fornecimento + Instalação fabricante |

**Vantagem:** Aumenta competitividade em itens de alto valor (materiais), mantendo margem nos serviços.

### 4.2 Precificação por Concorrência

Quando há licitação ou cotação competitiva:

1. **Calcule seu BDI "ideal"** (fórmula acima).
2. **Estime o preço do concorrente** (histórico, benchmark).
3. **Ajuste o Lucro (L)** para ficar competitivo:
   - $L_{ajustado} = \frac{PV_{desejado}}{CD} \times (1 - I) \div [(1+AC+S+R+G)(1+DF)] - 1$

**Limite:** Nunca opere com L < 0. Se necessário, decline a proposta.

### 4.3 Markup vs. BDI: Entenda a Diferença

| | **Markup** | **BDI** |
|---|-----------|---------|
| **Fórmula** | PV = CD × (1 + M) | PV = CD × (1 + BDI) |
| **Diferença** | Não considera impostos sobre faturamento corretamente | Considera impostos como divisor |
| **Erro típico** | "Vou colocar 30% de margem" → na verdade sobra ~15% após impostos | BDI de 30% entrega margem real conforme planejado |

**Exemplo do Erro:**
- CD = R$ 100
- Markup "de 30%": PV = R$ 130
- Impostos (12%): R$ 15,60
- Sobra: R$ 130 - 100 - 15,60 = R$ 14,40 (apenas 14,4% sobre CD)

---

## 5. Casos Especiais

### 5.1 Obras por Administração (Custo + Taxa)

Em contratos "Cost Plus":
- O cliente paga o Custo Direto comprovado + uma Taxa Fixa de Administração.
- A Taxa substitui o BDI e geralmente fica entre **12% a 18%**.
- **Não há risco de estouro** para o contratado, mas limita o lucro.

### 5.2 Mão de Obra Avulsa (Diária/Hora)

Para venda de mão de obra sem material:
- CD = Custo horário do profissional (salário + encargos + benefícios)
- BDI pode ser menor (20-25%) pois não há risco de material

**Exemplo:** Pedreiro custa R$ 35/h com encargos. PV = 35 × 1,25 = **R$ 43,75/h**.

### 5.3 Revisão de Preços (Reajuste Contratual)

Para contratos longos (> 12 meses), inclua cláusula de reajuste:
- **INCC** (Índice Nacional de Custo da Construção) para custo geral
- **IPCA** para itens gerais
- **Variação específica** para aço, combustível (se relevante)

---

## 6. Tabela de Referência Rápida

### BDI Típicos por Tipo de Obra (2026)

| Tipo de Obra | BDI Mínimo | BDI Médio | BDI Máximo |
|--------------|------------|-----------|------------|
| Reforma residencial (pequena) | 25% | 30% | 35% |
| Reforma comercial | 22% | 28% | 32% |
| Obra nova residencial | 20% | 25% | 30% |
| Obra pública (licitação) | 20% | 24% | 28% |
| Manutenção predial | 18% | 22% | 26% |

---

## 7. Checklist de Validação do BDI

- [ ] O regime tributário está correto (Simples, Presumido, Real)?
- [ ] Os impostos municipais (ISS) estão com alíquota do município correto?
- [ ] A administração central está proporcional ao porte da empresa?
- [ ] O lucro desejado é compatível com o mercado local?
- [ ] O BDI final está dentro da faixa de mercado para o tipo de obra?
- [ ] Se for licitação pública, o BDI está dentro dos limites do TCU?
- [ ] Há cláusula de reajuste para contratos > 12 meses?

---

## 8. Erros Fatais

| Erro | Consequência | Prevenção |
|------|-------------|-----------|
| Confundir Markup com BDI | Margem real menor que planejada | Usar fórmula com divisor (1-I) |
| Esquecer a CPRB (se desonerado) | Falta imposto no PV | Verificar regime da empresa |
| Usar ISS de 2% quando é 5% | Prejuízo de 3% do faturamento | Conferir legislação municipal |
| Não incluir Administração Central | Escritório fica "de graça" | Ratear custos fixos sobre todas as obras |
| Considerar Lucro "por fora" | Dupla contagem ou confusão | Lucro é componente do BDI |

---

*Metodologia conforme Acórdãos TCU 2369/2011, 2622/2013 e 2.369/2011-Plenário.*

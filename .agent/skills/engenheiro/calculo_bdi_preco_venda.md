---
name: Precificação - BDI e Valor de Venda
description: Metodologia avançada para cálculo de BDI (Benefícios e Despesas Indiretas) e formação de Preço de Venda, garantindo cobertura de custos indiretos, impostos e margem de lucro.
---

# Precificação: Cálculo de BDI e Preço de Venda

Preço não é chute. O Engenheiro Sênior calcula o preço de venda para garantir a saúde financeira do negócio, cobrindo todos os custos "invisíveis" e garantindo o lucro líquido.

## 1. O que compõe o Preço de Venda (PV)?

$$ PV = CD + CI + I + L $$

*   **CD (Custo Direto):** Material + Mão de Obra (o que fica na obra).
*   **CI (Custo Indireto / Adm):** Escritório, engenheiro, combustível, software, contador.
*   **I (Impostos):** PIS, COFINS, ISS, CPRB, IRPJ/CSLL (conforme regime).
*   **L (Lucro):** A remuneração do risco e do capital investido.

O **BDI** (Benefícios e Despesas Indiretas) é o fator multiplicador que transforma o Custo Direto no Preço de Venda.

## 2. A Fórmula do BDI (Padrão Mercado/TCU)

$$ BDI = \frac{(1 + AC + S + R + G)(1 + DF)(1 + L)}{(1 - I)} - 1 $$

Onde (valores de referência típicos para reformas):

*   **AC (Administração Central):** 3,0% a 5,5%. (Custo fixo do escritório rateado).
*   **S (Seguros):** 0,8% a 1,0%. (Seguro Risco Engenharia).
*   **R (Riscos):** 1,0% a 2,0%. (Imprevistos de obra, retrabalhos).
*   **G (Garantias):** 0,5% a 1,0%. (Custo financeiro de retenções ou cauções).
*   **DF (Despesas Financeiras):** 0,5% a 1,5%. (Custo do dinheiro no tempo/capital de giro).
*   **L (Lucro Operacional):** 7% a 15% (Depende da estratégia comercial).
*   **I (Impostos sobre Venda):**
    *   Simples Nacional (Anexo IV): ~10% a 16%.
    *   Lucro Presumido: ~14,25% a 16,25% (PIS+COFINS 3,65% + ISS 2-5% + CPRB 4,5% opcional + IRPJ/CSLL).

*Nota: No regime de Lucro Presumido, IRPJ e CSLL podem ser tratados dentro do Lucro ou como impostos, dependendo da contabilidade.*

## 3. Exemplo Prático de Aplicação

Para uma obra com **Custo Direto de R$ 100.000,00**:

1.  Definimos as Taxas:
    *   AC+S+R+G = 6% (0,06)
    *   DF = 1% (0,01)
    *   L = 10% (0,10)
    *   I = 14% (0,14) - Simples/ISS médio

2.  Cálculo do Numerador: `(1.06) * (1.01) * (1.10) = 1.17766`
3.  Cálculo do Denominador: `(1 - 0.14) = 0.86`
4.  Divisão: `1.17766 / 0.86 = 1.3693`
5.  **BDI Final:** 36,93%

**Preço de Venda = R$ 100.000 * 1,3693 = R$ 136.930,00**

## 4. Estratégias de Precificação (Engenharia Sênior)

*   **BDI Diferenciado:**
    *   É comum aplicar BDIs diferentes para Material e Mão de Obra.
    *   *Materiais de alto valor (ex: Elevador, Ar Condicionado VRF):* BDI Reduzido (15-20%) para não perder competitividade, já que o risco e o trabalho administrativo são menores que a execução civil em si (apenas repasse/gestão).
*   **Margem de Contribuição:**
    *   Em tempos de "vacas magras", pode-se reduzir o Lucro (L) objetivando apenas pagar os Custos Indiretos (AC), mantendo a equipe girando.

## 5. Erros Críticos

*   **Confumdir Margem com Markup:**
    *   Colocar 20% "em cima" do custo (`Custo * 1.20`) NÃO É ter 20% de lucro.
    *   Se você tem 14% de imposto, ao aplicar 20% de markup, sobra apenas 6% para pagar custo fixo e lucro. Provavelmente terá prejuízo.
    *   *Sempre use a fórmula do BDI (divisor 1-Imposto) para garantir a margem líquida real.*

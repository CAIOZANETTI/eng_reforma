---
name: Orçamentação Analítica e Composições SINAPI
description: Manual avançado de Engenharia de Custos para elaboração de orçamentos detalhados, análise de composições unitárias, uso de tabelas referenciais (SINAPI/TCPO) e auditoria de quantitativos.
---

# Orçamentação Analítica e Composições de Preço Unitário

> *"Um orçamento não é uma lista de preços. É a tradução financeira de um projeto técnico."*  
> — Engenheiro de Custos Sênior

---

## 1. Fundamentos da Orçamentação

### 1.1 Hierarquia do Orçamento

O orçamento de uma obra segue uma estrutura hierárquica rigorosa:

```
ORÇAMENTO GLOBAL
├── CUSTO DIRETO (CD)
│   ├── Materiais
│   ├── Mão de Obra
│   └── Equipamentos
├── CUSTO INDIRETO (CI)
│   ├── Administração Local (Canteiro)
│   └── Administração Central (Sede)
├── IMPOSTOS (I)
└── LUCRO (L)
```

**Fórmula Fundamental:**
$$PV = CD \times (1 + BDI)$$

Onde **BDI** (Benefícios e Despesas Indiretas) encapsula CI, I e L.

### 1.2 Níveis de Precisão

| Fase do Projeto | Tipo de Estimativa | Precisão Esperada | Base de Dados |
|-----------------|-------------------|-------------------|---------------|
| Estudo de Viabilidade | Paramétrica (CUB/m²) | ±30% | Históricos |
| Anteprojeto | Semi-analítica | ±15% | SINAPI + Cotações |
| Projeto Executivo | Analítica Detalhada | ±5% | SINAPI + 3 Cotações |
| Obra em Andamento | Reorçamento | ±2% | As-Built + Compras Reais |

---

## 2. Composição de Preço Unitário (CPU)

A CPU é o DNA do orçamento. Cada serviço deve ser decomposto em seus insumos fundamentais.

### 2.1 Estrutura Padrão de uma CPU

```
COMPOSIÇÃO: Alvenaria de Vedação com Bloco Cerâmico 14x19x29cm
Unidade: m²
Produção de referência: 1,00 m²

┌────────────────────────────────────────────────────────────────────┐
│ INSUMO                      │ UNID │ COEF.  │ PREÇO │   TOTAL    │
├─────────────────────────────┼──────┼────────┼───────┼────────────┤
│ MATERIAIS                                                         │
│ Bloco cerâmico 14x19x29     │ un   │ 13,00  │  2,50 │     32,50  │
│ Argamassa industrializada   │ kg   │ 15,00  │  0,65 │      9,75  │
│ Tela de amarração           │ m    │  0,30  │  8,00 │      2,40  │
├─────────────────────────────┼──────┼────────┼───────┼────────────┤
│ MÃO DE OBRA                                                       │
│ Pedreiro (com encargos)     │ h    │  0,90  │ 28,50 │     25,65  │
│ Servente (com encargos)     │ h    │  0,45  │ 19,20 │      8,64  │
├─────────────────────────────┼──────┼────────┼───────┼────────────┤
│ EQUIPAMENTOS                                                      │
│ Andaime metálico (locação)  │ m².mês│ 0,02  │ 12,00 │      0,24  │
├─────────────────────────────┼──────┼────────┼───────┼────────────┤
│ CUSTO UNITÁRIO DIRETO                              │     79,18  │
└────────────────────────────────────────────────────┴────────────┘
```

### 2.2 Os Coeficientes de Consumo

O **coeficiente** é a quantidade de insumo necessária para produzir 1 unidade do serviço.

**Fontes Oficiais de Coeficientes:**
1. **SINAPI** (Caixa Econômica) — Referência para obras públicas
2. **TCPO** (PINI) — Mais detalhado, padrão de mercado privado
3. **Histórico Próprio** — Empresas maduras desenvolvem bases próprias

**Atenção às Perdas:**
Os coeficientes SINAPI já incluem perdas típicas. Não duplique!

| Material | Perda Típica Já Inclusa |
|----------|------------------------|
| Blocos/Tijolos | 3% a 5% |
| Argamassas | 10% a 15% |
| Concreto usinado | 3% a 5% |
| Aço CA-50/60 | 10% (corte e dobra) |
| Cerâmicas/Pisos | 10% (assentamento reto) |

### 2.3 Produtividade da Mão de Obra

A produtividade é expressa como **Homem-hora por unidade de serviço (Hh/unid)**.

**Fatores que Afetam Produtividade em Reformas:**

| Fator | Impacto na Produtividade |
|-------|-------------------------|
| Acesso difícil (escadas, sem elevador) | -20% a -40% |
| Horário restrito (condomínio) | -15% a -25% |
| Trabalho sobre existente (não é "limpo") | -10% a -20% |
| Área pequena e recortada | -15% a -30% |
| Reforma habitada (morador presente) | -20% a -30% |

**Regra Prática:** Para reformas residenciais, aplique um **Fator de Ajuste de 1,3 a 1,5** sobre os coeficientes SINAPI de obra nova.

---

## 3. O Sistema SINAPI

### 3.1 Estrutura do SINAPI

O SINAPI é dividido em:

1. **Catálogo de Insumos:** Materiais, mão de obra e equipamentos com preços mensais por estado.
2. **Catálogo de Composições:** Serviços compostos por insumos com seus coeficientes.

**Códigos Importantes:**
- Insumos: `00xxxxx` (7 dígitos)
- Composições: `xxxxx` (5 dígitos) ou `9xxxx` (novas, 5 dígitos)

### 3.2 Desoneração da Folha

O SINAPI publica **duas tabelas de preços de mão de obra**:

| Tabela | Característica | Quando Usar |
|--------|---------------|-------------|
| **Com Desoneração** | INSS Patronal (20%) é substituído por CPRB (4,5%) | Construtoras que optaram pela desoneração |
| **Sem Desoneração** | Encargos completos (~80% sobre salário) | Maioria das empresas de reforma (Simples Nacional, MEI) |

**Erro Crítico:** Usar tabela desonerada para orçar obra de empresa não desonerada = **prejuízo de ~15%** na mão de obra.

### 3.3 Quando NÃO Usar o SINAPI

O SINAPI não é bala de prata. Evite-o para:

- **Materiais de acabamento especificados:** O SINAPI tem "porcelanato genérico". Se o projeto pede *Portobello Marmi Clássico 1,20x2,40m*, cote diretamente.
- **Serviços muito específicos:** Instalação de banheira de hidromassagem, automação residencial, marcenaria sob medida.
- **Equipamentos especiais:** Ar condicionado VRF, elevadores, sistemas de aquecimento solar.

---

## 4. Levantamento de Quantitativos

### 4.1 Fontes de Dados

| Elemento | Fonte Primária | Verificação |
|----------|---------------|-------------|
| Áreas de piso | Planta baixa (AutoCAD/Revit) | Medição in loco |
| Paredes (área) | Perímetro × Altura (descontar vãos > 2m²) | Conferir pé-direito |
| Instalações | Projeto específico (elétrica/hidráulica) | Quantificar pontos |

### 4.2 Critérios de Medição (NBR 12721)

- **Áreas:** Sempre em m², medidas internas (sem paredes) ou externas (com paredes), conforme definido.
- **Alvenaria:** Área bruta menos vãos maiores que 2m². Vãos pequenos (portas 0,80m) não são descontados.
- **Pintura:** Considera-se toda a superfície, incluindo recortes de janelas e portas (mão de obra de recorte é mais cara que a área "perdida").

### 4.3 Memória de Cálculo

**Toda quantidade deve ter rastreabilidade.**

Exemplo de Memória de Cálculo:
```
ITEM 3.2 - Piso Porcelanato Sala/Cozinha
─────────────────────────────────────────
Sala de estar:     4,50m × 5,20m = 23,40 m²
Cozinha:           3,20m × 4,00m = 12,80 m²
                                  ────────
Subtotal líquido:                  36,20 m²
Acréscimo de perda (10%):           3,62 m²
                                  ────────
QUANTIDADE TOTAL:                  39,82 m² → Arredondar: 40,00 m²
```

---

## 5. Cotação e Validação de Preços

### 5.1 Regra das 3 Cotações

Para itens da **Classe A** (Curva ABC), obtenha no mínimo 3 cotações:

1. **Menor Preço:** Referência de "piso".
2. **Preço Médio:** Base para o orçamento.
3. **Maior Preço:** Referência de "teto" (pode indicar qualidade superior).

### 5.2 Validade da Cotação

| Material | Validade Típica da Cotação |
|----------|---------------------------|
| Cimento, Areia, Brita | 7 dias |
| Aço | 3 a 7 dias (alta volatilidade) |
| Cerâmicas/Porcelanatos | 15 a 30 dias |
| Materiais importados | Cotação específica (dólar) |

**Cláusula de Proteção:** Sempre inclua no orçamento:  
*"Preços válidos por 15 dias. Sujeito a reajuste por variação de insumos superior a 5%."*

---

## 6. Auditoria do Orçamento

### 6.1 Checklist de Revisão (Antes de Liberar)

- [ ] **Coerência de Unidades:** m² de parede ≠ m² de piso. Revisar cada item.
- [ ] **Duplicidade:** Demolição já inclui caçamba? Ou caçamba está separada?
- [ ] **Itens Esquecidos:** Proteções (lona, fita), consumíveis (lixa, disco), mobilização.
- [ ] **Lógica de Quantidades:** 40m² de piso gera ~12m² de rodapé (perímetro)?
- [ ] **Compatibilidade com Projeto:** O orçamento reflete o que está desenhado?

### 6.2 Indicadores de Sanidade

Compare seu orçamento com benchmarks:

| Serviço | Custo Típico (Reforma SP - 2026) |
|---------|----------------------------------|
| Reforma completa banheiro | R$ 2.500 a R$ 4.500/m² |
| Reforma completa cozinha | R$ 2.000 a R$ 3.500/m² |
| Pintura completa (parede+teto) | R$ 35 a R$ 55/m² |
| Troca de piso (porcelanato 60x60) | R$ 180 a R$ 280/m² (material + M.O.) |
| Instalação elétrica nova (ponto) | R$ 180 a R$ 350/ponto |

Se seu orçamento estiver **mais de 20% fora** desses benchmarks, revise.

---

## 7. Ferramentas e Documentação

### 7.1 Planilha Orçamentária Padrão

A planilha deve conter, no mínimo:

| Coluna | Descrição |
|--------|-----------|
| Item | Código hierárquico (1.1, 1.2, 2.1...) |
| Descrição | Descrição completa do serviço |
| Unidade | m², m, un, kg, vb (verba) |
| Quantidade | Levantamento com memória de cálculo anexa |
| Preço Unitário | Fonte: SINAPI, cotação, histórico |
| Preço Total | Quantidade × Preço Unitário |
| Fonte | Código SINAPI ou "Cotação Fornecedor X" |

### 7.2 Documentos Anexos ao Orçamento

1. **Memória de Cálculo:** Rastreabilidade de quantidades.
2. **Cotações:** Cópias das propostas de fornecedores.
3. **Premissas:** Prazo, regime tributário, condições de acesso.
4. **Cronograma Físico-Financeiro:** Distribuição mensal do custo.

---

## 8. Erros Fatais em Orçamentação

| Erro | Consequência | Prevenção |
|------|-------------|-----------|
| Usar preço desatualizado | Prejuízo na compra | Sempre usar tabela do mês vigente |
| Esquecer o custo do lixo | Estouro de 3-5% | Incluir caçamba ou verba de descarte |
| Subestimar produtividade de reforma | Estouro de mão de obra | Fator de ajuste 1,3 a 1,5 |
| Não considerar logística vertical | Custo oculto de servente | Acrescentar transporte interno |
| Orçar "por cima" demais | Perder a concorrência | Refinar quantitativos, não "chutar" |

---

*Elaborado conforme práticas do IBEC (Instituto Brasileiro de Engenharia de Custos) e metodologia SINAPI/Caixa.*

---
name: Estrutura Analítica do Projeto (EAP) para Reformas
description: Metodologia de decomposição hierárquica de projetos de reforma residencial, incluindo organização por macro-fases, sequenciamento lógico, dependências e critérios de encerramento de etapas.
---

# Estrutura Analítica do Projeto (EAP) para Reformas

> *"Dividir para conquistar. Uma reforma bem planejada é uma soma de etapas simples."*  
> — Engenheiro Gestor de Obra

---

## 1. Conceito da EAP

### 1.1 Definição

A **EAP (Estrutura Analítica do Projeto)** — em inglês, *WBS (Work Breakdown Structure)* — é a decomposição hierárquica do projeto em entregas menores e gerenciáveis.

### 1.2 Níveis da Hierarquia

```
NÍVEL 0: Projeto (Reforma Completa)
├── NÍVEL 1: Macro-Fase (Demolição, Instalações, Acabamentos...)
│   ├── NÍVEL 2: Pacote de Trabalho (Demolição de Piso, Demolição de Parede...)
│   │   └── NÍVEL 3: Atividade (Quebrar piso sala, Remover entulho sala...)
```

**Regra dos 100%:** A soma de todos os pacotes filhos deve representar 100% do pacote pai.

### 1.3 Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Clareza de escopo** | Tudo que está na EAP será feito; o que não está, não será |
| **Base para cronograma** | Cada pacote vira uma linha no cronograma |
| **Base para orçamento** | Cada pacote tem custo associado |
| **Controle de progresso** | % concluído por pacote |
| **Gestão de mudanças** | Adição = novo pacote = aditivo |

---

## 2. Macro-Fases de uma Reforma Residencial

### 2.1 Sequência Padrão

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. PRELIMINARES                                                             │
│    Mobilização, proteções, canteiro                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. DEMOLIÇÃO E REMOÇÃO                                                      │
│    Demolição de revestimentos, paredes, forros, remoção de entulho          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. ESTRUTURA E VEDAÇÃO                                                      │
│    Reforços estruturais, novas alvenarias, dry wall                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 4. INSTALAÇÕES HIDRÁULICAS                                                  │
│    Água fria, água quente, esgoto, gás                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 5. INSTALAÇÕES ELÉTRICAS                                                    │
│    Infraestrutura, cabeamento, quadro, automação                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 6. IMPERMEABILIZAÇÃO                                                        │
│    Áreas molhadas, varandas, floreiras                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 7. CONTRAPISO E REGULARIZAÇÃO                                               │
│    Contrapiso, nivelamento, caimento para ralos                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 8. REVESTIMENTOS                                                            │
│    Pisos, paredes, rodapés, soleiras                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 9. FORRO E GESSO                                                            │
│    Forro de gesso, sancas, tabicas, cortineiros                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 10. ESQUADRIAS                                                              │
│    Portas, janelas, vidros, ferragens                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 11. PINTURA                                                                 │
│    Preparação, massa, fundo, acabamento                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 12. LOUÇAS E METAIS                                                         │
│    Vasos, cubas, torneiras, acessórios                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 13. MARCENARIA E MOBILIÁRIO                                                 │
│    Armários, bancadas, painéis                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 14. LIMPEZA E DESMOBILIZAÇÃO                                                │
│    Limpeza fina, retirada de proteções, entrega                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Dependências Críticas (Predecessoras)

| Macro-Fase | Predecessora Obrigatória | Justificativa |
|------------|-------------------------|---------------|
| 4. Hidráulica | 2. Demolição concluída | Acessar tubulações existentes |
| 5. Elétrica | 3. Vedação iniciada | Passar eletrodutos nas paredes |
| 6. Impermeabilização | 4. Hidráulica concluída (esse ambiente) | Testar pontos antes de impermeabilizar |
| 7. Contrapiso | 4 e 5 concluídas (esse ambiente) | Instalações embutidas prontas |
| 8. Revestimentos | 6 e 7 concluídas | Substrato pronto |
| 9. Forro | 5. Elétrica no teto concluída | Fechar infraestrutura |
| 11. Pintura | 9 e 10 concluídas | Paredes, forros e portas instalados |
| 12. Louças | 8. Revestimentos concluídos | Furação em revestimento finalizado |
| 13. Marcenaria | 11. Pintura concluída | Evitar danos à marcenaria |

---

## 3. EAP Detalhada — Modelo para Reforma de Banheiro

### 3.1 Decomposição Completa

```
1.0 REFORMA BANHEIRO
│
├── 1.1 PRELIMINARES
│   ├── 1.1.1 Proteção de áreas adjacentes (plástico, papelão)
│   ├── 1.1.2 Instalação de caixa d'água provisória (se necessário)
│   └── 1.1.3 Desligar água e eletricidade do ambiente
│
├── 1.2 DEMOLIÇÃO
│   ├── 1.2.1 Remoção de louças e metais existentes
│   ├── 1.2.2 Demolição de revestimento de parede
│   ├── 1.2.3 Demolição de piso cerâmico
│   ├── 1.2.4 Demolição de contrapiso (se necessário)
│   ├── 1.2.5 Demolição de forro de gesso (se existente)
│   ├── 1.2.6 Remoção e transporte de entulho
│   └── 1.2.7 Caçamba de entulho (1 a 2 unidades)
│
├── 1.3 INSTALAÇÕES HIDRÁULICAS
│   ├── 1.3.1 Reposicionamento de pontos de água fria
│   ├── 1.3.2 Instalação de ponto de água quente (se novo)
│   ├── 1.3.3 Reposicionamento de esgoto (vaso, ralo, lavatório)
│   ├── 1.3.4 Instalação de registros (pressão e gaveta)
│   └── 1.3.5 Teste de estanqueidade
│
├── 1.4 INSTALAÇÕES ELÉTRICAS
│   ├── 1.4.1 Novo ponto de iluminação (se alterar posição)
│   ├── 1.4.2 Novos pontos de tomada
│   ├── 1.4.3 Ponto de ducha higiênica
│   └── 1.4.4 Ponto de chuveiro (circuito exclusivo)
│
├── 1.5 IMPERMEABILIZAÇÃO
│   ├── 1.5.1 Regularização de piso (caimento para ralo)
│   ├── 1.5.2 Aplicação de manta asfáltica ou membrana
│   ├── 1.5.3 Subida nas paredes (mínimo 30cm, box integral)
│   └── 1.5.4 Teste de estanqueidade (48h)
│
├── 1.6 REVESTIMENTOS
│   ├── 1.6.1 Contrapiso (5cm, sarrafeado)
│   ├── 1.6.2 Assentamento de piso
│   ├── 1.6.3 Assentamento de revestimento de parede
│   ├── 1.6.4 Rejuntamento
│   └── 1.6.5 Aplicação de soleira (box, porta)
│
├── 1.7 FORRO
│   ├── 1.7.1 Estrutura de forro de gesso acartonado
│   ├── 1.7.2 Passagem de pontos elétricos no forro
│   └── 1.7.3 Fechamento e acabamento (tabica ou moldura)
│
├── 1.8 ESQUADRIAS
│   ├── 1.8.1 Instalação de porta (se nova)
│   ├── 1.8.2 Instalação de box de vidro temperado
│   └── 1.8.3 Ajuste de batentes e guarnições
│
├── 1.9 PINTURA
│   ├── 1.9.1 Fundo preparador (parede e teto não revestidos)
│   ├── 1.9.2 Massa corrida (se aplicável)
│   └── 1.9.3 Pintura de acabamento (teto)
│
├── 1.10 LOUÇAS E METAIS
│   ├── 1.10.1 Instalação de vaso sanitário
│   ├── 1.10.2 Instalação de lavatório/cuba
│   ├── 1.10.3 Instalação de torneiras e misturadores
│   ├── 1.10.4 Instalação de chuveiro/ducha
│   ├── 1.10.5 Instalação de acessórios (papeleira, saboneteira, espelho)
│   └── 1.10.6 Teste final de funcionamento
│
└── 1.11 LIMPEZA E ENTREGA
    ├── 1.11.1 Limpeza grossa (remoção de resíduos)
    ├── 1.11.2 Limpeza fina (rejunte, vidros, metais)
    └── 1.11.3 Retirada de proteções e entrega ao cliente
```

### 3.2 Pacotes de Trabalho para Orçamento

| Código | Pacote | Unidade | Quantidade |
|--------|--------|---------|------------|
| 1.2 | Demolição completa | vb | 1 |
| 1.3 | Instalações hidráulicas | pt | 5 |
| 1.4 | Instalações elétricas | pt | 4 |
| 1.5 | Impermeabilização | m² | 5 |
| 1.6.1 | Contrapiso | m² | 4 |
| 1.6.2-4 | Piso cerâmico | m² | 4,5 |
| 1.6.3 | Revestimento parede | m² | 16 |
| 1.7 | Forro de gesso | m² | 4 |
| 1.8.2 | Box vidro | m² | 2 |
| 1.10 | Louças e metais (instalação) | cj | 1 |

---

## 4. Critérios de Encerramento de Etapa

### 4.1 Checklists por Macro-Fase

**2. DEMOLIÇÃO — Critérios de Aceite:**
- [ ] Todas as superfícies especificadas foram removidas
- [ ] Entulho foi retirado (caçamba liberada)
- [ ] Instalações existentes estão expostas e identificadas
- [ ] Área limpa e pronta para próxima etapa
- [ ] Fotos de registro (antes/durante/depois)

**4. INSTALAÇÕES HIDRÁULICAS — Critérios de Aceite:**
- [ ] Todos os pontos de água conforme projeto
- [ ] Todos os pontos de esgoto conforme projeto
- [ ] Registros instalados e funcionando
- [ ] Teste de pressão realizado (sem vazamentos)
- [ ] Teste de caimento de esgoto (vazão livre)
- [ ] Projeto as-built atualizado

**6. IMPERMEABILIZAÇÃO — Critérios de Aceite:**
- [ ] Superfície regularizada com caimento
- [ ] Manta/membrana aplicada conforme especificação
- [ ] Subida nas paredes conforme altura especificada
- [ ] Teste de lâmina d'água 48h sem infiltração
- [ ] Laudo ou registro fotográfico do teste

**8. REVESTIMENTOS — Critérios de Aceite:**
- [ ] Alinhamento e prumo conferidos
- [ ] Juntas uniformes
- [ ] Sem peças trincadas ou soltas
- [ ] Rejunte aplicado e limpo
- [ ] Soleiras e acabamentos de borda instalados

---

## 5. Gestão de Mudanças na EAP

### 5.1 Processo de Controle de Mudança

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Solicitação│ ──► │   Análise   │ ──► │  Aprovação  │ ──► │ Incorporação│
│  de Mudança │     │ de Impacto  │     │   Cliente   │     │   na EAP    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │  Impacto em │
                    │ Custo/Prazo │
                    └─────────────┘
```

### 5.2 Registro de Aditivo

| Campo | Descrição |
|-------|-----------|
| **Nº da Mudança** | Sequencial (M-001, M-002...) |
| **Data** | Data da solicitação |
| **Descrição** | O que será alterado |
| **Justificativa** | Por que é necessário |
| **Impacto em Custo** | R$ adicional ou (economia) |
| **Impacto em Prazo** | Dias adicionais ou (redução) |
| **Aprovação** | Assinatura do cliente |

---

## 6. Cronograma Derivado da EAP

### 6.1 Estimativa de Duração

| Macro-Fase | Duração Típica (Banheiro 4m²) |
|------------|------------------------------|
| 1. Preliminares | 0,5 dia |
| 2. Demolição | 1 a 2 dias |
| 3. Estrutura/Vedação | N/A (sem nova alvenaria) |
| 4. Hidráulica | 2 dias |
| 5. Elétrica | 1 dia |
| 6. Impermeabilização | 1 dia (+ 2 dias cura/teste) |
| 7. Contrapiso | 1 dia (+ 3 dias cura) |
| 8. Revestimentos | 3 a 4 dias |
| 9. Forro | 1 dia |
| 10. Esquadrias | 0,5 dia |
| 11. Pintura | 1 dia |
| 12. Louças e Metais | 1 dia |
| 14. Limpeza | 0,5 dia |
| **TOTAL** | **15 a 20 dias úteis** |

### 6.2 Caminho Crítico

O **caminho crítico** é a sequência mais longa de atividades dependentes:

```
Demolição → Hidráulica → Impermeabilização → (Cura) → Contrapiso → (Cura) → Revestimentos → Louças
```

**Qualquer atraso nessa cadeia atrasa a obra inteira.**

---

## 7. Ferramentas Recomendadas

| Ferramenta | Uso | Custo |
|------------|-----|-------|
| **Excel** | EAP simples, orçamento | Gratuito/Office |
| **MS Project** | Cronograma com dependências | Pago |
| **Monday/Trello** | Gestão visual de tarefas | Freemium |
| **ProjectLibre** | Alternativa gratuita ao MS Project | Gratuito |
| **Power BI** | Dashboard de progresso | Freemium |

---

## 8. Checklist de Validação da EAP

- [ ] A EAP cobre 100% do escopo contratado?
- [ ] Cada pacote de trabalho tem um responsável claro?
- [ ] As dependências estão mapeadas corretamente?
- [ ] Há critérios de aceite definidos para cada macro-fase?
- [ ] A estrutura permite rastrear custo e cronograma por pacote?
- [ ] Há processo definido para mudanças de escopo?
- [ ] O cliente validou e aprovou a EAP?

---

*Metodologia baseada no PMBOK (PMI) e práticas do mercado de reformas residenciais.*

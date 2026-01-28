---
name: Cálculo de Quantidades e Consumos
description: Regras e coeficientes técnicos para levantamento de quantitativos de materiais e serviços em obras de reforma.
---

# Cálculo de Quantidades e Consumos

Esta skill orienta o Agente Engenheiro no levantamento preciso de materiais, aplicando coeficientes de consumo e perdas.

## 1. Alvenaria e Vedações

### 1.1 Paredes de Blocos (Cerâmico ou Concreto)
*   **Área:** Comprimento x Altura (descontar vãos > 2m²).
*   **Blocos:**: 12,5 a 13 unidades/m² (bloco padrão 39x19cm). 
    *   *Perda:* +10%.
*   **Argamassa de Assentamento:** 15 a 20 kg/m² (junta de 1,5cm).

### 1.2 Paredes de Drywall
*   **Área:** Comprimento x Altura (ambas as faces se for parede completa).
*   **Chapas (1,20x1,80m = 2,16m² ou 1,20x2,40m = 2,88m²):**
    *   Cálculo: (Área Parede x 2 faces) / Área Placa.
    *   *Perda:* +5% a 8%.
*   **Montantes (Perfis Verticais):**
    *   Espaçamento 60cm: (Comprimento Parede / 0,60) * 2 (se for parede dupla) ou * 1 (se for revestimento).
    *   Espaçamento 40cm (áreas molhadas/azulejo): (Comprimento / 0,40).
*   **Guias (Perfis Horizontais):** (Comprimento Parede x 2) (piso e teto).
*   **Parafusos:**
    *   GN25 (Placa-Perfil): 30 a 40 un/m² de parede pronta.
*   **Banda Acústica:** Perímetro da parede (m linear).

---

## 2. Revestimentos de Piso e Parede

### 2.1 Contrapiso (Argamassa)
*   **Volume:** Área (m²) x Espessura média (m). (Ex: 50m² x 0,05m = 2,5m³).
*   **Cimento/Areia (Traço 1:3):**
    *   Cimento: ~300 kg/m³.
    *   Areia: ~1,1 m³/m³.
*   **Argamassa Industrializada:** ~20 kg/m² para cada 1cm de espessura.

### 2.2 Cerâmicas e Porcelanatos
*   **Área de Piso:** Área do cômodo + Rodapé (Perímetro x Altura Rodapé).
    *   *Perda:* 
        *   Assentamento Reto: +10%.
        *   Assentamento Diagonal (45º): +15 a 20%.
*   **Área de Parede:** Perímetro x Altura (descontar portas/janelas).
*   **Argamassa Colante (AC-I, AC-II, AC-III):**
    *   Colagem Simples (peças até 30x30): 4 a 5 kg/m².
    *   Colagem Dupla (peças > 30x30): 7,5 a 8,5 kg/m².
*   **Rejunte:**
    *   Calculado em função da largura da junta e dimensões da peça.
    *   Estimativa rápida: 
        *   Peças grandes (60x60, junta 2mm): ~0,20 kg/m².
        *   Peças pequenas (pastilhas): > 1,5 kg/m².

---

## 3. Pintura

### 3.1 Tinta Látex/Acrílica (Paredes/Teto)
*   **Área:** (Perímetro x Altura) + Teto.
*   **Rendimento (Lata 18L):**
    *   Massa Corrida: ~30 a 40 m² (2 a 3 demãos) por lata.
    *   Tinta Acabamento: ~80 a 100 m² (2 a 3 demãos) por lata acabada.
    *   Selador: ~100 a 120 m² por lata.
*   *Consumo estimado:* 0,2 a 0,3 Litros/m² (sistema completo).

---

## 4. Instalações Elétricas (Estimativa Rápida)

*   **Fios e Cabos:**
    *   Levantamento preciso requer projeto ponto a ponto.
    *   *Estimativa:* Distância linear entre pontos + 10% (curvas) + Sobras nas caixas (0,30m a 0,50m por ponta).
*   **Eletrodutos:**
    *   Distância linear + 15%.

---

## 5. Tabela de Perdas Padrão (SINAPI/TCPO)

| Material | Perda Recomendada |
|----------|-------------------|
| Aço (CA-50/60) | 10% |
| Cimento | 5% |
| Areia/Brita | 10% a 15% (granel) |
| Blocos/Tijolos | 10% |
| Cerâmica/Piso | 10% (reto) / 15% (diag.) |
| Tinta | 5% a 10% |
| Madeira (Formas) | 15% a 20% |
| Tubos PVC | 5% a 8% |
| Fios/Cabos | 5% |

## 6. Como usar esta Skill

1.  Extraia as **Áreas e Perímetros** do arquivo JSON do projeto (SpaceId -> area/height).
2.  Identifique o **Serviço** a ser orçado.
3.  Aplique a fórmula correspondente para encontrar a quantidade de insumos.
4.  Adicione a **Percentagem de Perda** sobre o total calculado.
5.  O resultado é a quantidade de compra (Purchase Quantity).

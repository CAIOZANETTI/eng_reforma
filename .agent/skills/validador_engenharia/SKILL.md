name: Validador Engenharia
description: O Engenheiro Civil - Valida coerência técnica e física do projeto.
version: 1.0
dependencies: []
---

# Skill: Validador Engenharia

## Descrição
Executa testes lógicos "físicos" sobre o JSON gerado.

## Inputs
- `projeto.json`

## Outputs
- `report_engenharia.txt` (Aprovado ou Reprovado com motivos)

## Rules Check
- Quantidades não negativas.
- Densidade de Serviço (ex: não pode ter 100m² de piso em banheiro de 4m² - *implementação simples por enquanto*).

## Scripts

### `scripts/validate_engineering.py`
Verifica sanidade dos números.

**Uso:**
```bash
python validate_engineering.py --input_file ../../../../.agent/output/projeto.json
```

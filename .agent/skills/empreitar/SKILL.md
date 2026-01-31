---
name: Empreitar
description: Interface para receber prompts do cliente e converter em tabela estruturada
version: 1.0
dependencies: []
---

# Skill: Empreitar

## Objetivo
Processar prompts em linguagem natural do cliente (empreiteiro) e converter para uma estrutura de dados tabular que pode ser processada pelos demais skills.

## Entradas
- Prompt em texto livre do usuário
- Contexto opcional (tipo de imóvel, região, orçamento)

## Saídas
- Tabela estruturada (CSV/JSON) com:
  - Tipo de imóvel
  - Ambientes
  - Serviços desejados
  - Padrão de acabamento
  - Área estimada

## Scripts Disponíveis

### `scripts/prompt_tabela.py`
Converte texto livre em tabela estruturada.

```bash
python prompt_tabela.py --prompt "Quero reformar o banheiro do meu apartamento de 60m2, trocar piso e louças"
```

**Saída esperada:**
```json
{
  "tipo": "apto",
  "area_total": 60,
  "ambientes": [
    {
      "nome": "Banheiro",
      "servicos": ["troca de piso", "troca de louças"],
      "area_estimada": 5
    }
  ],
  "acabamento": "medio"
}
```

### `scripts/normalizar_prompt.py`
Limpa e normaliza o texto do prompt.

```bash
python normalizar_prompt.py --input "quero reformar mea casa" --output "quero reformar minha casa"
```

## Exemplos Disponíveis

### `examples/prompts.md`
Lista de prompts comuns e suas interpretações.

```markdown
## Prompt 1
**Entrada**: "Preciso reformar a cozinha, trocar armários e bancada"
**Interpretação**:
- Ambiente: Cozinha
- Serviços: Marcenaria, Bancada
- Padrão: Médio (inferido)

## Prompt 2
**Entrada**: "Reforma completa do banheiro com porcelanato e louças Deca"
**Interpretação**:
- Ambiente: Banheiro
- Serviços: Revestimento, Louças
- Padrão: Luxo (inferido por "Deca")
```

## Recursos Disponíveis

### `resources/linguagem_empreiteiro.md`
Dicionário de termos comuns usados por empreiteiros e clientes.

```markdown
| Termo Popular | Termo Técnico |
|---------------|---------------|
| "trocar o chão" | Troca de piso |
| "mexer na elétrica" | Instalações elétricas |
| "dar uma pintura" | Pintura completa |
| "arrumar o vazamento" | Reparo hidráulico |
| "colocar gesso" | Forro de gesso |
```

### `resources/sinonimos.json`
Mapeamento de sinônimos para normalização.

```json
{
  "banheiro": ["wc", "toilette", "lavabo", "sanitário"],
  "cozinha": ["copa", "área de cozinha"],
  "piso": ["chão", "pavimento", "revestimento de piso"],
  "louça": ["vaso", "pia", "cuba", "sanitário"]
}
```

## Regras de Inferência

### Padrão de Acabamento
| Indicadores | Padrão |
|-------------|--------|
| "barato", "simples", "básico" | Popular |
| "bom", "normal", "padrão" | Médio |
| "Deca", "Portobello", "premium", "design" | Luxo |

### Área por Imóvel
| Configuração | Área Estimada |
|--------------|---------------|
| 1Q+1B | 35-45 m² |
| 2Q+1B | 50-65 m² |
| 3Q+2B | 80-100 m² |
| 4Q+3B | 120-180 m² |

## Tratamento de Ambiguidade

Quando o prompt for ambíguo, o script deve:
1. Identificar a ambiguidade
2. Sugerir interpretações possíveis
3. Escolher a mais provável (com flag de baixa confiança)

```json
{
  "interpretacao": "...",
  "confianca": 0.6,
  "alternativas": ["...", "..."]
}
```

## Uso no Pipeline

```
[Prompt do Usuário] \u2192 empreitar \u2192 [Tabela Estruturada] \u2192 projetar
```

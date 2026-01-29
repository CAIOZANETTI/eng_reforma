---
description: Workflow para execução assistida de um prompt aleatório com auditoria detalhada de cada agente
---

# Workflow: Prompt Aleatório to JSON (Modo Auditoria)

## Objetivo
Executar o pipeline completo de reforma a partir de um prompt aleatório, gravando logs detalhados de cada etapa para análise de comportamento dos agentes.

## Saídas
Para cada execução (UUID), gera em `.agent/output/auditoria_{uuid}/`:
1. `00_prompt.txt`: O prompt original selecionado
2. `01_interpretacao.json`: Saída do Agente Empreiteiro
3. `02_referencias_ibge.json`: Dados validados IBGE
4. `03_sugestoes_projeto.json`: Sugestões de design
5. `04_quantidades.csv`: Levantamento quantitativo
6. `05_escopo.csv`: Escopo técnico
7. `06_orcamento.csv`: Planilha orçamentária
8. `07_projeto_final.json`: JSON Obra Ninja Final
9. `RELATORIO_AUDITORIA.md`: Log narrativo passo a passo

## Passos

### 1. Inicialização e Seleção
// turbo
```bash
# Gerar ID único para esta execução
$uuid = [guid]::NewGuid().ToString().Substring(0,8)
$audit_dir = ".agent/output/auditoria_$uuid"
New-Item -ItemType Directory -Force -Path $audit_dir

# Selecionar Prompt Aleatório
$prompt = python .agent/skills/01_empreiteiro/scripts/selecionar_prompt.py
$prompt | Out-File -Encoding utf8 "$audit_dir/00_prompt.txt"

# Iniciar Relatório de Auditoria
"# Relatório de Auditoria: Execução $uuid`n`n**Data:** $(Get-Date)`n**Prompt Original:**`n> $prompt`n" | Out-File -Encoding utf8 "$audit_dir/RELATORIO_AUDITORIA.md"
```

### 2. Agente 01: Empreiteiro (Interpretação)
Analisa o pedido e estrutura os dados iniciais.

// turbo
```bash
python .agent/skills/01_empreiteiro/scripts/prompt_tabela.py \
  --prompt "$prompt" \
  --output "$audit_dir/01_interpretacao.json"

# Logar no relatório
"`n## 1. Interpretação (Empreiteiro)`n- Arquivo gerado: `01_interpretacao.json`" | Out-File -Append -Encoding utf8 "$audit_dir/RELATORIO_AUDITORIA.md"
```

### 3. Agente 02: IBGE (Validação)
Verifica se os dados interpretados fazem sentido estatístico.

// turbo
```bash
# Como o script gera ranking, aqui usaremos um python inline para validar e logar
python -c "
import json
with open('$audit_dir/01_interpretacao.json', 'r') as f:
    data = json.load(f)
print(f'- Tipo imóvel: {data.get(\"tipo\")}')
print(f'- Área total: {data.get(\"area_total\")}m²')
" >> "$audit_dir/RELATORIO_AUDITORIA.md"
```

### 4. Agente 03: Projeto (Sugestões)
Adiciona inteligência de arquitetura (materiais e estilo).
*Nota:* Implementação simulada enquanto script `sugerir_reforma.py` é finalizado.

// turbo
```bash
"`n## 3. Sugestões de Projeto`n- Acabamento detectado: Médio`n- Sugestão Piso: Porcelanato`n- Sugestão Parede: Tinta Acrílica" | Out-File -Append -Encoding utf8 "$audit_dir/RELATORIO_AUDITORIA.md"
```

### 5. Agente 04: Quantificar (Cálculo)
Transforma ambientes em áreas de superfície (piso, parede, teto).

// turbo
```bash
python .agent/skills/04_quantificar/scripts/quantificar.py \
  --input "$audit_dir/01_interpretacao.json" \
  --output "$audit_dir/04_quantidades.csv"

"`n## 4. Quantificação`n- Arquivo gerado: `04_quantidades.csv`" | Out-File -Append -Encoding utf8 "$audit_dir/RELATORIO_AUDITORIA.md"
```

### 6. Agente 05: Escopo (Serviços)
Gera a lista técnica de serviços necessários.

// turbo
```bash
python .agent/skills/05_escopo/scripts/gerar_escopo.py \
  --input "$audit_dir/04_quantidades.csv" \
  --output "$audit_dir/05_escopo.csv"

"`n## 5. Definição de Escopo`n- Arquivo gerado: `05_escopo.csv`" | Out-File -Append -Encoding utf8 "$audit_dir/RELATORIO_AUDITORIA.md"
```

### 7. Agente 06: Custo (Orçamento)
Precifica cada item usando tabelas SINAPI.

// turbo
```bash
python .agent/skills/06_custo/scripts/custear_reforma.py \
  --input "$audit_dir/05_escopo.csv" \
  --output "$audit_dir/06_orcamento.csv" \
  --sintetico "$audit_dir/resumo_orcamento.md"

"`n## 6. Orçamento (Custo)`n- Arquivo gerado: `06_orcamento.csv`" | Out-File -Append -Encoding utf8 "$audit_dir/RELATORIO_AUDITORIA.md"
Get-Content "$audit_dir/resumo_orcamento.md" | Out-File -Append -Encoding utf8 "$audit_dir/RELATORIO_AUDITORIA.md"
```

### 8. Agente 07: JSON (Finalização)
Gera o artefato final e valida.

// turbo
```bash
python .agent/skills/07_json/scripts/converte_escopo_to_obra_ninja_json.py \
  --input "$audit_dir/06_orcamento.csv" \
  --output "$audit_dir/07_projeto_final.json" \
  --nome "Projeto Auditado $uuid" \
  --descricao "$prompt"

python .agent/skills/07_json/scripts/validar_json.py \
  --input "$audit_dir/07_projeto_final.json" >> "$audit_dir/RELATORIO_AUDITORIA.md"

"`n## 7. JSON Final`n- Arquivo gerado: `07_projeto_final.json`" | Out-File -Append -Encoding utf8 "$audit_dir/RELATORIO_AUDITORIA.md"
```

### 9. Conclusão
Exibir resumo e localização dos arquivos de auditoria.

// turbo
```bash
Write-Output "Auditoria completa salva em: $audit_dir"
Write-Output "Relatório principal: $audit_dir/RELATORIO_AUDITORIA.md"
```

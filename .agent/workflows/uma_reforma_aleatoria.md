---
description: Gera uma reforma aleatória completa, desde o prompt até o JSON final
---

1. Gerar Orçamento (Markdown)
// turbo
cd .agent/skills/cria_orcamento/scripts && python gerar_orcamento.py --prompt "Reforma completa de banheiro com pintura de teto e troca de piso por porcelanato" --kb_dir ../../../../.agent/knowledge_base --output ../../../../.agent/output/orcamento_banheiro.md

2. Validar Orçamento
// turbo
cd .agent/skills/valida_orcamento/scripts && python validar_dados.py --input ../../../../.agent/output/orcamento_banheiro.md --kb_dir ../../../../.agent/knowledge_base

3. Converter para JSON Obra Ninja
// turbo
cd .agent/skills/orcamento_obra_ninja/scripts && python converter_json.py --input ../../../../.agent/output/orcamento_banheiro.md --output_dir ../../../../.agent/output

4. Verificar Saídas
// turbo
ls -l ../.agent/output

---
description: Pipeline rigoroso para gerar variações de projeto mantendo integridade relacional SQL
---

1. Minerar Whitelist (Auditor)
// turbo
cd .agent/skills/minerador_relacional/scripts && python map_relational_ids.py --input_dir ../../../../obra_ninja/json --output_file ../../../../.agent/knowledge_base/whitelist.json

2. Gerar Variação 1.5x (Projetista)
// turbo
cd .agent/skills/gerador_json/scripts && python generate_variation.py --template ../../../../obra_ninja/json/banheiro_empregada_em_lavabo_f43e99d5-a4f7-45a0-bc6e-2db068f9e605.json --scale 1.5 --output_dir ../../../../.agent/output

3. Listar arquivo gerado
// turbo
ls -t ../../../../.agent/output/reforma_var_*.json | head -n 1

4. Validar Engenharia (Engenheiro)
// turbo
cd .agent/skills/validador_engenharia/scripts && python validate_engineering.py --input_file $(ls -t ../../../../.agent/output/reforma_var_*.json | head -n 1)

5. Validar Schema SQL (Programador)
// turbo
cd .agent/skills/validador_schema/scripts && python validate_schema.py --input_file $(ls -t ../../../../.agent/output/reforma_var_*.json | head -n 1) --whitelist ../../../../.agent/knowledge_base/whitelist.json

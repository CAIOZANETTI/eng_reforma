---
description: Pipeline para minerar dados de projetos JSON (Obra Ninja) e criar base de conhecimento CSV
---

1. Minerar JSONs e Criar CSVs
// turbo
cd .agent/skills/obra_ninja/scripts && python3 minerar_json.py --input_dir ../../../../obra_ninja/json --output_dir ../../../../.agent/knowledge_base

2. Listar arquivos
// turbo
ls -l ../.agent/knowledge_base

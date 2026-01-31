---
description: Pipeline para minerar dados de projetos JSON e criar base de conhecimento CSV
---

1. Extrair Catálogos (Materiais, Mão de Obra, Categorias)
// turbo
cd .agent/skills/minerar_dados/scripts && python extrair_catalogos.py --input_dir ../../../../obra_ninja/json --output_dir ../../../../.agent/knowledge_base

2. Extrair Definições de Serviços
// turbo
cd .agent/skills/minerar_dados/scripts && python extrair_servicos.py --input_dir ../../../../obra_ninja/json --output_dir ../../../../.agent/knowledge_base

3. Listar arquivos gerados
// turbo
ls -l ../.agent/knowledge_base

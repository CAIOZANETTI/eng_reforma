---
description: Converte um orçamento em Markdown de volta para o JSON oficial do Obra Ninja
---

1. Converter MD para JSON
// turbo
cd .agent/skills/orcamento_obra_ninja/scripts && python converter_json.py --input ${MD_FILE_PATH} --output_dir ../../../../.agent/output

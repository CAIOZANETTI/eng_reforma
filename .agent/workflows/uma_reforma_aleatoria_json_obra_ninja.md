---
description: Workflow para gerar uma reforma aleatória completa e exportar seu JSON seguindo o pipeline Obra Ninja
---

1. Gerar um tipo de imóvel aleatório do Ranking IBGE
// turbo
cd .agent/skills/mapear_imoveis/scripts && python gerar_ranking.py --random 1 --output ../../../outputs/imovel_base.json

2. Projetar a reforma para o imóvel selecionado
// turbo
cd .agent/skills/projetar/scripts && python sugerir_reforma.py --input ../../../outputs/imovel_base.json --output ../../../outputs/projeto_sugerido.json

3. Quantificar os serviços da reforma
// turbo
cd .agent/skills/quantificar/scripts && python quantificar_imovel.py --input ../../../outputs/projeto_sugerido.json --output ../../../outputs/quantidades.csv

4. Detalhar o escopo de serviços (EAP)
// turbo
cd .agent/skills/detalhar/scripts && python gerar_escopo.py --input ../../../outputs/quantidades.csv --output ../../../outputs/escopo_detalhado.csv

5. Custear a reforma (SINAPI)
// turbo
cd .agent/skills/custear/scripts && python custear_reforma.py --input ../../../outputs/escopo_detalhado.csv --output ../../../outputs/orcamento_custeado.csv

6. Exportar para JSON Obra Ninja
// turbo
cd .agent/skills/exportar/scripts && python converte_escopo_to_obra_ninja_json.py --input ../../../outputs/orcamento_custeado.csv --output ../../../outputs/projeto_final.json

7. Gerar relatório explicativo do processo
// turbo
echo "Gerando relatório final..." && python ../../../.agent/scripts/gerar_relatorio_pipeline.py --input ../../../outputs/projeto_final.json --output ../../../outputs/relatorio_processo.md

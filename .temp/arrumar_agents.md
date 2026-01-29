seguinte quero organizar a estrutura dos agentes

agent/rules/reforma_sem_ampliacao.md
agent/rules/uso_python_obrigatorio.md
agent/rules/uso_python_obrigatorio.md

workflows/json_refoma.md ( utilizar as skill para criar um json de reforma valido padrão obra ninja)

agent/skills/imoveis_brasil/skill.md  (rastrear tipo de moradia no brasil, tipo )
agent/skills/imoveis_brasil/scripts/  ()
agent/skills/imoveis_brasil/exemplos/ (tabelas de areas de moradias, apto, casa, escritorios)
agent/skills/imoveis_brasil/exemplos/ (ranking das moradias no brasil qual tipo tem mais)
agent/skills/imoveis_brasil/resource/ (dados de ibge)
agent/skills/imoveis_brasil/resource/ (dados reais de imoveis no brasil seconci )

agent/skills/empreiteiro/skill.md  (cliente que vai escrever um prompt e quer um orçamento)
agent/skills/empreiteiro/scripts/  (prompt_tabela.py codigo para converter escrita para tabela)
agent/skills/empreiteiro/exemplos/ (lista de possiveis prompts que o usuario pode pedir)
agent/skills/empreiteiro/resource/ (forma de lingugem do empreitiro)

agent/skills/projeto_reformas/skill.md  (dar opção de reforma para tipos de imoveis)
agent/skills/projeto_reformas/scripts/  (area conforme classe social, n banheiros conforme classe social)
agent/skills/projeto_reformas/exemplos/ (lista de revestimentos cores...)
agent/skills/projeto_reformas/exemplos/ (tendencia de reformas pinterest, locacao_airbnb, retrofit_casa)
agent/skills/projeto_reformas/resource/ (normas de acessibilidade, criterio projeto, iluminacao)
agent/skills/projeto_reformas/resource/ (paleta de cores, combinações, tendencias, conforto termico, acustico)
agent/skills/projeto_reformas/resource/ (padrão de acabamento popular, medio, luxo)

agent/skills/quantificar_reforma/skill.md  (com base na area e tipo do imovel, quantificar os serviços, area piso, parede, janela porta)
agent/skills/quantificar_reforma/scripts/  (criar um codigo python com entrada do imovel retorna area dos ambientes e quantidades)
agent/skills/quantificar_reforma/exemplos/ (exomplo de planlha do script)
agent/skills/quantificar_reforma/resource/ (normas e conceitos de para deteminar area dos ambientes e altura pe direito)

agent/skills/escopo_reforma/skill.md  (com base na area e tipo do imovel, quantificar os serviços, area piso, parede, janela porta)
agent/skills/escopo_reforma/scripts/  ( criar um codigo python com entrada do imovel retorna area dos ambientes e quantidades)
agent/skills/escopo_reforma/exemplos/ (exomplo de planlha do script)
agent/skills/escopo_reforma/resource/ (normas e conceitos de para deteminar area dos ambientes e altura pe direito)

agent/skills/custo_reforma/skill.md  (custear a reforma com base nos custos sinapi)
agent/skills/custo_reforma/scripts/  (recebe um escopo.csv e coloca preço unitario e parcial e total nas obra)
agent/skills/custo_reforma/exemplos/ (tabela sinapi, testar o um script para eu validar)
agent/skills/custo_reforma/resource/ (preços de serviços e materiais em .csv)

agent/skills/escopo_json/skill.md  (atraves do skills/escopo_reforma/skill.md, montar um json seguindo modelo, seguindo o id da lista de ambiente e materiais )
agent/skills/escopo_json/scripts/  (converte_escopo_to_obra_ninja_json.py, validar_json.py)
agent/skills/escopo_json/exemplos/ (obra_ninja_schema.json)
agent/skills/escopo_json/resource/ (lista_materiais.csv)
agent/skills/escopo_json/resource/ (lista_ambientes.csv)









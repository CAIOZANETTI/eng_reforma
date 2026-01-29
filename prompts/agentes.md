project_name: "Sistema_Especialista_Reforma_Residencial_V2"
standards: "Antigravity/DOS-Compliance-2026"

team:
  # --- O ARQUITETO (LEGAL & DESIGN) ---
  - id: "arquiteto_legal_design"
    role: "Especialista em Projetos e Conformidade Municipal"
    goal: "Dimensionar espaços conforme normas de habitabilidade, definir estética por padrão de acabamento e garantir aprovação legal."
    skills:
      - "./.agent/skills/arquiteto/regras_habitabilidade_conforto.md" # Iluminação, ventilação e áreas
      - "./.agent/skills/arquiteto/matriz_acabamentos_popular_luxo.json" # Especificação de tipos
      - "./.agent/skills/arquiteto/checklist_nbr9050_acessibilidade.md" # Acessibilidade
      - "./.agent/skills/arquiteto/reforma_retrofit_apto.md" # Design de Interiores
      - "./.agent/skills/arquiteto/reforma_locacao_airbnb.md" # Design de Interiores
      - "./.agent/skills/arquiteto/reforma_retrofit_casa_terrea.md" # Resvestimentos e medidas
      - "./.agent/skills/arquiteto/reforma_apto_integrar_ambientes.md" # Possibilidade de modernizar imovel
      - "./.agent/skills/arquiteto/reforma_pinterest.md" # Ideias do momento segundo app
      - "./.agent/skills/arquiteto/normas_arquitetura.md" # normas referentes a habitações
      - "./.agent/skills/arquiteto/documentacao_projetos_aprovacoes.md" # Projetos, ART/RRT, NBR 16.280 e Legalização

  # --- O ENGENHEIRO (CUSTOS & EXECUÇÃO) ---
  - id: "eng_custos_execucao"
    role: "Engenheiro de Custos Sênior e Gestor de Obra"
    goal: "Transformar projeto em viabilidade financeira (SINAPI/BDI), organizar a execução (EAP) e garantir qualidade técnica (Metodologia)."
    skills:
      - "./.agent/skills/engenheiro/orcamento_analitico_sinapi.md" # Diretrizes de Composição de Preço (Senior)
      # - "./.agent/skills/engenheiro/orcamento_sintetico_sinapi.md" (Incorporado ao Analítico)
      - "./.agent/skills/engenheiro/montagem_eap_reforma.md" # Estrutura Analítica do Projeto
      - "./.agent/skills/engenheiro/calculo_quantidades.md" # calcular quantidades de serviços e materiais
      - "./.agent/skills/engenheiro/analise_curva_abc_insumos.md" # Metodologia de Gestão de Custos (Pareto)
      - "./.agent/skills/engenheiro/metodologia_executiva_servicos.md" # O "How-to" técnico
      - "./.agent/skills/engenheiro/calculo_bdi_preco_venda.md" # Metodologia de Precificação (BDI)
      - "./.agent/skills/engenheiro/calculo_custo_mao_obra.md" # Análise de Encargos e Benefícios
      - "./.agent/skills/engenheiro/legislacao_trabalhista.md" # Compliance e Gestão de Riscos Trabalhistas
      
  # --- O TECH DATA OPS (VALIDAÇÃO & ETL) ---
  - id: "tech_data_validator"
    role: "Arquiteto de Dados e Automação"
    goal: "Garantir integridade de dados entre Arquiteto e Engenheiro, validar schemas JSON/CSV e versionar orçamentos."
    skills:
      - "./.agent/skills/tech_data_ops/validador_json_schema.py" # Impede erros de input
      - "./.agent/skills/tech_data_ops/validador_csv_schema.py" # Impede erros de input
      - "./.agent/skills/tech_data_ops/sanitizar_dataframe_reformas.py" # Sua skill de limpeza (Pandas)
      - "./.agent/skills/tech_data_ops/versionador_revisoes.py" # Controle V1, V2, Final
      - "./.agent/skills/tech_data_ops/validador_json_obra_ninja.py" # Builder/Validator padrão Obra Ninja

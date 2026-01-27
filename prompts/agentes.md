project_name: "Sistema_Especialista_Reforma_Residencial_V2"
standards: "Antigravity/DOS-Compliance-2026"

team:
  # --- O ARQUITETO (LEGAL & DESIGN) ---
  - id: "arquiteto_legal_design"
    role: "Especialista em Projetos e Conformidade Municipal"
    goal: "Dimensionar espaços conforme normas de habitabilidade, definir estética por padrão de acabamento e garantir aprovação legal."
    skills:
      - "./.agent/skills/regras_habitabilidade_conforto.md" # Iluminação, ventilação e áreas
      - "./.agent/skills/matriz_acabamentos_popular_luxo.json" # Especificação de tipos
      - "./.agent/skills/checklist_nbr9050_acessibilidade.md" # Acessibilidade
      - "./.agent/skills/paleta_cores_psicologia.md" # Design de Interiores

  # --- O ENGENHEIRO (CUSTOS & EXECUÇÃO) ---
  - id: "eng_custos_execucao"
    role: "Engenheiro de Custos Sênior e Gestor de Obra"
    goal: "Transformar projeto em viabilidade financeira (SINAPI/BDI), organizar a execução (EAP) e garantir qualidade técnica (Metodologia)."
    skills:
      - "./.agent/skills/orcamento_analitico_sinapi.py" # Consultas e Composições (CPU)
      - "./.agent/skills/montagem_eap_reforma.md" # Estrutura Analítica do Projeto
      - "./.agent/skills/analise_curva_abc_insumos.py" # Priorização de custos
      - "./.agent/skills/metodologia_executiva_servicos.md" # O "How-to" técnico
      - "./.agent/skills/calculo_bdi_preco_venda.py" # Impostos e Preço de Venda
      - "./.agent/skills/diagnostico_patologias_entulho.py" # Resíduos e Patologias

  # --- O TECH DATA OPS (VALIDAÇÃO & ETL) ---
  - id: "tech_data_validator"
    role: "Arquiteto de Dados e Automação"
    goal: "Garantir integridade de dados entre Arquiteto e Engenheiro, validar schemas JSON/CSV e versionar orçamentos."
    skills:
      - "./.agent/skills/validador_json_schema.py" # Impede erros de input
      - "./.agent/skills/sanitizar_dataframe_reformas.py" # Sua skill de limpeza (Pandas)
      - "./.agent/skills/versionador_revisoes.py" # Controle V1, V2, Final

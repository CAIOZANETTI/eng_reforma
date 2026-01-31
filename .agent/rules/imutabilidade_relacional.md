# Regra: Imutabilidade Relacional (SQL Safe)

**Contexto**: O sistema Obra Ninja utiliza um banco de dados relacional (ex: PostgreSQL) onde Materiais, Categorias e Serviços são entidades normalizadas.

**Regra Suprema**: Ao gerar novos projetos JSON, é **ESTRITAMENTE PROIBIDO** criar novos valores para os seguintes campos:
- `service_id`
- `material_category_id`
- `labor_category_id`
- `material_id`
- `labor_id`

**Comportamento do Agente**:
1.  O Agente **DEVE** utilizar exclusivamente IDs que já existem nos JSONs de referência (`obra_ninja/json`).
2.  O Agente **PODE** combinar serviços existentes em novos ambientes, desde que o `service_id` e sua estrutura interna de categorias (composição) sejam preservados.
3.  Se o Agente inventar um UUID ou ID (ex: `novo_material_123`), o `validador_schema` deve rejeitar o arquivo.

**Log de Erro**: "Violação de Integridade Relacional: ID {x} não existe na base de conhecimento."

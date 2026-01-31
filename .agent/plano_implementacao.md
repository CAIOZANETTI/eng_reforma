# Plano de Implementação: Gerador de Projetos Relacionais (SQL-Safe)

Este plano detalha a criação de um agente capaz de gerar novos projetos JSON variando apenas áreas e métricas, mantendo rigorosamente os IDs e estruturas relacionais existentes (Materiais, Serviços, Categorias) para integridade com banco de dados SQL.

## 🎯 Objetivo
Gerar novos arquivos `.json` que sejam **clones estruturais variáveis** dos projetos existentes.
- **Manter**: IDs (UUIDs) de materiais, categorias, serviços e labor.
- **Variar**: Áreas, alturas e quantidades (respeitando proporções de engenharia).
- **Validar**: Check duplo (Engenharia + Programação).

## 🏗️ Arquitetura de Agentes

### 1. Skills (Habilidades)

#### A. `minerador_relacional` (O Auditor)
- **Função**: Mapear todas as entidades válidas existentes nos JSONs da pasta `obra_ninja/json`.
- **Saída**: "White-list" de IDs compatíveis com o banco SQL. Mapeia também a relação `Serviço -> Composições` (quais materiais pertencem a qual serviço).

#### B. `gerador_json` (O Projetista)
- **Função**: Ler um projeto "template" e aplicar variações paramétricas.
- **Lógica**:
    - Alterar `total_area` do projeto.
    - Alterar `area` e `height` dos ambientes (`spaces`).
    - Recalcular `quantity` dos serviços proporcionalmente à nova geometria.
    - **Regra de Ouro**: JAMAIS criar novos `service_id` ou `material_id`. Apenas usar os existentes.

#### C. `validador_engenharia` (O Engenheiro Civil)
- **Função**: Validar coerência técnica.
- **Testes**:
    - "A quantidade de piso (m²) é compatível com a área do ambiente?"
    - "A quantidade de tinta (l) faz sentido para a metragem de parede?"
    - "Não existem quantidades negativas ou zeradas?"

#### D. `validador_schema` (O Programador)
- **Função**: Validar integridade de dados e formato.
- **Testes**:
    - "O JSON é válido?"
    - "Todos os IDs obrigatórios estão presentes?"
    - "A estrutura `spaces -> services -> categories` está intacta?"
    - "Os tipos de dados (float, string) estão corretos?"

### 2. Rules (Regras Globais)
- `regras/imutabilidade_relacional.md`: Proíbe criação de novos UUIDs para insumos/serviços.
- `regras/proporcionalidade.md`: Define como recalcular quantidades baseadas em área.
- `regras/protecao_modelos.md`: **CRÍTICO**. O diretório `obra_ninja/json` é somente leitura (Read-Only). Jamais escrever nele.

### 3. Workflows (Fluxos)
- `workflow_geracao_projeto.md`:
    1.  **Minerar**: Carregar dados válidos.
    2.  **Gerar**: Criar n variações de um projeto base.
    3.  **Validar (Eng)**: Aprovar tecnicamente.
    4.  **Validar (Dev)**: Aprovar estruturalmente.
    5.  **Salvar**: Gravar na pasta de saída.

## 📋 Passo a Passo de Implementação

1.  **Setup**: Criar estrutura de pastas (`.agent/skills`, `.agent/rules`).
2.  **Implementação do Minerador**: Script que cria o dicionário de serviços e composições.
3.  **Implementação do Gerador**: Script que aceita parâmetros (ex: fator de escala 1.5x) e clona um JSON ajustando valores.
4.  **Implementação dos Validadores**: Scripts de teste com asserções lógicas.
5.  **Integração**: Workflow que une as pontas.

## ✅ Critérios de Aceite
- [ ] O novo JSON deve ser importável no sistema SQL sem erros de Foreign Key (IDs inexistentes).
- [ ] O cálculo de material deve variar linearmente com a área (Se a área dobra, o piso dobra).

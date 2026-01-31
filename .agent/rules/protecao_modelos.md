# Regra: Proteção dos Modelos (Read-Only)

**Diretório Protegido**: `obra_ninja/json/`

**Descrição**:
Este diretório contém os "Gabariotos Mestre" (Golden Records) do sistema. Eles servem como a única fonte da verdade para a estrutura relacional e IDs válidos.

**Restrições Estritas**:
1.  **PROIBIDO ESCREVER**: O Agente NUNCA deve criar, modificar ou salvar arquivos dentro desta pasta.
2.  **PROIBIDO DELETAR**: O Agente NUNCA deve remover arquivos desta pasta.
3.  **SOMENTE LEITURA**: Scripts de mineração (`minerador_relacional`) e geração (`gerador_json`) devem tratar este caminho como *Source* (Origem) apenas.
4.  **SAÍDAS**: Qualquer novo arquivo gerado deve ser salvo exclusivamente em `.agent/output/` ou outras pastas designadas, JAMAIS misturado com os modelos originais.

**Motivo**: A integridade do banco de dados SQL depende da estabilidade destes arquivos. Alterá-los acidentalmente pode corromper a referência para gerações futuras.

# Regra: Uso de Python Obrigatório

## Descrição
Todos os scripts de processamento de dados, cálculos e conversões devem ser escritos em **Python 3.10+**.

## Padrões Obrigatórios

### Versão e Encoding
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

### Estrutura de Script
```python
"""
Módulo: nome_do_modulo.py
Descrição: [Descrição breve]
Versão: 1.0
"""

import ...

def main():
    ...

if __name__ == "__main__":
    main()
```

### Bibliotecas Permitidas
- **Dados**: `csv`, `json`, `pandas` (quando necessário)
- **Cálculos**: `math`, `decimal`
- **Datas**: `datetime`
- **Arquivos**: `os`, `pathlib`
- **UUIDs**: `uuid`
- **Validação**: `jsonschema` (para validação de JSON)

### Convenções de Código
- **Variáveis**: `snake_case`
- **Funções**: `snake_case`
- **Classes**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Docstrings**: Google Style

### Tratamento de Erros
```python
try:
    # operação
except SpecificError as e:
    print(f"Erro específico: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Justificativa
- Consistência entre todos os módulos
- Facilidade de manutenção
- Comunidade ativa e documentação abundante
- Integração nativa com ferramentas de dados

## Aplicação
Todos os arquivos em `scripts/` devem seguir estas regras.

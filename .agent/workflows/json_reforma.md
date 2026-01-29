---
description: Workflow para criar um JSON de reforma válido no padrão Obra Ninja
---

# Workflow: JSON Reforma

## Objetivo
Gerar um arquivo JSON válido seguindo o padrão Obra Ninja a partir de um escopo de reforma.

## Pré-requisitos
- Dados do imóvel (tipo, área, acabamento)
- Escopo de reforma definido (ambientes e serviços)
- Acesso às listas de materiais e ambientes válidos

## Passos

### 1. Validar Entrada
```python
# Verificar se o tipo de imóvel está na lista válida
tipos_validos = ["apto", "casa", "escritório", "loja", "clínica", "restaurante"]
```

### 2. Executar Skill: Quantificar Reforma
// turbo
```bash
python .agent/skills/quantificar_reforma/scripts/quantificar.py --input dados_imovel.json --output quantidades.csv
```

### 3. Executar Skill: Escopo Reforma  
// turbo
```bash
python .agent/skills/escopo_reforma/scripts/gerar_escopo.py --input quantidades.csv --output escopo.csv
```

### 4. Executar Skill: Custo Reforma
// turbo
```bash
python .agent/skills/custo_reforma/scripts/custear_reforma.py --input escopo.csv --sinapi sinapi_2025.csv --output escopo_custeado.csv
```

### 5. Executar Skill: Escopo JSON
// turbo
```bash
python .agent/skills/escopo_json/scripts/converte_escopo_to_obra_ninja_json.py --input escopo_custeado.csv --output projeto.json
```

### 6. Validar JSON
// turbo
```bash
python .agent/skills/escopo_json/scripts/validar_json.py --input projeto.json --schema obra_ninja_schema.json
```

### 7. Retornar Resultado
- Se válido: retornar caminho do JSON
- Se inválido: retornar lista de erros

## Saída Esperada
```json
{
  "status": "success",
  "file": "projeto.json",
  "validation": {
    "is_valid": true,
    "errors": []
  }
}
```

## Tratamento de Erros
| Erro | Ação |
|------|------|
| Ambiente não encontrado | Sugerir ambiente similar |
| Material não encontrado | Usar material genérico |
| Área inválida | Solicitar correção |

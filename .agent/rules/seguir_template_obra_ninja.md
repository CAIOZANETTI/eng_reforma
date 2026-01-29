---
trigger: always_on
---

# Regra: Seguir Template Obra Ninja

## Descrição
Todos os JSONs gerados devem seguir estritamente o schema **Obra Ninja V1**. Materiais e ambientes devem estar na lista de IDs aprovados.

## Schema Obrigatório

### Estrutura Raiz
```json
{
  "version": "1.0",
  "exportedAt": "ISO8601 timestamp",
  "template": { ... },
  "project": { ... },
  "spaces": [ ... ]
}
```

### Template
```json
{
  "title": "string",
  "description": "string",
  "language_code": "pt-BR",
  "property_type": "apartamento|casa|escritório|loja|clínica|restaurante",
  "status": "ready|draft"
}
```

### Project
```json
{
  "name": "string",
  "total_area": number
}
```

### Space
```json
{
  "space_id": "UUID",
  "_name": "string (deve estar em lista_ambientes.csv)",
  "area": number,
  "height": number (default 2.6),
  "services": [ ... ]
}
```

### Service
```json
{
  "service_id": "slug",
  "_name": "string",
  "quantity": number,
  "material_categories": [ ... ],
  "labor_categories": [ ... ]
}
```

### Material Category
```json
{
  "material_category_id": "slug",
  "_name": "string",
  "base_qtd": number,
  "base_unit": "m²|m|un|l|kg|vb|h",
  "materials": [
    {
      "material_id": "UUID ou ID da lista",
      "_name": "string (deve estar em lista_materiais.csv)"
    }
  ]
}
```

## Listas de Referência

### Ambientes Válidos (`ambientes-29012026.csv`)
### Materiais Válidos (`materials-29012026.csv`)

### Unidades Válidas
| Código | Descrição |
|--------|-----------|
| m² | Metro quadrado |
| m | Metro linear |
| un | Unidade |
| l | Litro |
| kg | Quilograma |
| vb | Verba |
| h | Hora |

## Validação Obrigatória
Antes de exportar qualquer JSON:
1. Validar contra `obra_ninja_schema.json`
2. Verificar se todos os `_name` de spaces estão em `lista_ambientes.csv`
3. Verificar se todos os `_name` de materials estão em `lista_materiais.csv`
4. Garantir que `total_area` = soma das áreas dos spaces

## Consequências de Violação
- JSON inválido será rejeitado
- Log de erro detalhado
- Sugestão de correção automática quando possível

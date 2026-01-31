---
name: Minerar Dados
description: Extrair bases de conhecimento (CSV) a partir de arquivos JSON de projetos existentes
version: 1.0
dependencies: []
---

# Skill: Minerar Dados

## Objetivo
Analisar arquivos JSON de projetos (formato Obra Ninja) e extrair catálogos consolidados de materiais, mão de obra, categorias e serviços. Isso permite criar uma "memória" do sistema baseada em projetos anteriores.

## Entradas
- Diretório contendo arquivos JSON válidos

## Saídas
- `materials.csv`: Catálogo de materiais encontrados
- `labor.csv`: Catálogo de mão de obra encontrada
- `categories.csv`: Categorias de insumos
- `services.csv`: Lista de serviços
- `compositions.csv`: Composição detalhada dos serviços (quais insumos compõem cada serviço)

## Scripts Disponíveis

### `scripts/extrair_catalogos.py`
Varre os JSONs e cria os arquivos de catálogo básico (materiais, mão de obra, categorias).

```bash
python extrair_catalogos.py --input_dir ../../input_json --output_dir ../../../knowledge_base
```

### `scripts/extrair_servicos.py`
Varre os JSONs e cria a base de serviços e suas composições.

```bash
python extrair_servicos.py --input_dir ../../input_json --output_dir ../../../knowledge_base
```

## Uso no Pipeline
Este skill é geralmente executado periodicamente ou sob demanda para atualizar a base de conhecimento do sistema, que será usada posteriormente pelos skills de `projetar` e `detalhar`.

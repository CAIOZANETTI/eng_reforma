#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: validar_json.py
Descrição: Valida JSONs contra o schema Obra Ninja
Versão: 1.0
"""

import json
import csv
import argparse
import os
import uuid
from pathlib import Path
from datetime import datetime

# Diretório base
SCRIPT_DIR = Path(__file__).parent.parent
AMBIENTES_CSV = SCRIPT_DIR / "resources" / "lista_ambientes.csv"
MATERIAIS_CSV = SCRIPT_DIR / "resources" / "lista_materiais.csv"


def carregar_lista_valida(filepath):
    """Carrega lista de nomes válidos de um CSV."""
    nomes = set()
    if not os.path.exists(filepath):
        return nomes
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = row.get("nome", "").strip()
            if nome:
                nomes.add(nome.lower())
    return nomes


def validar_uuid(valor):
    """Verifica se é um UUID válido."""
    try:
        uuid.UUID(valor)
        return True
    except:
        return False


def validar_estrutura_raiz(data):
    """Valida campos obrigatórios na raiz."""
    erros = []
    warnings = []
    
    campos_obrigatorios = ["version", "template", "project", "spaces"]
    for campo in campos_obrigatorios:
        if campo not in data:
            erros.append(f"Campo obrigatório ausente: {campo}")
    
    if "version" in data and data["version"] != "1.0":
        warnings.append(f"Versão diferente de 1.0: {data['version']}")
    
    if "exportedAt" in data:
        try:
            # Tentar parsear data ISO
            datetime.fromisoformat(data["exportedAt"].replace("Z", "+00:00"))
        except:
            warnings.append(f"Data de exportação em formato inválido: {data['exportedAt']}")
    
    return erros, warnings


def validar_template(template):
    """Valida seção template."""
    erros = []
    warnings = []
    
    if not template:
        erros.append("Template ausente ou vazio")
        return erros, warnings
    
    campos = ["title", "language_code", "property_type", "status"]
    for campo in campos:
        if campo not in template:
            erros.append(f"Campo template.{campo} ausente")
    
    property_types_validos = ["apto", "casa", "escritório", "escritorio", "loja", "clínica", "clinica", "restaurante"]
    if "property_type" in template:
        if template["property_type"].lower() not in property_types_validos:
            warnings.append(f"Tipo de imóvel não reconhecido: {template['property_type']}")
    
    status_validos = ["ready", "draft"]
    if "status" in template:
        if template["status"] not in status_validos:
            erros.append(f"Status inválido: {template['status']} (esperado: ready ou draft)")
    
    return erros, warnings


def validar_project(project):
    """Valida seção project."""
    erros = []
    warnings = []
    
    if not project:
        erros.append("Project ausente ou vazio")
        return erros, warnings
    
    if "name" not in project:
        erros.append("Nome do projeto ausente")
    
    if "total_area" not in project:
        erros.append("Área total do projeto ausente")
    elif not isinstance(project["total_area"], (int, float)):
        erros.append("Área total deve ser numérica")
    elif project["total_area"] <= 0:
        warnings.append("Área total é zero ou negativa")
    
    return erros, warnings


def validar_spaces(spaces, ambientes_validos):
    """Valida seção spaces."""
    erros = []
    warnings = []
    
    if not spaces:
        erros.append("Nenhum space definido")
        return erros, warnings
    
    if not isinstance(spaces, list):
        erros.append("Spaces deve ser uma lista")
        return erros, warnings
    
    soma_areas = 0
    
    for i, space in enumerate(spaces):
        prefix = f"spaces[{i}]"
        
        # Validar space_id
        if "space_id" not in space:
            erros.append(f"{prefix}: space_id ausente")
        elif not validar_uuid(space["space_id"]):
            warnings.append(f"{prefix}: space_id não é UUID válido")
        
        # Validar _name
        if "_name" not in space:
            erros.append(f"{prefix}: _name ausente")
        else:
            nome = space["_name"].lower()
            if ambientes_validos and nome not in ambientes_validos:
                warnings.append(f"{prefix}: ambiente '{space['_name']}' não está na lista de ambientes válidos")
        
        # Validar area
        if "area" not in space:
            erros.append(f"{prefix}: area ausente")
        elif not isinstance(space["area"], (int, float)):
            erros.append(f"{prefix}: area deve ser numérica")
        else:
            soma_areas += space["area"]
        
        # Validar services
        if "services" not in space:
            warnings.append(f"{prefix}: services ausente (vazio é permitido)")
        elif space["services"]:
            serv_erros, serv_warnings = validar_services(space["services"], prefix)
            erros.extend(serv_erros)
            warnings.extend(serv_warnings)
    
    return erros, warnings


def validar_services(services, prefix):
    """Valida lista de services."""
    erros = []
    warnings = []
    
    if not isinstance(services, list):
        erros.append(f"{prefix}.services deve ser uma lista")
        return erros, warnings
    
    for j, service in enumerate(services):
        svc_prefix = f"{prefix}.services[{j}]"
        
        if "service_id" not in service:
            erros.append(f"{svc_prefix}: service_id ausente")
        
        if "_name" not in service:
            erros.append(f"{svc_prefix}: _name ausente")
        
        if "quantity" not in service:
            warnings.append(f"{svc_prefix}: quantity ausente")
        elif not isinstance(service["quantity"], (int, float)):
            erros.append(f"{svc_prefix}: quantity deve ser numérica")
    
    return erros, warnings


def validar_json(data, ambientes_csv=None, materiais_csv=None):
    """
    Valida um JSON completo contra o schema Obra Ninja.
    
    Args:
        data: dict com o JSON parseado
        ambientes_csv: path para lista de ambientes válidos
        materiais_csv: path para lista de materiais válidos
    
    Returns:
        dict com is_valid, errors e warnings
    """
    todos_erros = []
    todos_warnings = []
    
    # Carregar listas de validação
    ambientes_validos = set()
    if ambientes_csv and os.path.exists(ambientes_csv):
        ambientes_validos = carregar_lista_valida(ambientes_csv)
    
    # Validar estrutura raiz
    erros, warnings = validar_estrutura_raiz(data)
    todos_erros.extend(erros)
    todos_warnings.extend(warnings)
    
    # Validar template
    erros, warnings = validar_template(data.get("template", {}))
    todos_erros.extend(erros)
    todos_warnings.extend(warnings)
    
    # Validar project
    erros, warnings = validar_project(data.get("project", {}))
    todos_erros.extend(erros)
    todos_warnings.extend(warnings)
    
    # Validar spaces
    erros, warnings = validar_spaces(data.get("spaces", []), ambientes_validos)
    todos_erros.extend(erros)
    todos_warnings.extend(warnings)
    
    return {
        "is_valid": len(todos_erros) == 0,
        "errors": todos_erros,
        "warnings": todos_warnings,
        "total_errors": len(todos_erros),
        "total_warnings": len(todos_warnings),
    }


def validar_arquivo(filepath, ambientes_csv=None, materiais_csv=None):
    """Valida um arquivo JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return {
            "is_valid": False,
            "errors": [f"JSON inválido: {str(e)}"],
            "warnings": [],
            "total_errors": 1,
            "total_warnings": 0,
        }
    except Exception as e:
        return {
            "is_valid": False,
            "errors": [f"Erro ao ler arquivo: {str(e)}"],
            "warnings": [],
            "total_errors": 1,
            "total_warnings": 0,
        }
    
    return validar_json(data, ambientes_csv, materiais_csv)


def validar_lote(diretorio, ambientes_csv=None, materiais_csv=None):
    """Valida todos os JSONs em um diretório."""
    resultados = []
    total_validos = 0
    total_invalidos = 0
    
    for filename in os.listdir(diretorio):
        if filename.endswith('.json'):
            filepath = os.path.join(diretorio, filename)
            resultado = validar_arquivo(filepath, ambientes_csv, materiais_csv)
            resultado["arquivo"] = filename
            resultados.append(resultado)
            
            if resultado["is_valid"]:
                total_validos += 1
            else:
                total_invalidos += 1
    
    return {
        "total_arquivos": len(resultados),
        "validos": total_validos,
        "invalidos": total_invalidos,
        "detalhes": resultados,
    }


def main():
    parser = argparse.ArgumentParser(description="Validar JSON Obra Ninja")
    parser.add_argument("--input", type=str, help="Arquivo JSON para validar")
    parser.add_argument("--dir", type=str, help="Diretório com JSONs para validar em lote")
    parser.add_argument("--ambientes", type=str, default=str(AMBIENTES_CSV), 
                        help="CSV com lista de ambientes válidos")
    parser.add_argument("--materiais", type=str, default=str(MATERIAIS_CSV),
                        help="CSV com lista de materiais válidos")
    parser.add_argument("--output", type=str, help="Arquivo JSON de saída com resultados")
    
    args = parser.parse_args()
    
    if args.input:
        # Validar arquivo único
        resultado = validar_arquivo(args.input, args.ambientes, args.materiais)
        
        print(f"\nValidação de: {args.input}")
        print(f"Válido: {'✅ SIM' if resultado['is_valid'] else '❌ NÃO'}")
        print(f"Erros: {resultado['total_errors']}")
        print(f"Avisos: {resultado['total_warnings']}")
        
        if resultado['errors']:
            print("\n❌ ERROS:")
            for erro in resultado['errors']:
                print(f"  - {erro}")
        
        if resultado['warnings']:
            print("\n⚠️ AVISOS:")
            for aviso in resultado['warnings']:
                print(f"  - {aviso}")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    elif args.dir:
        # Validar lote
        resultado = validar_lote(args.dir, args.ambientes, args.materiais)
        
        print(f"\nValidação em lote: {args.dir}")
        print(f"Total de arquivos: {resultado['total_arquivos']}")
        print(f"✅ Válidos: {resultado['validos']}")
        print(f"❌ Inválidos: {resultado['invalidos']}")
        
        # Mostrar arquivos inválidos
        invalidos = [r for r in resultado['detalhes'] if not r['is_valid']]
        if invalidos:
            print("\n❌ Arquivos com erros:")
            for inv in invalidos[:10]:  # Mostrar primeiros 10
                print(f"  - {inv['arquivo']}: {inv['total_errors']} erros")
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
    
    else:
        print("Uso:")
        print("  python validar_json.py --input projeto.json")
        print("  python validar_json.py --dir ranking_test_ott/")
        print("  python validar_json.py --input projeto.json --output resultado.json")


if __name__ == "__main__":
    main()

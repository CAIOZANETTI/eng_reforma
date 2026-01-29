#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: gerar_escopo.py
Descrição: Gera escopo detalhado de reforma baseado nas quantidades calculadas
Versão: 1.0
"""

import json
import csv
import argparse
import os

# Templates de serviços por tipo de reforma
TEMPLATES_REFORMA = {
    "banheiro_basico": {
        "nome": "Reforma Básica de Banheiro",
        "servicos": [
            {"servico": "Pintura de azulejos", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Troca de louças", "formula": "fixo", "unidade": "vb", "quantidade": 1},
            {"servico": "Troca de metais", "formula": "fixo", "unidade": "vb", "quantidade": 1},
            {"servico": "Pintura de teto", "formula": "area_teto", "unidade": "m²", "fator": 1.0},
        ]
    },
    "banheiro_completo": {
        "nome": "Reforma Completa de Banheiro",
        "servicos": [
            {"servico": "Demolição de revestimentos", "formula": "area_piso + area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Impermeabilização", "formula": "area_piso", "unidade": "m²", "fator": 1.3},
            {"servico": "Contrapiso", "formula": "area_piso", "unidade": "m²", "fator": 1.0},
            {"servico": "Revestimento piso", "formula": "area_piso", "unidade": "m²", "fator": 1.1},
            {"servico": "Revestimento parede", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.1},
            {"servico": "Rejunte", "formula": "area_piso + area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Vaso sanitário", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Cuba", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Torneira", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Chuveiro/Ducha", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Box de vidro", "formula": "fixo", "unidade": "m²", "quantidade": 2.5},
            {"servico": "Pintura de teto", "formula": "area_teto", "unidade": "m²", "fator": 1.0},
        ]
    },
    "banheiro_luxo": {
        "nome": "Reforma Premium de Banheiro",
        "servicos": [
            {"servico": "Demolição de revestimentos", "formula": "area_piso + area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Impermeabilização premium", "formula": "area_piso", "unidade": "m²", "fator": 1.5},
            {"servico": "Contrapiso com caimento", "formula": "area_piso", "unidade": "m²", "fator": 1.0},
            {"servico": "Porcelanato grande formato piso", "formula": "area_piso", "unidade": "m²", "fator": 1.15},
            {"servico": "Porcelanato grande formato parede", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.15},
            {"servico": "Rejunte epóxi", "formula": "area_piso + area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Vaso sanitário design", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Cuba esculpida", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Torneira de design", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Ducha com cromoterapia", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Ducha higiênica", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Box vidro 10mm até teto", "formula": "fixo", "unidade": "m²", "quantidade": 4.0},
            {"servico": "Nicho iluminado", "formula": "fixo", "unidade": "un", "quantidade": 2},
            {"servico": "Forro de gesso", "formula": "area_teto", "unidade": "m²", "fator": 1.0},
            {"servico": "Iluminação LED", "formula": "fixo", "unidade": "un", "quantidade": 4},
        ]
    },
    "cozinha_basica": {
        "nome": "Reforma Básica de Cozinha",
        "servicos": [
            {"servico": "Pintura lavável", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Revestimento área molhada", "formula": "area_parede_liquida * 0.4", "unidade": "m²", "fator": 1.1},
            {"servico": "Bancada granito", "formula": "perimetro * 0.3", "unidade": "m", "fator": 1.0},
            {"servico": "Cuba inox", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Torneira", "formula": "fixo", "unidade": "un", "quantidade": 1},
        ]
    },
    "cozinha_completa": {
        "nome": "Reforma Completa de Cozinha",
        "servicos": [
            {"servico": "Demolição de revestimentos", "formula": "area_piso + area_parede_liquida * 0.5", "unidade": "m²", "fator": 1.0},
            {"servico": "Contrapiso", "formula": "area_piso", "unidade": "m²", "fator": 1.0},
            {"servico": "Revestimento piso", "formula": "area_piso", "unidade": "m²", "fator": 1.1},
            {"servico": "Revestimento parede", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.1},
            {"servico": "Rejunte", "formula": "area_piso + area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Bancada quartzo", "formula": "perimetro * 0.4", "unidade": "m", "fator": 1.0},
            {"servico": "Cuba dupla", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Torneira gourmet", "formula": "fixo", "unidade": "un", "quantidade": 1},
            {"servico": "Marcenaria sob medida", "formula": "perimetro * 0.6", "unidade": "m", "fator": 1.0},
            {"servico": "Iluminação de bancada", "formula": "perimetro * 0.4", "unidade": "m", "fator": 1.0},
        ]
    },
    "sala_pintura": {
        "nome": "Pintura de Sala",
        "servicos": [
            {"servico": "Massa corrida", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Pintura parede", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Pintura teto", "formula": "area_teto", "unidade": "m²", "fator": 1.0},
        ]
    },
    "sala_completa": {
        "nome": "Reforma Completa de Sala",
        "servicos": [
            {"servico": "Demolição de piso", "formula": "area_piso", "unidade": "m²", "fator": 1.0},
            {"servico": "Contrapiso", "formula": "area_piso", "unidade": "m²", "fator": 1.0},
            {"servico": "Revestimento piso", "formula": "area_piso", "unidade": "m²", "fator": 1.1},
            {"servico": "Rodapé", "formula": "perimetro", "unidade": "m", "fator": 1.05},
            {"servico": "Massa corrida", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Pintura parede", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Forro de gesso", "formula": "area_teto", "unidade": "m²", "fator": 1.0},
            {"servico": "Iluminação LED", "formula": "area_teto * 0.2", "unidade": "un", "fator": 1.0},
        ]
    },
    "quarto_basico": {
        "nome": "Reforma Básica de Quarto",
        "servicos": [
            {"servico": "Pintura parede", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Pintura teto", "formula": "area_teto", "unidade": "m²", "fator": 1.0},
            {"servico": "Piso vinílico sobreposto", "formula": "area_piso", "unidade": "m²", "fator": 1.1},
            {"servico": "Rodapé", "formula": "perimetro", "unidade": "m", "fator": 1.05},
        ]
    },
    "quarto_completo": {
        "nome": "Reforma Completa de Quarto",
        "servicos": [
            {"servico": "Demolição de piso", "formula": "area_piso", "unidade": "m²", "fator": 1.0},
            {"servico": "Contrapiso", "formula": "area_piso", "unidade": "m²", "fator": 1.0},
            {"servico": "Piso laminado", "formula": "area_piso", "unidade": "m²", "fator": 1.1},
            {"servico": "Rodapé MDF", "formula": "perimetro", "unidade": "m", "fator": 1.05},
            {"servico": "Massa corrida", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Pintura parede", "formula": "area_parede_liquida", "unidade": "m²", "fator": 1.0},
            {"servico": "Forro de gesso", "formula": "area_teto", "unidade": "m²", "fator": 1.0},
            {"servico": "Iluminação", "formula": "fixo", "unidade": "un", "quantidade": 4},
        ]
    },
    "geral_pintura": {
        "nome": "Pintura Geral",
        "servicos": [
            {"servico": "Preparo de superfície", "formula": "area_parede_liquida + area_teto", "unidade": "m²", "fator": 1.0},
            {"servico": "Massa corrida", "formula": "area_parede_liquida + area_teto", "unidade": "m²", "fator": 1.0},
            {"servico": "Selador", "formula": "area_parede_liquida + area_teto", "unidade": "m²", "fator": 1.0},
            {"servico": "Pintura 2 demãos", "formula": "area_parede_liquida + area_teto", "unidade": "m²", "fator": 1.0},
        ]
    },
}

# Mapeamento de ambiente + acabamento para template
MAPEAMENTO_TEMPLATE = {
    ("Banheiro", "Popular"): "banheiro_basico",
    ("Banheiro", "Médio"): "banheiro_completo",
    ("Banheiro", "Luxo"): "banheiro_luxo",
    ("Banheiro social", "Popular"): "banheiro_basico",
    ("Banheiro social", "Médio"): "banheiro_completo",
    ("Banheiro social", "Luxo"): "banheiro_luxo",
    ("Lavabo", "Luxo"): "banheiro_luxo",
    ("Cozinha", "Popular"): "cozinha_basica",
    ("Cozinha", "Médio"): "cozinha_completa",
    ("Cozinha", "Luxo"): "cozinha_completa",
    ("Sala", "Popular"): "sala_pintura",
    ("Sala", "Médio"): "sala_completa",
    ("Sala", "Luxo"): "sala_completa",
    ("Quarto", "Popular"): "quarto_basico",
    ("Quarto", "Médio"): "quarto_completo",
    ("Quarto", "Luxo"): "quarto_completo",
}


def avaliar_formula(formula, quantidades):
    """
    Avalia uma fórmula usando as quantidades disponíveis.
    
    Args:
        formula: string com a fórmula (ex: "area_piso + area_parede_liquida")
        quantidades: dict com os valores disponíveis
    
    Returns:
        float com o resultado
    """
    if formula == "fixo":
        return None
    
    # Substituir variáveis pelos valores
    expr = formula
    for key, value in quantidades.items():
        if isinstance(value, (int, float)):
            expr = expr.replace(key, str(value))
    
    try:
        resultado = eval(expr)
        return round(resultado, 2)
    except:
        return 0.0


def gerar_escopo_ambiente(ambiente, quantidades, acabamento="Médio"):
    """
    Gera escopo de serviços para um ambiente.
    
    Args:
        ambiente: Nome do ambiente
        quantidades: dict com quantidades calculadas
        acabamento: Padrão de acabamento (Popular, Médio, Luxo)
    
    Returns:
        list de dicts com serviços e quantidades
    """
    # Encontrar template adequado
    template_key = MAPEAMENTO_TEMPLATE.get((ambiente, acabamento))
    
    # Fallback para template genérico
    if not template_key:
        # Tentar sem acabamento específico
        for (amb, acab), key in MAPEAMENTO_TEMPLATE.items():
            if amb.lower() in ambiente.lower():
                template_key = key
                break
    
    if not template_key:
        template_key = "geral_pintura"
    
    template = TEMPLATES_REFORMA.get(template_key, TEMPLATES_REFORMA["geral_pintura"])
    
    escopo = []
    item = 1
    
    for servico in template["servicos"]:
        if servico["formula"] == "fixo":
            quantidade = servico["quantidade"]
        else:
            quantidade = avaliar_formula(servico["formula"], quantidades)
            if quantidade and "fator" in servico:
                quantidade = round(quantidade * servico["fator"], 2)
        
        escopo.append({
            "item": item,
            "ambiente": ambiente,
            "servico": servico["servico"],
            "descricao": f"{servico['servico']} - {ambiente}",
            "unidade": servico["unidade"],
            "quantidade": quantidade if quantidade else 0,
        })
        item += 1
    
    return escopo


def gerar_escopo_imovel(quantidades_csv, acabamento="Médio"):
    """
    Gera escopo completo para um imóvel a partir do CSV de quantidades.
    
    Args:
        quantidades_csv: path para arquivo CSV de quantidades
        acabamento: Padrão de acabamento
    
    Returns:
        list com todos os serviços
    """
    escopo_total = []
    item_global = 1
    
    with open(quantidades_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            ambiente = row["ambiente"]
            quantidades = {
                "area_piso": float(row.get("area_piso", 0)),
                "perimetro": float(row.get("perimetro", 0)),
                "area_parede_bruta": float(row.get("area_parede_bruta", 0)),
                "area_parede_liquida": float(row.get("area_parede_liquida", 0)),
                "area_teto": float(row.get("area_teto", 0)),
                "rodape": float(row.get("rodape", 0)),
            }
            
            escopo_ambiente = gerar_escopo_ambiente(ambiente, quantidades, acabamento)
            
            for item in escopo_ambiente:
                item["item"] = item_global
                escopo_total.append(item)
                item_global += 1
    
    return escopo_total


def exportar_escopo_csv(escopo, filepath):
    """Exporta escopo para CSV."""
    if not escopo:
        return
    
    fieldnames = ["item", "ambiente", "servico", "descricao", "unidade", "quantidade"]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(escopo)
    
    print(f"Escopo exportado: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Gerar escopo de reforma")
    parser.add_argument("--input", type=str, required=True, help="CSV de quantidades")
    parser.add_argument("--acabamento", type=str, default="Médio", 
                        choices=["Popular", "Médio", "Luxo"], help="Padrão de acabamento")
    parser.add_argument("--output", type=str, required=True, help="CSV de saída")
    
    args = parser.parse_args()
    
    escopo = gerar_escopo_imovel(args.input, args.acabamento)
    exportar_escopo_csv(escopo, args.output)
    
    print(f"Total de itens no escopo: {len(escopo)}")


if __name__ == "__main__":
    main()

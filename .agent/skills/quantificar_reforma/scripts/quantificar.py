#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: quantificar.py
Descrição: Calcula quantidades de serviços baseado na área e tipo do ambiente
Versão: 1.0
"""

import json
import csv
import math
import argparse
import os

# Constantes de dimensões padrão
DIMENSOES_ABERTURAS = {
    "porta_interna": {"largura": 0.80, "altura": 2.10, "area": 1.68},
    "porta_entrada": {"largura": 0.90, "altura": 2.10, "area": 1.89},
    "janela_quarto": {"largura": 1.20, "altura": 1.20, "area": 1.44},
    "janela_banheiro": {"largura": 0.60, "altura": 0.60, "area": 0.36},
    "janela_cozinha": {"largura": 1.00, "altura": 1.00, "area": 1.00},
    "janela_sala": {"largura": 1.50, "altura": 1.20, "area": 1.80},
}

# Configuração padrão de aberturas por ambiente
ABERTURAS_POR_AMBIENTE = {
    "Banheiro": {"portas": 1, "janelas": 1, "tipo_janela": "janela_banheiro"},
    "Banheiro social": {"portas": 1, "janelas": 1, "tipo_janela": "janela_banheiro"},
    "Lavabo": {"portas": 1, "janelas": 0, "tipo_janela": None},
    "Quarto": {"portas": 1, "janelas": 1, "tipo_janela": "janela_quarto"},
    "Quarto solteiro": {"portas": 1, "janelas": 1, "tipo_janela": "janela_quarto"},
    "Quarto hóspedes": {"portas": 1, "janelas": 1, "tipo_janela": "janela_quarto"},
    "Suíte": {"portas": 2, "janelas": 1, "tipo_janela": "janela_quarto"},
    "Suíte master": {"portas": 2, "janelas": 2, "tipo_janela": "janela_quarto"},
    "Cozinha": {"portas": 1, "janelas": 1, "tipo_janela": "janela_cozinha"},
    "Cozinha americana": {"portas": 0, "janelas": 1, "tipo_janela": "janela_cozinha"},
    "Sala": {"portas": 1, "janelas": 2, "tipo_janela": "janela_sala"},
    "Sala + cozinha integradas": {"portas": 1, "janelas": 2, "tipo_janela": "janela_sala"},
    "Lavanderia": {"portas": 1, "janelas": 1, "tipo_janela": "janela_cozinha"},
    "Varanda": {"portas": 1, "janelas": 0, "tipo_janela": None},
    "Varanda gourmet": {"portas": 1, "janelas": 0, "tipo_janela": None},
    "Home office": {"portas": 1, "janelas": 1, "tipo_janela": "janela_quarto"},
    "Área gourmet": {"portas": 1, "janelas": 0, "tipo_janela": None},
    "Garagem": {"portas": 1, "janelas": 0, "tipo_janela": None},
}

# Pé-direito padrão por tipo de imóvel
PE_DIREITO_PADRAO = {
    "apto": 2.6,
    "casa": 2.8,
    "escritório": 2.8,
    "loja": 3.0,
    "clínica": 2.8,
    "restaurante": 3.0,
}


def calcular_perimetro(area, proporcao=1.5):
    """
    Calcula o perímetro aproximado de um ambiente retangular.
    Assume proporção largura:comprimento = 1:proporcao (default 1:1.5)
    """
    # area = largura * comprimento
    # comprimento = largura * proporcao
    # area = largura * largura * proporcao
    # largura = sqrt(area / proporcao)
    largura = math.sqrt(area / proporcao)
    comprimento = largura * proporcao
    perimetro = 2 * (largura + comprimento)
    return round(perimetro, 2)


def calcular_area_parede_bruta(perimetro, pe_direito):
    """Calcula área bruta de parede (sem descontar aberturas)."""
    return round(perimetro * pe_direito, 2)


def obter_aberturas(ambiente):
    """Retorna configuração de aberturas para o ambiente."""
    config = ABERTURAS_POR_AMBIENTE.get(ambiente, {"portas": 1, "janelas": 1, "tipo_janela": "janela_quarto"})
    return config


def calcular_area_aberturas(ambiente):
    """Calcula área total de aberturas (portas + janelas)."""
    config = obter_aberturas(ambiente)
    
    area_portas = config["portas"] * DIMENSOES_ABERTURAS["porta_interna"]["area"]
    
    area_janelas = 0
    if config["tipo_janela"] and config["janelas"] > 0:
        area_janelas = config["janelas"] * DIMENSOES_ABERTURAS[config["tipo_janela"]]["area"]
    
    return {
        "n_portas": config["portas"],
        "area_portas": round(area_portas, 2),
        "n_janelas": config["janelas"],
        "area_janelas": round(area_janelas, 2),
        "area_total": round(area_portas + area_janelas, 2)
    }


def quantificar_ambiente(ambiente, area, pe_direito=None, tipo_imovel="apto"):
    """
    Quantifica todas as métricas de um ambiente.
    
    Args:
        ambiente: Nome do ambiente (ex: "Banheiro")
        area: Área do ambiente em m²
        pe_direito: Pé-direito em metros (opcional, usa padrão se não informado)
        tipo_imovel: Tipo do imóvel para determinar pé-direito padrão
    
    Returns:
        dict com todas as quantidades calculadas
    """
    if pe_direito is None:
        pe_direito = PE_DIREITO_PADRAO.get(tipo_imovel.lower(), 2.6)
    
    perimetro = calcular_perimetro(area)
    area_parede_bruta = calcular_area_parede_bruta(perimetro, pe_direito)
    aberturas = calcular_area_aberturas(ambiente)
    area_parede_liquida = round(area_parede_bruta - aberturas["area_total"], 2)
    
    return {
        "ambiente": ambiente,
        "area_piso": round(area, 2),
        "perimetro": perimetro,
        "pe_direito": pe_direito,
        "area_parede_bruta": area_parede_bruta,
        "aberturas": aberturas,
        "area_parede_liquida": max(0, area_parede_liquida),
        "area_teto": round(area, 2),
        "rodape": perimetro,  # Mesmo que perímetro, descontando portas depois
    }


def quantificar_imovel(dados_imovel):
    """
    Processa um imóvel completo com múltiplos ambientes.
    
    Args:
        dados_imovel: dict com estrutura:
            {
                "tipo": "apto",
                "area_total": 55,
                "pe_direito": 2.6,  # opcional
                "ambientes": [
                    {"nome": "Sala", "area": 18},
                    {"nome": "Quarto", "area": 12},
                    ...
                ]
            }
    
    Returns:
        list de dicts com quantidades por ambiente
    """
    tipo = dados_imovel.get("tipo", "apto")
    pe_direito_geral = dados_imovel.get("pe_direito")
    
    resultados = []
    for amb in dados_imovel.get("ambientes", []):
        nome = amb.get("nome", "Ambiente")
        area = amb.get("area", 0)
        pe_direito = amb.get("pe_direito", pe_direito_geral)
        
        resultado = quantificar_ambiente(nome, area, pe_direito, tipo)
        resultados.append(resultado)
    
    return resultados


def exportar_csv(resultados, filepath):
    """Exporta resultados para CSV."""
    if not resultados:
        return
    
    fieldnames = [
        "ambiente", "area_piso", "perimetro", "pe_direito",
        "area_parede_bruta", "area_parede_liquida", "area_teto",
        "n_portas", "area_portas", "n_janelas", "area_janelas", "rodape"
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for r in resultados:
            row = {
                "ambiente": r["ambiente"],
                "area_piso": r["area_piso"],
                "perimetro": r["perimetro"],
                "pe_direito": r["pe_direito"],
                "area_parede_bruta": r["area_parede_bruta"],
                "area_parede_liquida": r["area_parede_liquida"],
                "area_teto": r["area_teto"],
                "n_portas": r["aberturas"]["n_portas"],
                "area_portas": r["aberturas"]["area_portas"],
                "n_janelas": r["aberturas"]["n_janelas"],
                "area_janelas": r["aberturas"]["area_janelas"],
                "rodape": r["rodape"],
            }
            writer.writerow(row)
    
    print(f"Exportado: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Quantificar áreas de reforma")
    parser.add_argument("--ambiente", type=str, help="Nome do ambiente")
    parser.add_argument("--area", type=float, help="Área do ambiente em m²")
    parser.add_argument("--pe_direito", type=float, default=2.6, help="Pé-direito em metros")
    parser.add_argument("--tipo", type=str, default="apto", help="Tipo de imóvel")
    parser.add_argument("--input", type=str, help="Arquivo JSON de entrada com dados do imóvel")
    parser.add_argument("--output", type=str, help="Arquivo CSV de saída")
    
    args = parser.parse_args()
    
    if args.input:
        # Processar arquivo JSON
        with open(args.input, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        resultados = quantificar_imovel(dados)
        
        if args.output:
            exportar_csv(resultados, args.output)
        else:
            print(json.dumps(resultados, indent=2, ensure_ascii=False))
    
    elif args.ambiente and args.area:
        # Processar ambiente único
        resultado = quantificar_ambiente(
            args.ambiente,
            args.area,
            args.pe_direito,
            args.tipo
        )
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    
    else:
        # Exemplo de uso
        print("Exemplo de uso:")
        print("  python quantificar.py --ambiente Banheiro --area 5 --pe_direito 2.6")
        print("  python quantificar.py --input imovel.json --output quantidades.csv")
        print()
        
        # Demo
        exemplo = quantificar_ambiente("Banheiro", 5, 2.6, "apto")
        print("Exemplo - Banheiro 5m²:")
        print(json.dumps(exemplo, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

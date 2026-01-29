#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: gerar_ranking.py
Descrição: Gera ranking de reformas baseado em dados IBGE
Versão: 1.0
"""

import csv
import json
import argparse
import os
import random
from pathlib import Path
from datetime import datetime

# Diretório base
SCRIPT_DIR = Path(__file__).parent.parent

# Base de dados de reformas comuns
REFORMAS_BASE = [
    # Apartamentos
    {"tipo": "Apto", "ambiente": "Banheiro", "area_range": (3, 8), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Banheiro social", "area_range": (3, 6), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Lavabo", "area_range": (1.5, 4), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Cozinha", "area_range": (6, 16), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Cozinha americana", "area_range": (10, 25), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Sala", "area_range": (14, 35), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Sala + cozinha integradas", "area_range": (25, 50), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Quarto", "area_range": (8, 18), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Suíte", "area_range": (12, 25), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Quarto infantil", "area_range": (8, 14), "acabamentos": ["Popular", "Médio"]},
    {"tipo": "Apto", "ambiente": "Home office", "area_range": (6, 14), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Lavanderia", "area_range": (3, 8), "acabamentos": ["Popular", "Médio"]},
    {"tipo": "Apto", "ambiente": "Varanda", "area_range": (4, 12), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Varanda gourmet", "area_range": (8, 18), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Apto", "ambiente": "Geral", "area_range": (35, 120), "acabamentos": ["Popular", "Médio", "Luxo"]},
    
    # Casas
    {"tipo": "Casa", "ambiente": "Banheiro", "area_range": (4, 10), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Banheiro suíte", "area_range": (6, 15), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Lavabo", "area_range": (2, 5), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Cozinha", "area_range": (10, 30), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Sala", "area_range": (20, 60), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Living integrado", "area_range": (35, 80), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Quarto", "area_range": (12, 25), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Suíte master", "area_range": (18, 40), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Área gourmet", "area_range": (15, 40), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Varanda", "area_range": (8, 20), "acabamentos": ["Popular", "Médio"]},
    {"tipo": "Casa", "ambiente": "Lavanderia", "area_range": (6, 15), "acabamentos": ["Popular", "Médio"]},
    {"tipo": "Casa", "ambiente": "Garagem", "area_range": (20, 50), "acabamentos": ["Popular", "Médio"]},
    {"tipo": "Casa", "ambiente": "Quintal", "area_range": (30, 100), "acabamentos": ["Popular", "Médio"]},
    {"tipo": "Casa", "ambiente": "Fachada", "area_range": (40, 120), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Muros e portão", "area_range": (30, 80), "acabamentos": ["Popular", "Médio"]},
    {"tipo": "Casa", "ambiente": "Telhado", "area_range": (60, 200), "acabamentos": ["Popular", "Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Piscina", "area_range": (15, 50), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Edícula", "area_range": (15, 40), "acabamentos": ["Médio", "Luxo"]},
    {"tipo": "Casa", "ambiente": "Geral", "area_range": (80, 250), "acabamentos": ["Popular", "Médio", "Luxo"]},
    
    # Comercial
    {"tipo": "Escritório", "ambiente": "Recepção", "area_range": (15, 50), "acabamentos": ["Comercial"]},
    {"tipo": "Escritório", "ambiente": "Open space", "area_range": (60, 200), "acabamentos": ["Comercial"]},
    {"tipo": "Escritório", "ambiente": "Sala de reunião", "area_range": (15, 40), "acabamentos": ["Comercial"]},
    {"tipo": "Escritório", "ambiente": "Copa", "area_range": (10, 30), "acabamentos": ["Comercial"]},
    {"tipo": "Escritório", "ambiente": "Banheiros", "area_range": (8, 25), "acabamentos": ["Comercial"]},
    {"tipo": "Loja", "ambiente": "Salão de vendas", "area_range": (40, 150), "acabamentos": ["Comercial"]},
    {"tipo": "Loja", "ambiente": "Fachada comercial", "area_range": (15, 50), "acabamentos": ["Comercial"]},
    {"tipo": "Clínica", "ambiente": "Recepção", "area_range": (15, 35), "acabamentos": ["Comercial"]},
    {"tipo": "Clínica", "ambiente": "Consultório", "area_range": (10, 25), "acabamentos": ["Comercial"]},
    {"tipo": "Restaurante", "ambiente": "Salão", "area_range": (60, 150), "acabamentos": ["Comercial"]},
    {"tipo": "Restaurante", "ambiente": "Cozinha industrial", "area_range": (30, 80), "acabamentos": ["Comercial"]},
]

# Configurações de imóvel
CONFIG_IMOVEL = {
    "1Q+1B": {"area": 40, "peso": 15},
    "2Q+1B": {"area": 55, "peso": 30},
    "2Q+2B": {"area": 65, "peso": 20},
    "3Q+2B": {"area": 85, "peso": 25},
    "3Q+3B": {"area": 100, "peso": 5},
    "4Q+3B": {"area": 140, "peso": 3},
    "0Q+1B": {"area": 50, "peso": 2},  # Comercial
    "0Q+2B": {"area": 80, "peso": 2},  # Comercial
    "0Q+4B": {"area": 120, "peso": 1}, # Comercial grande
}

# Descrições base por tipo de reforma
DESCRICOES = {
    "Banheiro": {
        "Popular": "Reforma básica de banheiro: pintura de azulejos, troca de louças/metais econômicos, box acrílico",
        "Médio": "Reforma completa de banheiro: demolição, impermeabilização, porcelanato, louças/metais de qualidade, box vidro",
        "Luxo": "Banheiro premium: porcelanato grande formato, metais de design, box até o teto, nicho iluminado, ducha higiênica",
    },
    "Cozinha": {
        "Popular": "Cozinha funcional: pintura lavável, revestimento básico área molhada, bancada granito, cuba/torneira simples",
        "Médio": "Cozinha completa: piso/parede porcelanato, bancada quartzo, marcenaria sob medida, iluminação de bancada",
        "Luxo": "Cozinha gourmet: ilha central, bancada premium, marcenaria com ferragens Blum, eletros embutidos de alto padrão",
    },
    "Sala": {
        "Popular": "Sala renovada: pintura, piso vinílico, luminárias LED, organização de cabos",
        "Médio": "Sala moderna: piso laminado/porcelanato, forro com iluminação embutida, painel de TV, pintura de destaque",
        "Luxo": "Living premium: porcelanato grande formato, sanca, automação, lareira ecológica, marcenaria de TV premium",
    },
    "Quarto": {
        "Popular": "Quarto básico: pintura, piso vinílico sobreposto, rodapé, luminárias novas",
        "Médio": "Quarto completo: piso laminado, forro de gesso, iluminação setorizada, closet linear",
        "Luxo": "Suíte integrada: piso madeira, painel ripado, closet iluminado, automação de iluminação e cortinas",
    },
    "Geral": {
        "Popular": "Reforma rápida: pintura geral, troca de luminárias, revisão elétrica, pequenos reparos",
        "Médio": "Reforma completa: pintura, troca de pisos áreas sociais, reforma de banheiros, marcenaria de cozinha",
        "Luxo": "Retrofit completo: demolição, novo projeto de interiores, materiais premium, automação residencial",
    },
}


def gerar_descricao(tipo, ambiente, acabamento):
    """Gera descrição para uma reforma."""
    # Tentar descrição específica
    if ambiente in DESCRICOES and acabamento in DESCRICOES[ambiente]:
        return DESCRICOES[ambiente][acabamento]
    
    # Fallback para descrição genérica
    if "Geral" in DESCRICOES and acabamento in DESCRICOES["Geral"]:
        return DESCRICOES["Geral"][acabamento].replace("reforma", f"reforma de {ambiente.lower()}")
    
    return f"Reforma de {ambiente} padrão {acabamento.lower()}"


def selecionar_configuracao(tipo):
    """Seleciona configuração de imóvel baseado no tipo."""
    if tipo in ["Escritório", "Loja", "Clínica", "Restaurante"]:
        configs = ["0Q+1B", "0Q+2B", "0Q+4B"]
        pesos = [50, 35, 15]
    else:
        configs = ["1Q+1B", "2Q+1B", "2Q+2B", "3Q+2B", "3Q+3B", "4Q+3B"]
        pesos = [CONFIG_IMOVEL[c]["peso"] for c in configs]
    
    return random.choices(configs, weights=pesos, k=1)[0]


def gerar_ranking(quantidade, seed=None):
    """
    Gera ranking de reformas.
    
    Args:
        quantidade: número de itens no ranking
        seed: seed para reprodutibilidade
    
    Returns:
        list de dicts com dados de reforma
    """
    if seed:
        random.seed(seed)
    
    ranking = []
    id_counter = 1
    
    # Pesos de frequência por tipo de imóvel
    pesos_tipo = {
        "Apto": 45,
        "Casa": 40,
        "Escritório": 8,
        "Loja": 3,
        "Clínica": 2,
        "Restaurante": 2,
    }
    
    while len(ranking) < quantidade:
        # Selecionar tipo de reforma baseado em frequência
        reforma_base = random.choice(REFORMAS_BASE)
        tipo = reforma_base["tipo"]
        ambiente = reforma_base["ambiente"]
        
        # Ajustar probabilidade por peso do tipo
        if random.random() * 100 > pesos_tipo.get(tipo, 10):
            continue
        
        # Selecionar acabamento
        acabamento = random.choice(reforma_base["acabamentos"])
        
        # Gerar área
        area_min, area_max = reforma_base["area_range"]
        area = round(random.uniform(area_min, area_max), 0)
        
        # Selecionar configuração
        configuracao = selecionar_configuracao(tipo)
        
        # Gerar descrição
        descricao = gerar_descricao(tipo, ambiente, acabamento)
        
        item = {
            "id": id_counter,
            "tipo": tipo,
            "área (ambiente)": ambiente,
            "area_m2": area,
            "qtd_imovel (padrão 2Q+1B)": configuracao,
            "acabamento (popular / médio / luxo / comercial)": acabamento,
            "descrição da reforma (sem ampliação)": descricao,
        }
        
        ranking.append(item)
        id_counter += 1
    
    return ranking


def exportar_csv(ranking, filepath):
    """Exporta ranking para CSV."""
    if not ranking:
        return
    
    fieldnames = list(ranking[0].keys())
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ranking)
    
    print(f"Ranking exportado: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Gerar ranking de reformas IBGE")
    parser.add_argument("--quantidade", type=int, default=50, help="Quantidade de itens")
    parser.add_argument("--output", type=str, help="Arquivo CSV de saída")
    parser.add_argument("--seed", type=int, help="Seed para reprodutibilidade")
    
    args = parser.parse_args()
    
    ranking = gerar_ranking(args.quantidade, args.seed)
    
    if args.output:
        exportar_csv(ranking, args.output)
    else:
        # Output padrão
        output_dir = SCRIPT_DIR / "examples"
        os.makedirs(output_dir, exist_ok=True)
        filepath = output_dir / f"reforma_ibge_ranking_{args.quantidade}.csv"
        exportar_csv(ranking, filepath)
    
    print(f"Gerados {len(ranking)} itens no ranking")


if __name__ == "__main__":
    main()

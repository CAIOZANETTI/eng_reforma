#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: query_catalogo.py
Descrição: Busca combinações no catálogo de reformas
Versão: 1.0
"""

import csv
import json
import argparse
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
CATALOGO_DIR = SCRIPT_DIR / "catalogo"


def carregar_catalogo(filepath=None):
    """Carrega catálogo do CSV."""
    if filepath is None:
        # Usar o maior catálogo disponível
        for meta in [99, 95, 90, 80, 70]:
            path = CATALOGO_DIR / f"catalogo_{meta}pct.csv"
            if path.exists():
                filepath = path
                break
    
    if not filepath or not os.path.exists(filepath):
        return []
    
    catalogo = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            catalogo.append(row)
    
    return catalogo


def query(catalogo, tipo=None, ambiente=None, acabamento=None, 
          area_min=None, area_max=None, config=None, limit=10):
    """
    Busca no catálogo com filtros.
    
    Args:
        catalogo: Lista de combinações
        tipo: Filtro por tipo de imóvel
        ambiente: Filtro por ambiente (busca parcial)
        acabamento: Filtro por acabamento
        area_min: Área mínima
        area_max: Área máxima
        config: Configuração do imóvel
        limit: Limite de resultados
    
    Returns:
        list de combinações que atendem aos filtros
    """
    resultados = []
    
    for item in catalogo:
        # Filtrar por tipo
        if tipo and item.get("tipo", "").lower() != tipo.lower():
            continue
        
        # Filtrar por ambiente (busca parcial)
        if ambiente:
            item_ambiente = item.get("ambiente", "").lower()
            if ambiente.lower() not in item_ambiente:
                continue
        
        # Filtrar por acabamento
        if acabamento:
            item_acabamento = item.get("acabamento", "").lower()
            if acabamento.lower() not in item_acabamento:
                continue
        
        # Filtrar por área
        try:
            item_area = float(item.get("area_m2", 0))
        except:
            item_area = 0
        
        if area_min is not None and item_area < area_min:
            continue
        if area_max is not None and item_area > area_max:
            continue
        
        # Filtrar por configuração
        if config:
            item_config = item.get("configuracao", "")
            if config.upper() not in item_config.upper():
                continue
        
        resultados.append(item)
        
        if limit and len(resultados) >= limit:
            break
    
    return resultados


def buscar_similar(catalogo, tipo, ambiente, area, acabamento):
    """
    Busca a combinação mais similar aos parâmetros.
    
    Returns:
        A combinação mais próxima ou None
    """
    # Primeiro, buscar exata
    exatas = query(catalogo, tipo=tipo, ambiente=ambiente, 
                   acabamento=acabamento, limit=5)
    
    if exatas:
        # Encontrar a mais próxima em área
        melhor = None
        menor_diff = float('inf')
        
        for item in exatas:
            try:
                item_area = float(item.get("area_m2", 0))
                diff = abs(item_area - area)
                if diff < menor_diff:
                    menor_diff = diff
                    melhor = item
            except:
                pass
        
        return melhor
    
    # Fallback: buscar só por tipo e ambiente
    tipo_ambiente = query(catalogo, tipo=tipo, ambiente=ambiente, limit=10)
    
    if tipo_ambiente:
        # Retornar o primeiro
        return tipo_ambiente[0]
    
    # Fallback 2: só ambiente
    so_ambiente = query(catalogo, ambiente=ambiente, limit=5)
    
    if so_ambiente:
        return so_ambiente[0]
    
    return None


def estatisticas(catalogo):
    """Gera estatísticas do catálogo."""
    stats = {
        "total": len(catalogo),
        "por_tipo": {},
        "por_acabamento": {},
        "area_media": 0,
        "origens": {"base": 0, "expandido": 0}
    }
    
    soma_area = 0
    
    for item in catalogo:
        tipo = item.get("tipo", "Outro")
        acabamento = item.get("acabamento", "Outro")
        origem = item.get("origem", "base")
        
        stats["por_tipo"][tipo] = stats["por_tipo"].get(tipo, 0) + 1
        stats["por_acabamento"][acabamento] = stats["por_acabamento"].get(acabamento, 0) + 1
        
        if origem in stats["origens"]:
            stats["origens"][origem] += 1
        
        try:
            soma_area += float(item.get("area_m2", 0))
        except:
            pass
    
    if stats["total"] > 0:
        stats["area_media"] = round(soma_area / stats["total"], 1)
    
    return stats


def main():
    parser = argparse.ArgumentParser(description="Query no catálogo de reformas")
    parser.add_argument("--catalogo", type=str, help="Arquivo CSV do catálogo")
    parser.add_argument("--tipo", type=str, help="Filtro por tipo de imóvel")
    parser.add_argument("--ambiente", type=str, help="Filtro por ambiente")
    parser.add_argument("--acabamento", type=str, help="Filtro por acabamento")
    parser.add_argument("--area_min", type=float, help="Área mínima")
    parser.add_argument("--area_max", type=float, help="Área máxima")
    parser.add_argument("--config", type=str, help="Configuração (ex: 2Q+1B)")
    parser.add_argument("--limit", type=int, default=10, help="Limite de resultados")
    parser.add_argument("--stats", action="store_true", help="Mostrar estatísticas")
    parser.add_argument("--json", action="store_true", help="Output em JSON")
    
    args = parser.parse_args()
    
    # Carregar catálogo
    catalogo = carregar_catalogo(args.catalogo)
    
    if not catalogo:
        print("Catalogo vazio ou nao encontrado. Execute expandir_base.py primeiro.")
        return
    
    # Estatísticas
    if args.stats:
        stats = estatisticas(catalogo)
        if args.json:
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            print(f"\nEstatisticas do Catalogo:")
            print(f"Total: {stats['total']} combinacoes")
            print(f"Area media: {stats['area_media']} m2")
            print(f"\nPor tipo:")
            for tipo, qtd in sorted(stats['por_tipo'].items(), key=lambda x: -x[1]):
                print(f"  {tipo}: {qtd}")
            print(f"\nPor acabamento:")
            for acab, qtd in sorted(stats['por_acabamento'].items(), key=lambda x: -x[1]):
                print(f"  {acab}: {qtd}")
            print(f"\nOrigem:")
            for orig, qtd in stats['origens'].items():
                print(f"  {orig}: {qtd}")
        return
    
    # Query
    resultados = query(
        catalogo,
        tipo=args.tipo,
        ambiente=args.ambiente,
        acabamento=args.acabamento,
        area_min=args.area_min,
        area_max=args.area_max,
        config=args.config,
        limit=args.limit
    )
    
    if args.json:
        print(json.dumps(resultados, indent=2, ensure_ascii=False))
    else:
        print(f"\nEncontrados: {len(resultados)} resultados\n")
        
        for item in resultados:
            print(f"[{item.get('id', '?')}] {item.get('tipo')} | {item.get('ambiente')} | "
                  f"{item.get('area_m2')}m2 | {item.get('acabamento')} | {item.get('configuracao')}")


if __name__ == "__main__":
    main()

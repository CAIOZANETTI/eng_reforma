#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: expandir_base.py
Descrição: Expande a base curada de reformas aplicando variações
Versão: 1.0
"""

import csv
import json
import argparse
import os
from pathlib import Path
from copy import deepcopy

# Diretório base
SCRIPT_DIR = Path(__file__).parent.parent
RESOURCES_DIR = SCRIPT_DIR / "resources"
CATALOGO_DIR = SCRIPT_DIR / "catalogo"

# Carregar configurações
def carregar_faixas_area():
    """Carrega faixas de área do JSON."""
    filepath = RESOURCES_DIR / "faixas_area.json"
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def carregar_matriz_compatibilidade():
    """Carrega matriz de compatibilidade."""
    filepath = RESOURCES_DIR / "matriz_compatibilidade.csv"
    matriz = {}
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tipo = row["tipo"]
                ambiente = row["ambiente"]
                if tipo not in matriz:
                    matriz[tipo] = {}
                matriz[tipo][ambiente] = {
                    "valido": row["valido"] == "1",
                    "peso": int(row.get("peso_frequencia", 1))
                }
    return matriz

# Configurações de expansão
VARIANTES_ACABAMENTO = {
    "Popular": ["Popular"],
    "Médio": ["Popular", "Médio"],
    "Luxo": ["Médio", "Luxo"],
    "Comercial": ["Comercial"]
}

FAIXAS_AREA_RELATIVAS = {
    "pequeno": 0.7,
    "medio": 1.0,
    "grande": 1.4
}

CONFIGURACOES_IMOVEL = {
    "Apto": ["1Q+1B", "2Q+1B", "2Q+2B", "3Q+2B", "3Q+3B", "4Q+3B"],
    "Casa": ["1Q+1B", "2Q+1B", "2Q+2B", "3Q+2B", "3Q+3B", "4Q+3B"],
    "Escritório": ["0Q+1B", "0Q+2B", "0Q+4B"],
    "Loja": ["0Q+1B", "0Q+2B"],
    "Clínica": ["0Q+1B", "0Q+2B"],
    "Restaurante": ["0Q+2B", "0Q+4B"]
}


def validar_combinacao(tipo, ambiente, area, acabamento, faixas, matriz):
    """
    Valida se uma combinação é válida.
    
    Returns:
        (bool, str): (válido, motivo se inválido)
    """
    # Verificar matriz de compatibilidade
    if tipo in matriz:
        if ambiente not in matriz[tipo]:
            return False, f"Ambiente '{ambiente}' não válido para {tipo}"
        if not matriz[tipo][ambiente]["valido"]:
            return False, f"Combinação {tipo}/{ambiente} desabilitada"
    
    # Verificar faixa de área
    if ambiente in faixas:
        faixa = faixas[ambiente]
        if area < faixa["min"] * 0.5:  # Margem de tolerância
            return False, f"Área {area}m² menor que mínimo {faixa['min']}m²"
        if faixa["max"] > 0 and area > faixa["max"] * 1.5:
            return False, f"Área {area}m² maior que máximo {faixa['max']}m²"
    
    # Verificar acabamento comercial
    if tipo in ["Escritório", "Loja", "Clínica", "Restaurante"]:
        if acabamento != "Comercial":
            return False, f"Tipo {tipo} requer acabamento Comercial"
    elif acabamento == "Comercial":
        return False, f"Acabamento Comercial só para tipos comerciais"
    
    return True, ""


def gerar_variantes_area(area_base, ambiente, faixas):
    """Gera variantes de área para um ambiente."""
    variantes = []
    
    if ambiente in faixas:
        faixa = faixas[ambiente]
        area_min = faixa["min"]
        area_max = faixa["max"] if faixa["max"] > 0 else faixa["default"] * 2
        
        # Pequeno
        area_pequena = max(area_min, area_base * FAIXAS_AREA_RELATIVAS["pequeno"])
        variantes.append(round(area_pequena, 0))
        
        # Médio (original)
        variantes.append(round(area_base, 0))
        
        # Grande
        area_grande = min(area_max, area_base * FAIXAS_AREA_RELATIVAS["grande"])
        variantes.append(round(area_grande, 0))
    else:
        variantes = [round(area_base, 0)]
    
    return list(set(variantes))  # Remover duplicatas


def gerar_variantes_acabamento(acabamento_base):
    """Gera variantes de acabamento baseado no original."""
    return VARIANTES_ACABAMENTO.get(acabamento_base, [acabamento_base])


def gerar_variantes_config(tipo):
    """Retorna configurações válidas para um tipo de imóvel."""
    return CONFIGURACOES_IMOVEL.get(tipo, ["2Q+1B"])


def expandir_base(input_csv, meta=90, seed=None):
    """
    Expande a base curada aplicando variações.
    
    Args:
        input_csv: Path do CSV base
        meta: Meta de cobertura (70, 80, 90, 95, 99)
        seed: Seed para reprodutibilidade
    
    Returns:
        list de dicts com combinações expandidas
    """
    faixas = carregar_faixas_area()
    matriz = carregar_matriz_compatibilidade()
    
    # Carregar base
    base = []
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            base.append(row)
    
    print(f"Base carregada: {len(base)} combinações")
    
    # Definir multiplicadores por meta
    multiplicadores = {
        70: {"area": False, "acabamento": False, "config": False},
        80: {"area": True, "acabamento": False, "config": False},
        90: {"area": True, "acabamento": True, "config": False},
        95: {"area": True, "acabamento": True, "config": True},
        99: {"area": True, "acabamento": True, "config": True, "full": True},
    }
    
    config = multiplicadores.get(meta, multiplicadores[90])
    
    # Expandir
    expandido = []
    id_counter = 1
    
    for item in base:
        tipo = item.get("tipo", "Apto")
        ambiente = item.get("área (ambiente)", item.get("ambiente", "Geral"))
        area_base = float(item.get("area_m2", 30))
        acabamento_base = item.get("acabamento (popular / médio / luxo / comercial)", 
                                   item.get("acabamento", "Médio"))
        config_base = item.get("qtd_imovel (padrão 2Q+1B)", 
                               item.get("configuracao", "2Q+1B"))
        descricao = item.get("descrição da reforma (sem ampliação)", 
                            item.get("descricao", ""))
        
        # Normalizar acabamento
        acabamento_base = acabamento_base.split("/")[0].strip().title()
        if acabamento_base.lower() in ["popular", "médio", "medio", "luxo", "comercial"]:
            acabamento_base = acabamento_base.replace("Medio", "Médio")
        else:
            acabamento_base = "Médio"
        
        # Gerar variantes
        areas = gerar_variantes_area(area_base, ambiente, faixas) if config["area"] else [area_base]
        acabamentos = gerar_variantes_acabamento(acabamento_base) if config["acabamento"] else [acabamento_base]
        configs = gerar_variantes_config(tipo) if config.get("config") else [config_base]
        
        # Limitar configs para não explodir
        if not config.get("full"):
            configs = configs[:2]  # Top 2 configurações
        
        # Gerar combinações
        for area in areas:
            for acabamento in acabamentos:
                for cfg in configs:
                    # Validar
                    valido, motivo = validar_combinacao(
                        tipo, ambiente, area, acabamento, faixas, matriz
                    )
                    
                    if not valido:
                        continue
                    
                    nova_comb = {
                        "id": id_counter,
                        "tipo": tipo,
                        "ambiente": ambiente,
                        "area_m2": area,
                        "configuracao": cfg,
                        "acabamento": acabamento,
                        "descricao": descricao,
                        "origem": "expandido" if (area != area_base or 
                                                  acabamento != acabamento_base or 
                                                  cfg != config_base) else "base"
                    }
                    
                    expandido.append(nova_comb)
                    id_counter += 1
    
    # Remover duplicatas exatas
    seen = set()
    unique = []
    for item in expandido:
        key = (item["tipo"], item["ambiente"], item["area_m2"], 
               item["acabamento"], item["configuracao"])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    
    print(f"Expandido para: {len(unique)} combinações únicas")
    
    return unique


def exportar_catalogo(combinacoes, output_path):
    """Exporta catálogo para CSV."""
    if not combinacoes:
        return
    
    fieldnames = ["id", "tipo", "ambiente", "area_m2", "configuracao", 
                  "acabamento", "descricao", "origem"]
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i, item in enumerate(combinacoes, 1):
            item["id"] = i
            writer.writerow(item)
    
    print(f"Exportado: {output_path}")


def gerar_catalogos_progressivos(input_csv, output_dir):
    """Gera todos os catálogos progressivos."""
    metas = [70, 80, 90, 95]
    
    for meta in metas:
        combinacoes = expandir_base(input_csv, meta=meta)
        output_path = os.path.join(output_dir, f"catalogo_{meta}pct.csv")
        exportar_catalogo(combinacoes, output_path)
        
        print(f"Meta {meta}%: {len(combinacoes)} combinações")


def main():
    parser = argparse.ArgumentParser(description="Expandir base de reformas")
    parser.add_argument("--input", type=str, required=True, help="CSV base curada")
    parser.add_argument("--output", type=str, help="CSV de saída")
    parser.add_argument("--meta", type=int, default=90, choices=[70, 80, 90, 95, 99],
                        help="Meta de cobertura")
    parser.add_argument("--all", action="store_true", help="Gerar todos os catálogos")
    
    args = parser.parse_args()
    
    if args.all:
        output_dir = str(CATALOGO_DIR)
        gerar_catalogos_progressivos(args.input, output_dir)
    else:
        combinacoes = expandir_base(args.input, meta=args.meta)
        
        if args.output:
            exportar_catalogo(combinacoes, args.output)
        else:
            output_path = CATALOGO_DIR / f"catalogo_{args.meta}pct.csv"
            exportar_catalogo(combinacoes, str(output_path))
    
    print("Concluído!")


if __name__ == "__main__":
    main()

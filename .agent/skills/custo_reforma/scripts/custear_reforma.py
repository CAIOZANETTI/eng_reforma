#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: custear_reforma.py
Descrição: Adiciona preços SINAPI ao escopo de reforma
Versão: 1.0
"""

import csv
import json
import argparse
import os
from pathlib import Path

# Diretório base para resources
SCRIPT_DIR = Path(__file__).parent.parent
SINAPI_DEFAULT = SCRIPT_DIR / "resources" / "sinapi_2025.csv"


def carregar_sinapi(filepath):
    """
    Carrega tabela SINAPI em um dicionário.
    
    Returns:
        dict com descrição como chave e dados do serviço como valor
    """
    sinapi = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Indexar por descrição (normalizada)
            desc = row["descricao"].lower().strip()
            sinapi[desc] = {
                "codigo": row["codigo"],
                "descricao": row["descricao"],
                "unidade": row["unidade"],
                "preco_material": float(row.get("preco_material", 0) or 0),
                "preco_mo": float(row.get("preco_mo", 0) or 0),
                "preco_total": float(row.get("preco_total", 0) or 0),
                "grupo": row.get("grupo", ""),
            }
    
    return sinapi


# Mapeamento de serviços do escopo para códigos SINAPI
MAPEAMENTO_SINAPI = {
    "demolição de revestimentos": "97622",
    "demolição de piso": "97622",
    "impermeabilização": "98546",
    "impermeabilização premium": "98557",
    "contrapiso": "94990",
    "contrapiso com caimento": "94991",
    "revestimento piso": "87878",
    "revestimento parede": "87878",
    "porcelanato grande formato piso": "87880",
    "porcelanato grande formato parede": "87880",
    "rejunte": "88485",
    "rejunte epóxi": "88486",
    "rodapé": "88497",
    "rodapé mdf": "88498",
    "pintura parede": "88625",
    "pintura teto": "88625",
    "pintura de teto": "88625",
    "pintura lavável": "88626",
    "pintura 2 demãos": "88625",
    "massa corrida": "88627",
    "selador": "88628",
    "preparo de superfície": "88627",
    "vaso sanitário": "86891",
    "vaso sanitário design": "86893",
    "cuba": "86900",
    "cuba esculpida": "86901",
    "cuba inox": "86910",
    "cuba dupla": "86911",
    "torneira": "86940",
    "torneira gourmet": "86942",
    "torneira de design": "86943",
    "chuveiro/ducha": "86951",
    "ducha com cromoterapia": "86951",  # usar mesmo código, ajustar preço manual
    "ducha higiênica": "86950",
    "box de vidro": "89366",
    "box vidro 10mm até teto": "89367",
    "bancada granito": "89356",
    "bancada quartzo": "89357",
    "forro de gesso": "96113",
    "iluminação led": "93281",
    "iluminação": "93281",
    "iluminação de bancada": "93281",
    "nicho iluminado": "93281",
    "piso vinílico sobreposto": "87540",
    "piso laminado": "87323",
    "marcenaria sob medida": "87878",  # placeholder
    "revestimento área molhada": "87265",
    "troca de louças": "86891",
    "troca de metais": "86940",
    "pintura de azulejos": "88625",
}


def buscar_preco_sinapi(servico, sinapi_db):
    """
    Busca preço SINAPI para um serviço.
    
    Args:
        servico: nome do serviço
        sinapi_db: dicionário SINAPI carregado
    
    Returns:
        dict com dados do serviço ou None
    """
    servico_lower = servico.lower().strip()
    
    # Tentar mapeamento direto
    codigo = MAPEAMENTO_SINAPI.get(servico_lower)
    
    if codigo:
        # Buscar pelo código
        for item in sinapi_db.values():
            if item["codigo"] == codigo:
                return item
    
    # Tentar busca por similaridade
    for desc, item in sinapi_db.items():
        if servico_lower in desc or desc in servico_lower:
            return item
    
    return None


def custear_escopo(escopo_csv, sinapi_csv, bdi=0.25):
    """
    Adiciona preços ao escopo de reforma.
    
    Args:
        escopo_csv: path para CSV de escopo
        sinapi_csv: path para CSV SINAPI
        bdi: Bonificação e Despesas Indiretas (default 25%)
    
    Returns:
        list com escopo custeado
    """
    sinapi_db = carregar_sinapi(sinapi_csv)
    escopo_custeado = []
    total_geral = 0.0
    
    with open(escopo_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            servico = row["servico"]
            quantidade = float(row.get("quantidade", 0) or 0)
            
            # Buscar preço
            dados_sinapi = buscar_preco_sinapi(servico, sinapi_db)
            
            if dados_sinapi:
                preco_base = dados_sinapi["preco_total"]
                codigo = dados_sinapi["codigo"]
            else:
                # Preço estimado genérico
                preco_base = 50.00  # R$ 50/unidade como fallback
                codigo = "N/A"
            
            # Aplicar BDI
            preco_unitario = round(preco_base * (1 + bdi), 2)
            preco_parcial = round(quantidade * preco_unitario, 2)
            total_geral += preco_parcial
            
            escopo_custeado.append({
                "item": row["item"],
                "ambiente": row["ambiente"],
                "servico": servico,
                "descricao": row.get("descricao", servico),
                "codigo_sinapi": codigo,
                "unidade": row["unidade"],
                "quantidade": quantidade,
                "preco_unitario": preco_unitario,
                "preco_parcial": preco_parcial,
            })
    
    return escopo_custeado, total_geral


def exportar_custeado_csv(escopo, total, filepath):
    """Exporta escopo custeado para CSV."""
    fieldnames = [
        "item", "ambiente", "servico", "descricao", "codigo_sinapi",
        "unidade", "quantidade", "preco_unitario", "preco_parcial"
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(escopo)
        
        # Linha de total
        writer.writerow({
            "item": "",
            "ambiente": "",
            "servico": "TOTAL GERAL",
            "descricao": "",
            "codigo_sinapi": "",
            "unidade": "",
            "quantidade": "",
            "preco_unitario": "",
            "preco_parcial": total,
        })
    
    print(f"Escopo custeado exportado: {filepath}")


def gerar_relatorio_sintetico(escopo, total, filepath):
    """Gera relatório sintético em Markdown."""
    md = "# Orçamento Sintético de Reforma\n\n"
    md += f"**Total Geral: R$ {total:,.2f}**\n\n".replace(",", "X").replace(".", ",").replace("X", ".")
    md += "| Item | Ambiente | Serviço | Unid. | Qtd | Preço Unit. | Preço Parcial |\n"
    md += "|:---:|:---|:---|:---:|:---:|---:|---:|\n"
    
    for item in escopo:
        preco_unit_fmt = f"R$ {item['preco_unitario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        preco_parc_fmt = f"R$ {item['preco_parcial']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        md += f"| {item['item']} | {item['ambiente']} | {item['servico']} | {item['unidade']} | {item['quantidade']:.2f} | {preco_unit_fmt} | {preco_parc_fmt} |\n"
    
    total_fmt = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    md += f"| | | **TOTAL** | | | | **{total_fmt}** |\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"Relatório sintético: {filepath}")


def gerar_relatorio_analitico(escopo, total, filepath, sinapi_csv):
    """Gera relatório analítico detalhado em Markdown."""
    sinapi_db = carregar_sinapi(sinapi_csv)
    
    md = "# Orçamento Analítico de Reforma\n\n"
    md += "> Valores baseados na tabela SINAPI com BDI de 25%\n\n"
    md += f"**Total Geral: R$ {total:,.2f}**\n\n".replace(",", "X").replace(".", ",").replace("X", ".")
    md += "---\n\n"
    
    for item in escopo:
        md += f"## {item['item']}. {item['servico']}\n\n"
        md += f"**Ambiente**: {item['ambiente']}  \n"
        md += f"**Código SINAPI**: {item['codigo_sinapi']}  \n"
        md += f"**Unidade**: {item['unidade']}  \n"
        md += f"**Quantidade**: {item['quantidade']:.2f}  \n"
        
        preco_unit_fmt = f"R$ {item['preco_unitario']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        preco_parc_fmt = f"R$ {item['preco_parcial']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        md += f"**Preço Unitário**: {preco_unit_fmt}  \n"
        md += f"**Preço Total**: {preco_parc_fmt}  \n\n"
        
        # Composição se disponível
        codigo = item['codigo_sinapi']
        if codigo != "N/A":
            for desc, dados in sinapi_db.items():
                if dados["codigo"] == codigo:
                    md += "| Componente | Valor |\n"
                    md += "|:---|---:|\n"
                    mat_fmt = f"R$ {dados['preco_material']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    mo_fmt = f"R$ {dados['preco_mo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    md += f"| Material | {mat_fmt} |\n"
                    md += f"| Mão de Obra | {mo_fmt} |\n"
                    break
        
        md += "\n---\n\n"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"Relatório analítico: {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Custear escopo de reforma com SINAPI")
    parser.add_argument("--input", type=str, required=True, help="CSV de escopo")
    parser.add_argument("--sinapi", type=str, default=str(SINAPI_DEFAULT), help="CSV SINAPI")
    parser.add_argument("--bdi", type=float, default=0.25, help="BDI (default 0.25)")
    parser.add_argument("--output", type=str, required=True, help="CSV de saída custeado")
    parser.add_argument("--sintetico", type=str, help="Relatório sintético MD")
    parser.add_argument("--analitico", type=str, help="Relatório analítico MD")
    
    args = parser.parse_args()
    
    # Custear
    escopo, total = custear_escopo(args.input, args.sinapi, args.bdi)
    exportar_custeado_csv(escopo, total, args.output)
    
    print(f"Total: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    # Relatórios opcionais
    if args.sintetico:
        gerar_relatorio_sintetico(escopo, total, args.sintetico)
    
    if args.analitico:
        gerar_relatorio_analitico(escopo, total, args.analitico, args.sinapi)


if __name__ == "__main__":
    main()

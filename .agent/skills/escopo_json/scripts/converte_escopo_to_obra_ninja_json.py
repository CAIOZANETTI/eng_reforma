#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: converte_escopo_to_obra_ninja_json.py
Descrição: Converte escopo custeado CSV para JSON no padrão Obra Ninja
Versão: 1.0
"""

import json
import csv
import uuid
import argparse
import os
from datetime import datetime, timezone
from pathlib import Path

# Diretório base
SCRIPT_DIR = Path(__file__).parent.parent
AMBIENTES_CSV = SCRIPT_DIR / "resources" / "lista_ambientes.csv"
MATERIAIS_CSV = SCRIPT_DIR / "resources" / "lista_materiais.csv"


def gerar_uuid():
    """Gera um UUID v4."""
    return str(uuid.uuid4())


def normalizar_slug(texto):
    """Converte texto para slug."""
    texto = texto.lower().strip()
    substituicoes = {
        'ç': 'c', 'ã': 'a', 'á': 'a', 'à': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o', 'ô': 'o',
        'õ': 'o', 'ú': 'u', 'ü': 'u', ' ': '_', '/': '_',
    }
    for char, sub in substituicoes.items():
        texto = texto.replace(char, sub)
    return texto


def carregar_materiais(filepath):
    """Carrega lista de materiais para mapeamento."""
    materiais = {}
    if not os.path.exists(filepath):
        return materiais
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nome = row.get("nome", "").lower()
            materiais[nome] = {
                "material_id": row.get("material_id", gerar_uuid()),
                "nome": row.get("nome", ""),
                "categoria": row.get("categoria", ""),
                "unidade": row.get("unidade", "un"),
            }
    return materiais


def inferir_tipo_imovel(ambientes):
    """Infere tipo de imóvel baseado nos ambientes."""
    ambientes_lower = [a.lower() for a in ambientes]
    
    if any("escritório" in a or "recepção" in a or "open space" in a for a in ambientes_lower):
        return "escritório"
    if any("loja" in a or "salão de vendas" in a for a in ambientes_lower):
        return "loja"
    if any("consultório" in a or "clínica" in a for a in ambientes_lower):
        return "clínica"
    if any("restaurante" in a or "cozinha industrial" in a for a in ambientes_lower):
        return "restaurante"
    if any("quintal" in a or "garagem" in a or "edícula" in a or "piscina" in a for a in ambientes_lower):
        return "casa"
    
    return "apto"


def converter_escopo_para_json(escopo_csv, materiais_csv=None, project_name=None, description=""):
    """
    Converte escopo CSV para estrutura JSON Obra Ninja.
    
    Args:
        escopo_csv: path para CSV de escopo custeado
        materiais_csv: path para CSV de materiais (opcional)
        project_name: nome do projeto (opcional)
        description: descrição do projeto
    
    Returns:
        dict com estrutura JSON Obra Ninja
    """
    # Carregar materiais para mapeamento
    materiais_db = {}
    if materiais_csv and os.path.exists(materiais_csv):
        materiais_db = carregar_materiais(materiais_csv)
    
    # Agrupar serviços por ambiente
    ambientes_servicos = {}
    area_total = 0
    
    with open(escopo_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Pular linha de total
            if row.get("servico", "").upper() == "TOTAL GERAL":
                continue
            
            ambiente = row.get("ambiente", "Geral")
            
            if ambiente not in ambientes_servicos:
                ambientes_servicos[ambiente] = {
                    "space_id": gerar_uuid(),
                    "_name": ambiente,
                    "area": 0,  # Será estimado
                    "height": 2.6,
                    "services": []
                }
            
            # Criar serviço
            servico_nome = row.get("servico", "")
            quantidade = float(row.get("quantidade", 0) or 0)
            unidade = row.get("unidade", "un")
            
            service = {
                "service_id": normalizar_slug(servico_nome),
                "_name": servico_nome,
                "quantity": quantidade,
                "material_categories": [],
                "labor_categories": []
            }
            
            # Adicionar categoria de material baseado no serviço
            categoria_material = inferir_categoria_material(servico_nome, unidade, quantidade, materiais_db)
            if categoria_material:
                service["material_categories"].append(categoria_material)
            
            # Adicionar categoria de mão de obra
            categoria_labor = inferir_categoria_labor(servico_nome, quantidade)
            if categoria_labor:
                service["labor_categories"].append(categoria_labor)
            
            ambientes_servicos[ambiente]["services"].append(service)
    
    # Estimar áreas dos ambientes
    for amb_nome, amb_data in ambientes_servicos.items():
        area_estimada = estimar_area_ambiente(amb_nome, amb_data["services"])
        amb_data["area"] = area_estimada
        area_total += area_estimada
    
    # Inferir tipo de imóvel
    tipo_imovel = inferir_tipo_imovel(list(ambientes_servicos.keys()))
    
    # Montar estrutura final
    if not project_name:
        project_name = f"Reforma {datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    json_data = {
        "version": "1.0",
        "exportedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "template": {
            "title": project_name,
            "description": description,
            "language_code": "pt-BR",
            "property_type": tipo_imovel,
            "status": "ready"
        },
        "project": {
            "name": project_name,
            "total_area": area_total
        },
        "spaces": list(ambientes_servicos.values())
    }
    
    return json_data


def inferir_categoria_material(servico, unidade, quantidade, materiais_db):
    """Infere categoria de material baseado no serviço."""
    servico_lower = servico.lower()
    
    # Mapeamentos de serviço para material
    mapeamentos = {
        "revestimento piso": ("Revestimento", "Porcelanato 60x60"),
        "revestimento parede": ("Revestimento", "Porcelanato 60x60"),
        "porcelanato": ("Revestimento", "Porcelanato 60x60"),
        "cerâmica": ("Revestimento", "Cerâmica 45x45"),
        "piso vinílico": ("Revestimento", "Piso vinílico clicado"),
        "piso laminado": ("Revestimento", "Piso laminado qualidade"),
        "pintura": ("Pintura", "Tinta acrílica premium"),
        "massa corrida": ("Pintura", "Massa corrida PVA"),
        "rejunte": ("Acessórios", "Rejunte comum"),
        "rejunte epóxi": ("Acessórios", "Rejunte epóxi"),
        "impermeabilização": ("Impermeabilização", "Manta asfáltica 3mm"),
        "vaso sanitário": ("Louças", "Vaso sanitário Deca"),
        "cuba": ("Louças", "Cuba de apoio"),
        "torneira": ("Metais", "Torneira monocomando"),
        "chuveiro": ("Metais", "Chuveiro elétrico"),
        "ducha": ("Metais", "Ducha higiênica"),
        "box": ("Box", "Box vidro temperado 8mm"),
        "bancada": ("Bancadas", "Bancada quartzo"),
        "forro": ("Forro", "Gesso acartonado ST"),
        "iluminação": ("Iluminação", "Luminária LED embutida"),
        "rodapé": ("Acessórios", "Rodapé MDF"),
    }
    
    for keyword, (categoria, material) in mapeamentos.items():
        if keyword in servico_lower:
            return {
                "material_category_id": normalizar_slug(categoria),
                "_name": categoria,
                "base_qtd": quantidade,
                "base_unit": unidade,
                "materials": [
                    {
                        "material_id": gerar_uuid(),
                        "_name": material
                    }
                ]
            }
    
    return None


def inferir_categoria_labor(servico, quantidade):
    """Infere categoria de mão de obra baseado no serviço."""
    servico_lower = servico.lower()
    
    # Mapeamentos de serviço para profissional
    mapeamentos = {
        "demolição": ("Servente", 0.5),
        "contrapiso": ("Pedreiro", 0.8),
        "revestimento": ("Azulejista", 1.0),
        "porcelanato": ("Azulejista", 1.2),
        "cerâmica": ("Azulejista", 0.8),
        "piso": ("Pedreiro", 0.6),
        "pintura": ("Pintor", 0.3),
        "massa": ("Pintor", 0.2),
        "impermeabilização": ("Pedreiro", 0.5),
        "vaso": ("Encanador", 1.5),
        "cuba": ("Encanador", 1.0),
        "torneira": ("Encanador", 0.5),
        "chuveiro": ("Encanador", 0.5),
        "box": ("Vidraceiro", 2.0),
        "bancada": ("Marmorista", 1.5),
        "forro": ("Gesseiro", 0.8),
        "elétrica": ("Eletricista", 1.0),
        "iluminação": ("Eletricista", 0.5),
    }
    
    for keyword, (profissional, horas_por_unidade) in mapeamentos.items():
        if keyword in servico_lower:
            return {
                "labor_category_id": normalizar_slug(profissional),
                "_name": profissional,
                "base_qtd": round(quantidade * horas_por_unidade, 2),
                "base_unit": "h",
                "labors": [
                    {
                        "labor_id": gerar_uuid(),
                        "_name": profissional
                    }
                ]
            }
    
    return None


def estimar_area_ambiente(nome, services):
    """Estima área do ambiente baseado nos serviços."""
    # Procurar serviços de piso para estimar área
    for service in services:
        nome_servico = service["_name"].lower()
        if "piso" in nome_servico or "contrapiso" in nome_servico:
            # Descontar fator de perda
            return round(service["quantity"] / 1.1, 2)
    
    # Fallback: usar média baseada no tipo de ambiente
    areas_medias = {
        "banheiro": 5,
        "lavabo": 2,
        "cozinha": 10,
        "sala": 20,
        "quarto": 12,
        "suíte": 16,
        "lavanderia": 5,
        "varanda": 8,
    }
    
    nome_lower = nome.lower()
    for key, area in areas_medias.items():
        if key in nome_lower:
            return area
    
    return 10  # Default


def main():
    parser = argparse.ArgumentParser(description="Converter escopo para JSON Obra Ninja")
    parser.add_argument("--input", type=str, required=True, help="CSV de escopo custeado")
    parser.add_argument("--output", type=str, required=True, help="JSON de saída")
    parser.add_argument("--materiais", type=str, default=str(MATERIAIS_CSV),
                        help="CSV de materiais para mapeamento")
    parser.add_argument("--nome", type=str, help="Nome do projeto")
    parser.add_argument("--descricao", type=str, default="", help="Descrição do projeto")
    
    args = parser.parse_args()
    
    json_data = converter_escopo_para_json(
        args.input,
        args.materiais,
        args.nome,
        args.descricao
    )
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"JSON gerado: {args.output}")
    print(f"Total de ambientes: {len(json_data['spaces'])}")
    print(f"Área total: {json_data['project']['total_area']} m²")


if __name__ == "__main__":
    main()

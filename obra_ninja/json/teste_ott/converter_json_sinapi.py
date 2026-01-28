"""
Conversor de JSON Obra Ninja para Orçamento SINAPI
Lê os JSONs de reforma de telhado e gera tabelas orçamentárias detalhadas
"""

import json
import pandas as pd
from pathlib import Path

# Carregar catálogo de materiais
materials_catalog = pd.read_csv(r"d:\github\eng_reforma\obra_ninja\csv\download\materials-28012026.csv")
materials_dict = dict(zip(materials_catalog['ID'], materials_catalog['Name']))

# Preços de referência SINAPI (Janeiro 2026 - SP)
PRECOS_MATERIAIS = {
    "cacamba_entulho_media": 450.00,
    "viga_madeira_serrada_6x12": 45.00,  # por metro
    "pontalete_madeira_serrada_7,5x7,5": 28.00,
    "caibro_madeira_serrada_6x6": 22.00,
    "ripa_madeira_serrada_1x2,5": 8.50,
    "prego_18x27": 12.00,  # por kg
    "parafuso_zincado_5/16\"": 0.80,  # por unidade
    "telha_fibrocimento_6mm": 38.00,  # por m²
    "cumeeira_fibrocimento": 42.00,  # por metro
    "telha_ceramica_romana": 68.00,
    "cumeeira_ceramica": 55.00,
    "telha_concreto_classica": 95.00,
    "cumeeira_concreto": 72.00,
}

PRECOS_MAO_OBRA = {
    "carpinteiro": 28.50,  # por hora com encargos
    "servente": 19.20,
    "pedreiro": 28.50,
    "encanador": 32.00,
}

def load_project_json(filepath):
    """Carrega JSON do projeto"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_materials_from_json(project_data):
    """Extrai materiais e quantidades do JSON"""
    materials_list = []
    labor_list = []
    
    for space in project_data.get('spaces', []):
        space_name = space.get('_name', 'N/A')
        space_area = space.get('area', 0)
        
        for service in space.get('services', []):
            service_name = service.get('_name', 'N/A')
            service_qty = service.get('quantity', 1)
            
            # Materiais
            for mat_cat in service.get('material_categories', []):
                base_qtd = mat_cat.get('base_qtd', 0)
                base_unit = mat_cat.get('base_unit', '')
                category_name = mat_cat.get('_name', '')
                
                for material in mat_cat.get('materials', []):
                    mat_id = material.get('material_id', '')
                    mat_name = material.get('_name', '')
                    
                    # Calcular quantidade total
                    if base_unit == 'm2':
                        total_qty = base_qtd * space_area * service_qty
                    elif base_unit == 'm':
                        total_qty = base_qtd * service_qty
                    elif base_unit == 'kg':
                        total_qty = base_qtd * service_qty
                    elif base_unit == 'pack':
                        total_qty = base_qtd * service_qty
                    else:
                        total_qty = base_qtd * service_qty
                    
                    materials_list.append({
                        'service': service_name,
                        'category': category_name,
                        'material_id': mat_id,
                        'material_name': mat_name,
                        'base_qtd': base_qtd,
                        'unit': base_unit,
                        'service_qty': service_qty,
                        'space_area': space_area,
                        'total_qty': total_qty
                    })
            
            # Mão de obra
            for labor_cat in service.get('labor_categories', []):
                base_qtd = labor_cat.get('base_qtd', 0)
                base_unit = labor_cat.get('base_unit', 'h')
                category_name = labor_cat.get('_name', '')
                
                # Calcular horas totais
                if base_unit == 'h':
                    if 'm2' in str(service.get('service_id', '')):
                        total_hours = base_qtd * space_area * service_qty
                    else:
                        total_hours = base_qtd * service_qty
                else:
                    total_hours = base_qtd * service_qty
                
                labor_list.append({
                    'service': service_name,
                    'labor_category': category_name,
                    'base_qtd': base_qtd,
                    'unit': base_unit,
                    'total_hours': total_hours
                })
    
    return materials_list, labor_list

def generate_budget_table(project_name, materials, labor):
    """Gera tabela orçamentária"""
    print(f"\n{'='*80}")
    print(f"ORÇAMENTO ANALÍTICO - {project_name.upper()}")
    print(f"{'='*80}\n")
    
    # Agrupar por serviço
    services = {}
    for mat in materials:
        svc = mat['service']
        if svc not in services:
            services[svc] = {'materials': [], 'labor': []}
        services[svc]['materials'].append(mat)
    
    for lab in labor:
        svc = lab['service']
        if svc not in services:
            services[svc] = {'materials': [], 'labor': []}
        services[svc]['labor'].append(lab)
    
    total_materials = 0
    total_labor = 0
    
    for service_name, items in services.items():
        print(f"\n{service_name.upper()}")
        print("-" * 80)
        
        # Materiais
        if items['materials']:
            print(f"\n{'Material':<40} {'Unid':<6} {'Qtd':>10} {'Preço Unit':>12} {'Total':>12}")
            print("-" * 80)
            
            for mat in items['materials']:
                mat_name = mat['material_name']
                qty = mat['total_qty']
                unit = mat['unit']
                
                # Buscar preço
                price = PRECOS_MATERIAIS.get(mat_name, 0)
                total = qty * price
                total_materials += total
                
                print(f"{mat_name:<40} {unit:<6} {qty:>10.2f} R$ {price:>9.2f} R$ {total:>9.2f}")
        
        # Mão de obra
        if items['labor']:
            print(f"\n{'Mão de Obra':<40} {'Unid':<6} {'Horas':>10} {'Preço/h':>12} {'Total':>12}")
            print("-" * 80)
            
            for lab in items['labor']:
                labor_name = lab['labor_category']
                hours = lab['total_hours']
                
                # Buscar preço
                price = PRECOS_MAO_OBRA.get(labor_name, 0)
                total = hours * price
                total_labor += total
                
                print(f"{labor_name:<40} {'h':<6} {hours:>10.2f} R$ {price:>9.2f} R$ {total:>9.2f}")
    
    # Totais
    print(f"\n{'='*80}")
    print(f"{'SUBTOTAL MATERIAIS':<58} R$ {total_materials:>18.2f}")
    print(f"{'SUBTOTAL MÃO DE OBRA':<58} R$ {total_labor:>18.2f}")
    custo_direto = total_materials + total_labor
    print(f"{'CUSTO DIRETO TOTAL':<58} R$ {custo_direto:>18.2f}")
    
    bdi = custo_direto * 0.28
    print(f"{'BDI (28%)':<58} R$ {bdi:>18.2f}")
    
    preco_venda = custo_direto + bdi
    print(f"{'PREÇO DE VENDA':<58} R$ {preco_venda:>18.2f}")
    print(f"{'='*80}\n")
    
    return {
        'materiais': total_materials,
        'mao_obra': total_labor,
        'custo_direto': custo_direto,
        'bdi': bdi,
        'preco_venda': preco_venda
    }

# Processar os 3 projetos
projetos = [
    ("Telhado Fibrocimento", r"d:\github\eng_reforma\obra_ninja\json\teste_ott\reforma_telhado_fibrocimento.json"),
    ("Telhado Cerâmica Romana", r"d:\github\eng_reforma\obra_ninja\json\teste_ott\reforma_telhado_ceramica.json"),
    ("Telhado Concreto Clássica", r"d:\github\eng_reforma\obra_ninja\json\teste_ott\reforma_telhado_concreto.json"),
]

resultados = {}

for nome, filepath in projetos:
    print(f"\n\n{'#'*80}")
    print(f"# PROCESSANDO: {nome}")
    print(f"{'#'*80}")
    
    data = load_project_json(filepath)
    materials, labor = extract_materials_from_json(data)
    resultado = generate_budget_table(nome, materials, labor)
    resultados[nome] = resultado

# Comparativo final
print(f"\n\n{'='*80}")
print("COMPARATIVO DOS 3 PROJETOS")
print(f"{'='*80}\n")

print(f"{'Projeto':<30} {'Custo Direto':>15} {'BDI (28%)':>15} {'Preço Venda':>15}")
print("-" * 80)

for nome, res in resultados.items():
    print(f"{nome:<30} R$ {res['custo_direto']:>12.2f} R$ {res['bdi']:>12.2f} R$ {res['preco_venda']:>12.2f}")

print(f"{'='*80}\n")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: validar_combinacao.py
Descrição: Valida se uma combinação de reforma é válida
Versão: 1.0
"""

import csv
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
RESOURCES_DIR = SCRIPT_DIR / "resources"


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


def validar(tipo, ambiente, area=None, acabamento=None, config=None):
    """
    Valida uma combinação de reforma.
    
    Args:
        tipo: Tipo de imóvel (Apto, Casa, Escritório, etc.)
        ambiente: Nome do ambiente
        area: Área em m² (opcional)
        acabamento: Padrão de acabamento (opcional)
        config: Configuração do imóvel (opcional)
    
    Returns:
        dict com resultado da validação
    """
    faixas = carregar_faixas_area()
    matriz = carregar_matriz_compatibilidade()
    
    erros = []
    avisos = []
    sugestoes = []
    
    # 1. Validar tipo de imóvel
    tipos_validos = ["Apto", "Casa", "Escritório", "Loja", "Clínica", "Restaurante"]
    if tipo not in tipos_validos:
        erros.append(f"Tipo '{tipo}' inválido. Use: {', '.join(tipos_validos)}")
    
    # 2. Validar compatibilidade tipo-ambiente
    if tipo in matriz:
        if ambiente not in matriz[tipo]:
            erros.append(f"Ambiente '{ambiente}' não existe para tipo '{tipo}'")
            # Sugerir ambientes válidos
            validos = [a for a, v in matriz[tipo].items() if v["valido"]]
            sugestoes.append(f"Ambientes válidos para {tipo}: {', '.join(validos[:5])}...")
        elif not matriz[tipo][ambiente]["valido"]:
            erros.append(f"Combinação {tipo}/{ambiente} está desabilitada")
    
    # 3. Validar área
    if area is not None:
        if ambiente in faixas:
            faixa = faixas[ambiente]
            if area < faixa["min"]:
                erros.append(f"Área {area}m² menor que mínimo {faixa['min']}m² para {ambiente}")
                sugestoes.append(f"Área sugerida: {faixa['default']}m²")
            elif faixa["max"] > 0 and area > faixa["max"]:
                erros.append(f"Área {area}m² maior que máximo {faixa['max']}m² para {ambiente}")
                sugestoes.append(f"Área sugerida: {faixa['default']}m²")
            elif area < faixa["default"] * 0.5:
                avisos.append(f"Área {area}m² está abaixo do comum para {ambiente}")
        else:
            avisos.append(f"Ambiente '{ambiente}' não tem faixas de área definidas")
    
    # 4. Validar acabamento
    if acabamento:
        if tipo in ["Escritório", "Loja", "Clínica", "Restaurante"]:
            if acabamento.lower() != "comercial":
                erros.append(f"Tipo '{tipo}' requer acabamento 'Comercial'")
        else:
            acabamentos_validos = ["popular", "médio", "medio", "luxo"]
            if acabamento.lower() not in acabamentos_validos:
                avisos.append(f"Acabamento '{acabamento}' não reconhecido")
    
    # 5. Validar configuração
    if config:
        configs_validas = {
            "Apto": ["1Q+1B", "2Q+1B", "2Q+2B", "3Q+2B", "3Q+3B", "4Q+3B"],
            "Casa": ["1Q+1B", "2Q+1B", "2Q+2B", "3Q+2B", "3Q+3B", "4Q+3B"],
            "Escritório": ["0Q+1B", "0Q+2B", "0Q+4B"],
            "Loja": ["0Q+1B", "0Q+2B"],
            "Clínica": ["0Q+1B", "0Q+2B"],
            "Restaurante": ["0Q+2B", "0Q+4B"]
        }
        
        if tipo in configs_validas:
            if config not in configs_validas[tipo]:
                avisos.append(f"Configuração '{config}' não é comum para {tipo}")
    
    # Resultado
    is_valid = len(erros) == 0
    
    return {
        "valido": is_valid,
        "combinacao": {
            "tipo": tipo,
            "ambiente": ambiente,
            "area": area,
            "acabamento": acabamento,
            "config": config
        },
        "erros": erros,
        "avisos": avisos,
        "sugestoes": sugestoes
    }


def main():
    parser = argparse.ArgumentParser(description="Validar combinação de reforma")
    parser.add_argument("--tipo", type=str, required=True, help="Tipo de imóvel")
    parser.add_argument("--ambiente", type=str, required=True, help="Nome do ambiente")
    parser.add_argument("--area", type=float, help="Área em m²")
    parser.add_argument("--acabamento", type=str, help="Padrão de acabamento")
    parser.add_argument("--config", type=str, help="Configuração do imóvel")
    parser.add_argument("--json", action="store_true", help="Output em JSON")
    
    args = parser.parse_args()
    
    resultado = validar(
        args.tipo,
        args.ambiente,
        args.area,
        args.acabamento,
        args.config
    )
    
    if args.json:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    else:
        print(f"\nValidacao: {args.tipo} / {args.ambiente}")
        print(f"Resultado: {'[OK] VALIDO' if resultado['valido'] else '[ERRO] INVALIDO'}")
        
        if resultado['erros']:
            print("\nErros:")
            for e in resultado['erros']:
                print(f"  - {e}")
        
        if resultado['avisos']:
            print("\nAvisos:")
            for a in resultado['avisos']:
                print(f"  - {a}")
        
        if resultado['sugestoes']:
            print("\nSugestoes:")
            for s in resultado['sugestoes']:
                print(f"  - {s}")


if __name__ == "__main__":
    main()

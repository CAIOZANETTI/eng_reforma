#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo: prompt_tabela.py
Descrição: Converte prompts em linguagem natural para tabela estruturada
Versão: 1.0
"""

import json
import re
import argparse
from pathlib import Path

# Sinônimos para normalização
SINONIMOS = {
    # Ambientes
    "banheiro": ["wc", "toilette", "sanitário", "lavabo", "bwc"],
    "cozinha": ["copa", "área de cozinha", "copa-cozinha"],
    "sala": ["living", "estar", "sala de estar", "sala de jantar"],
    "quarto": ["dormitório", "suíte", "dormitorio", "alcova"],
    "varanda": ["sacada", "terraço", "balcão", "terraco"],
    "lavanderia": ["área de serviço", "area de servico", "lavabo"],
    "escritório": ["home office", "escritorio", "office", "homeoffice"],
    "garagem": ["garage", "vaga", "estacionamento"],
    
    # Serviços
    "piso": ["chão", "pavimento", "revestimento de piso", "chao"],
    "parede": ["revestimento de parede", "azulejo"],
    "pintura": ["pintar", "tinta", "repintar"],
    "louça": ["vaso", "pia", "cuba", "sanitário", "bacia"],
    "metais": ["torneira", "chuveiro", "ducha", "misturador"],
    "marcenaria": ["armário", "móvel", "armarios", "moveis"],
    "box": ["boxe", "box de vidro", "blindex"],
    "impermeabilização": ["impermeabilizar", "manta"],
    "elétrica": ["eletrica", "tomada", "interruptor", "fiação"],
    "hidráulica": ["hidraulica", "encanamento", "tubulação"],
}

# Indicadores de padrão de acabamento
INDICADORES_PADRAO = {
    "popular": ["barato", "simples", "básico", "basico", "econômico", "economico", "menor custo"],
    "médio": ["bom", "normal", "padrão", "padrao", "intermediário", "intermediario"],
    "luxo": ["deca", "portobello", "premium", "design", "alto padrão", "alto padrao", "sofisticado", "topo de linha"],
}

# Configurações de imóvel por tipo
CONFIG_IMOVEL = {
    "1Q+1B": {"area": 40, "quartos": 1, "banheiros": 1},
    "2Q+1B": {"area": 55, "quartos": 2, "banheiros": 1},
    "2Q+2B": {"area": 65, "quartos": 2, "banheiros": 2},
    "3Q+2B": {"area": 85, "quartos": 3, "banheiros": 2},
    "3Q+3B": {"area": 100, "quartos": 3, "banheiros": 3},
    "4Q+3B": {"area": 140, "quartos": 4, "banheiros": 3},
}


def normalizar_texto(texto):
    """Normaliza texto para análise."""
    texto = texto.lower().strip()
    # Remover acentos básicos
    substituicoes = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ü': 'u',
        'ç': 'c',
    }
    for char, sub in substituicoes.items():
        texto = texto.replace(char, sub)
    return texto


def extrair_ambiente(texto):
    """Extrai ambiente mencionado no texto."""
    texto_norm = normalizar_texto(texto)
    ambientes_encontrados = []
    
    # Mapeamento direto
    ambientes_diretos = [
        "banheiro", "banheiro social", "lavabo", "cozinha", "cozinha americana",
        "sala", "quarto", "suíte", "suite", "quarto solteiro", "quarto hóspedes",
        "varanda", "varanda gourmet", "lavanderia", "área de serviço", "area de servico",
        "escritório", "escritorio", "home office", "garagem", "quintal", "jardim",
        "área gourmet", "area gourmet", "churrasqueira", "piscina", "telhado",
        "fachada", "geral", "apartamento", "casa", "inteiro", "completo"
    ]
    
    for ambiente in ambientes_diretos:
        if ambiente in texto_norm:
            # Normalizar
            if ambiente in ["apartamento", "inteiro", "completo"]:
                ambientes_encontrados.append("Geral")
            elif ambiente in ["suite", "suíte"]:
                ambientes_encontrados.append("Suíte")
            else:
                ambientes_encontrados.append(ambiente.title())
    
    # Checar sinônimos
    for ambiente_padrao, sinonimos in SINONIMOS.items():
        for sinonimo in sinonimos:
            if sinonimo in texto_norm and ambiente_padrao.title() not in ambientes_encontrados:
                ambientes_encontrados.append(ambiente_padrao.title())
    
    return ambientes_encontrados if ambientes_encontrados else ["Geral"]


def extrair_servicos(texto):
    """Extrai serviços mencionados no texto."""
    texto_norm = normalizar_texto(texto)
    servicos_encontrados = []
    
    # Mapeamento de palavras-chave para serviços
    mapeamento_servicos = {
        "piso": ["trocar piso", "troca de piso", "piso novo"],
        "revestimento de parede": ["azulejo", "cerâmica parede", "revestimento"],
        "pintura": ["pintar", "pintura", "repintar", "tinta"],
        "louças": ["vaso", "pia", "cuba", "louças", "loucas"],
        "metais": ["torneira", "chuveiro", "ducha", "metais"],
        "box de vidro": ["box", "blindex", "vidro temperado"],
        "bancada": ["bancada", "granito", "mármore", "marmore", "quartzo"],
        "marcenaria": ["armário", "armarios", "móvel", "movel", "planejado"],
        "impermeabilização": ["impermeabilizar", "manta", "vazamento"],
        "elétrica": ["elétrica", "eletrica", "tomada", "interruptor"],
        "hidráulica": ["hidráulica", "hidraulica", "encanamento"],
        "forro de gesso": ["gesso", "forro", "rebaixo"],
        "iluminação": ["luz", "iluminação", "iluminacao", "led", "luminária"],
        "demolição": ["demolir", "quebrar", "remover"],
    }
    
    for servico, keywords in mapeamento_servicos.items():
        for keyword in keywords:
            if keyword in texto_norm:
                if servico not in servicos_encontrados:
                    servicos_encontrados.append(servico)
    
    # Se não encontrou serviços específicos, assumir reforma completa
    if not servicos_encontrados:
        if any(palavra in texto_norm for palavra in ["reform", "complet", "total", "geral"]):
            servicos_encontrados = ["reforma completa"]
    
    return servicos_encontrados


def extrair_acabamento(texto):
    """Extrai padrão de acabamento do texto."""
    texto_norm = normalizar_texto(texto)
    
    for padrao, indicadores in INDICADORES_PADRAO.items():
        for indicador in indicadores:
            if indicador in texto_norm:
                return padrao.title()
    
    # Se mencionar marcas específicas
    marcas_luxo = ["deca", "portobello", "portinari", "roca", "kohler", "grohe"]
    marcas_media = ["docol", "celite", "eliane", "pointer"]
    
    for marca in marcas_luxo:
        if marca in texto_norm:
            return "Luxo"
    
    for marca in marcas_media:
        if marca in texto_norm:
            return "Médio"
    
    return "Médio"  # Default


def extrair_area(texto):
    """Extrai área mencionada no texto."""
    # Padrões para área
    padroes = [
        r'(\d+)\s*m[²2]',
        r'(\d+)\s*metros?\s*quadrados?',
        r'área?\s*(?:de|:)?\s*(\d+)',
    ]
    
    for padrao in padroes:
        match = re.search(padrao, texto.lower())
        if match:
            return float(match.group(1))
    
    return None


def extrair_configuracao(texto):
    """Extrai configuração do imóvel (quartos/banheiros)."""
    # Padrões como "2 quartos", "3Q+2B", etc
    padroes = [
        r'(\d)\s*(?:quartos?|q)\s*(?:e|,|\+)?\s*(\d)\s*(?:banheiros?|b)',
        r'(\d)q\s*\+?\s*(\d)b',
    ]
    
    for padrao in padroes:
        match = re.search(padrao, texto.lower())
        if match:
            quartos = int(match.group(1))
            banheiros = int(match.group(2))
            return f"{quartos}Q+{banheiros}B"
    
    return None


def extrair_tipo_imovel(texto):
    """Extrai tipo de imóvel."""
    texto_norm = normalizar_texto(texto)
    
    if any(palavra in texto_norm for palavra in ["apartamento", "apto", "apt"]):
        return "apto"
    if any(palavra in texto_norm for palavra in ["casa", "sobrado", "residência", "residencia"]):
        return "casa"
    if any(palavra in texto_norm for palavra in ["escritório", "escritorio", "comercial", "sala comercial"]):
        return "escritório"
    if any(palavra in texto_norm for palavra in ["loja", "comércio", "comercio"]):
        return "loja"
    
    return "apto"  # Default


def processar_prompt(prompt):
    """
    Processa um prompt em linguagem natural e extrai informações estruturadas.
    
    Args:
        prompt: texto do usuário
    
    Returns:
        dict com dados estruturados
    """
    ambientes = extrair_ambiente(prompt)
    servicos = extrair_servicos(prompt)
    acabamento = extrair_acabamento(prompt)
    area = extrair_area(prompt)
    configuracao = extrair_configuracao(prompt)
    tipo_imovel = extrair_tipo_imovel(prompt)
    
    # Estimar área se não informada
    if not area:
        if configuracao and configuracao in CONFIG_IMOVEL:
            area = CONFIG_IMOVEL[configuracao]["area"]
        else:
            # Estimar por tipo de imóvel
            area = {"apto": 55, "casa": 100, "escritório": 80, "loja": 60}.get(tipo_imovel, 55)
    
    # Estimar área por ambiente
    ambientes_dados = []
    for ambiente in ambientes:
        area_ambiente = estimar_area_ambiente(ambiente, area, len(ambientes))
        ambientes_dados.append({
            "nome": ambiente,
            "area_estimada": area_ambiente,
            "servicos": servicos if ambiente != "Geral" else ["reforma completa"]
        })
    
    resultado = {
        "tipo": tipo_imovel,
        "area_total": area,
        "configuracao": configuracao,
        "acabamento": acabamento,
        "ambientes": ambientes_dados,
        "servicos_gerais": servicos,
        "prompt_original": prompt,
        "confianca": calcular_confianca(prompt, ambientes, servicos)
    }
    
    return resultado


def estimar_area_ambiente(ambiente, area_total, num_ambientes):
    """Estima área de um ambiente específico."""
    proporcoes = {
        "Banheiro": 0.08,
        "Banheiro Social": 0.06,
        "Lavabo": 0.04,
        "Cozinha": 0.12,
        "Cozinha Americana": 0.15,
        "Sala": 0.25,
        "Quarto": 0.15,
        "Suíte": 0.18,
        "Quarto Solteiro": 0.12,
        "Varanda": 0.08,
        "Lavanderia": 0.06,
        "Escritório": 0.10,
        "Home Office": 0.08,
        "Garagem": 0.20,
        "Geral": 1.0,
    }
    
    proporcao = proporcoes.get(ambiente, 0.10)
    
    if ambiente == "Geral":
        return area_total
    
    return round(area_total * proporcao, 2)


def calcular_confianca(prompt, ambientes, servicos):
    """Calcula nível de confiança da interpretação."""
    score = 0.5  # Base
    
    # Mais ambientes identificados = mais confiança
    if len(ambientes) > 0 and ambientes[0] != "Geral":
        score += 0.15
    
    # Mais serviços identificados = mais confiança
    if len(servicos) > 1:
        score += 0.15
    
    # Palavras-chave claras
    palavras_claras = ["reforma", "trocar", "instalar", "remover", "pintar"]
    for palavra in palavras_claras:
        if palavra in prompt.lower():
            score += 0.05
    
    return min(round(score, 2), 1.0)


def main():
    parser = argparse.ArgumentParser(description="Converter prompt para tabela")
    parser.add_argument("--prompt", type=str, help="Texto do prompt")
    parser.add_argument("--input", type=str, help="Arquivo com prompt")
    parser.add_argument("--output", type=str, help="Arquivo JSON de saída")
    
    args = parser.parse_args()
    
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            prompt = f.read()
    elif args.prompt:
        prompt = args.prompt
    else:
        # Exemplo interativo
        print("Digite o prompt (ou pressione Enter para exemplo):")
        prompt = input().strip()
        if not prompt:
            prompt = "Quero reformar o banheiro do meu apartamento de 60m2, trocar piso e louças Deca"
    
    resultado = processar_prompt(prompt)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        print(f"Resultado salvo em: {args.output}")
    else:
        print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

"""
Skill: Cálculo de BDI e Preço de Venda
Descrição: Calcula a taxa de BDI (Benefícios e Despesas Indiretas) e o Preço de Venda final de serviços de engenharia, conforme fórmulas padrão do TCU/SINAPI.
"""

def calcular_bdi(taxas_impostos, despesas_indiretas, lucro_previsto):
    """
    Calcula o BDI baseada na fórmula do Instituto de Engenharia / TCU.
    
    Fórmula Padronizada:
    BDI = { [ (1 + AC + S + R) * (1 + DF) * (1 + L) ] / (1 - I) } - 1
    
    Onde:
    AC = Administração Central
    S = Seguros e Garantias
    R = Risco
    DF = Despesas Financeiras
    L = Lucro
    I = Impostos (PIS, COFINS, ISS, CPRB)
    """
    
    # Extrair variáveis (inputs em percentual, converter para decimal)
    AC = despesas_indiretas.get('adm_central', 0) / 100
    S = despesas_indiretas.get('seguros', 0) / 100
    R = despesas_indiretas.get('riscos', 0) / 100
    DF = despesas_indiretas.get('despesas_financeiras', 0) / 100
    L = lucro_previsto / 100
    
    # Soma dos impostos
    I = sum(taxas_impostos.values()) / 100
    
    if I >= 1:
        raise ValueError("A soma dos impostos não pode ser 100% ou mais.")
        
    numerador = (1 + AC + S + R) * (1 + DF) * (1 + L)
    denominador = (1 - I)
    
    bdi_decimal = (numerador / denominador) - 1
    bdi_percentual = bdi_decimal * 100
    
    return round(bdi_percentual, 2)

def calcular_preco_venda(custo_direto, bdi_percentual):
    """
    Aplica o BDI sobre o Custo Direto para encontrar o Preço de Venda.
    """
    fator = 1 + (bdi_percentual / 100)
    preco_venda = custo_direto * fator
    return round(preco_venda, 2)

def detalhar_preco(custo_direto, bdi_percentual, taxas_impostos):
    """
    Gera um detalhamento reverso de para onde vai o dinheiro.
    Warning: Cálculo simplificado para visualização.
    """
    pv = calcular_preco_venda(custo_direto, bdi_percentual)
    impostos_total = sum(taxas_impostos.values()) / 100
    valor_impostos = pv * impostos_total
    
    # O valor restante (PV - CD - Impostos) é a Margem Bruta (Lucro + Despesas Indiretas)
    margem_bruta = pv - custo_direto - valor_impostos
    
    return {
        "Custo Direto": custo_direto,
        "Preço Venda": pv,
        "Valor BDI": pv - custo_direto,
        "Destino": {
            "Impostos": valor_impostos,
            "Margem Operacional (Lucro + Desp. Ind.)": margem_bruta,
            "Custo Produção": custo_direto
        }
    }

# Exemplo padrão SINAPI (Sem desoneração)
PADRAO_SIMPLES_NACIONAL = {
    "impostos": {
        "PIS": 0.65,
        "COFINS": 3.00,
        "ISS": 5.00, # Varia por município (2 a 5%)
        "CPRB": 0.00 # Se não desonerado
    },
    "indiretos": {
        "adm_central": 3.00,
        "seguros": 0.80,
        "riscos": 0.97,
        "despesas_financeiras": 0.59
    },
    "lucro": 6.16 # Lucro operacional
}

PADRAO_LUCRO_PRESUMIDO = {
    "impostos": {
        "PIS": 0.65,
        "COFINS": 3.00,
        "ISS": 5.00,
        "CPRB": 4.50 # Com desoneração
    },
    "indiretos": {
        "adm_central": 4.00,
        "seguros": 0.80,
        "riscos": 1.27,
        "despesas_financeiras": 1.23
    },
    "lucro": 7.40
}

if __name__ == "__main__":
    custo = 10000.00 # Custo Direto Exemplo
    
    print("--- SIMULAÇÃO BDI ---")
    
    # Caso 1: Reforma Pequena (Simples Nacional)
    bdi_simples = calcular_bdi(PADRAO_SIMPLES_NACIONAL['impostos'], PADRAO_SIMPLES_NACIONAL['indiretos'], 10.0) # Lucro 10%
    detalhe = detalhar_preco(custo, bdi_simples, PADRAO_SIMPLES_NACIONAL['impostos'])
    
    print(f"\nCENÁRIO: Reforma Simples Nacional (Lucro 10%)")
    print(f"Custo Direto: R$ {custo:,.2f}")
    print(f"BDI Calculado: {bdi_simples}%")
    print(f"Preço de Venda: R$ {detalhe['Preço Venda']:,.2f}")

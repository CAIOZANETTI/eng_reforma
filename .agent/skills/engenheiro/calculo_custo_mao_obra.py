"""
Skill: Cálculo de Custo Horário de Mão de Obra
Descrição: Calcula o custo real da hora-homem considerando salário base, encargos sociais (Grupo A, B, C, D) e benefícios (Vale Transporte, Alimentação, EPI).
"""

def calcular_custo_horario(salario_mensal, horas_mensais=220, tipo_encargos='horista', regime='simples'):
    """
    Calcula o custo total da hora do trabalhador.
    
    Args:
        salario_mensal (float): Salário base em carteira.
        horas_mensais (int): Divisor de horas (padrão 220h).
        tipo_encargos (str): 'horista' ou 'mensalista'.
        regime (str): 'simples' (Simples Nacional) ou 'real' (Lucro Real/Presumido).
        
    Returns:
        dict: Detalhamento do custo.
    """
    
    # 1. Salário Base Hora
    salario_hora = salario_mensal / horas_mensais
    
    # 2. Definição de Encargos Sociais (Estimativa baseada em SINAPI SP)
    # Grupo A: INSS, FGTS, SESI, SENAI...
    # Grupo B: Férias, 13º, Feriados, Auxílio Enfermidade...
    # Grupo C: Aviso Prévio, Indenização...
    # Grupo D: Reincidência de Grupo A sobre B.
    
    if regime == 'simples':
        # Simples Nacional tem isenção de parte dos encargos patronais (INSS 20%)
        encargos_percent = 84.00 if tipo_encargos == 'horista' else 45.00
    else:
        # Regime normal (encargos cheios)
        encargos_percent = 115.00 if tipo_encargos == 'horista' else 75.00
        
    custo_encargos = salario_hora * (encargos_percent / 100)
    
    # 3. Benefícios (Estimativa por hora)
    # VR (~R$ 25/dia), VT (~R$ 15/dia), EPI/Ferramentas (~R$ 5/dia) = R$ 45/dia
    # Dias úteis ~21. Custo mensal ~R$ 945.00
    beneficios_mensal = 945.00
    beneficios_hora = beneficios_mensal / horas_mensais
    
    custo_total_hora = salario_hora + custo_encargos + beneficios_hora
    
    return {
        "regime": regime,
        "salario_base_hora": round(salario_hora, 2),
        "encargos_sociais_hora": round(custo_encargos, 2),
        "beneficios_hora": round(beneficios_hora, 2),
        "custo_total_hora": round(custo_total_hora, 2),
        "fator_k": round(custo_total_hora / salario_hora, 2) # Multiplicador sobre o salário
    }

if __name__ == "__main__":
    # Exemplo Pedreiro
    salario = 2800.00
    
    print(f"CÁLCULO CUSTO MÃO DE OBRA (Salário Base: R$ {salario:.2f})")
    
    # Cenário 1: Empresa Simples Nacional
    res_simples = calcular_custo_horario(salario, regime='simples')
    print(f"\n[Simples Nacional] Custo Hora: R$ {res_simples['custo_total_hora']} (Fator K: {res_simples['fator_k']})")
    
    # Cenário 2: Construtora Grande (Lucro Real)
    res_real = calcular_custo_horario(salario, regime='real')
    print(f"[Lucro Real]     Custo Hora: R$ {res_real['custo_total_hora']} (Fator K: {res_real['fator_k']})")

"""
Skill: Legislação Trabalhista (Calculadora de Adicionais)
Descrição: Aplica as regras da CLT para cálculo de horas extras, adicional noturno, insalubridade e periculosidade em orçamentos de mão de obra.
"""

def calcular_adicionais_clt(custo_hora_base, horas_extras=0, periculosidade=False, insalubridade_grau=None):
    """
    Calcula o impacto financeiro de adicionais trabalhistas.
    
    Args:
        custo_hora_base (float): Valor da hora normal do trabalhador.
        horas_extras (int): Quantidade de horas extras a calcular.
        periculosidade (bool): Se há adicional de periculosidade (30%).
        insalubridade_grau (str): 'minimo' (10%), 'medio' (20%), 'maximo' (40%) ou None.
        
    Note: Insalubridade é calculada sobre o SALÁRIO MÍNIMO, não sobre o salário base.
          Aqui usaremos uma aproximação baseada no valor hora do salário mínimo (~R$ 6,50 em 2026).
    """
    
    SALARIO_MINIMO_HORA = 7.50 # Estimativa base 2026
    
    custo_total = 0
    log = []
    
    # 1. Periculosidade (30% sobre Salário Base)
    valor_periculosidade = 0
    if periculosidade:
        valor_periculosidade = custo_hora_base * 0.30
        log.append(f"Periculosidade (+30%): R$ {valor_periculosidade:.2f}/h")
        
    # 2. Insalubridade
    valor_insalubridade = 0
    if insalubridade_grau:
        fator = 0
        if insalubridade_grau == 'minimo': fator = 0.10
        elif insalubridade_grau == 'medio': fator = 0.20
        elif insalubridade_grau == 'maximo': fator = 0.40
        
        valor_insalubridade = SALARIO_MINIMO_HORA * fator
        log.append(f"Insalubridade ({insalubridade_grau}): R$ {valor_insalubridade:.2f}/h")
        
    # Hora Base com Adicionais Fixos
    hora_cheia = custo_hora_base + valor_periculosidade + valor_insalubridade
    
    # 3. Horas Extras (50% padrão dias úteis)
    # Custo da HE = Hora Cheia * 1.5
    custo_he_unit = hora_cheia * 1.5
    total_he = custo_he_unit * horas_extras
    if horas_extras > 0:
        log.append(f"Horas Extras (50%): {horas_extras}h x R$ {custo_he_unit:.2f} = R$ {total_he:.2f}")
        
    return {
        "hora_normal_com_adicionais": round(hora_cheia, 2),
        "custo_hora_extra_50": round(custo_he_unit, 2),
        "total_adicionais_variaveis": round(total_he, 2),
        "detalhamento": log
    }

if __name__ == "__main__":
    custo_pedreiro = 15.00 # Só o salário base hora
    
    # Exemplo: Obra com risco elétrico (Periculosidade) e 10 horas extras
    res = calcular_adicionais_clt(custo_pedreiro, horas_extras=10, periculosidade=True)
    
    print(f"Cálculo CLT (Base: R$ {custo_pedreiro:.2f}/h)")
    for item in res['detalhamento']:
        print(f" - {item}")
    print(f"Custo Hora Normal (ajustada): R$ {res['hora_normal_com_adicionais']:.2f}")
    print(f"Custo Hora Extra: R$ {res['custo_hora_extra_50']:.2f}")


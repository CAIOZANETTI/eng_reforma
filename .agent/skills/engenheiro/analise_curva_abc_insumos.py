"""
Skill: Análise de Curva ABC de Insumos
Descrição: Classifica os insumos de um orçamento nas curvas A (mais relevantes), B (intermediários) e C (menos relevantes) para focar a gestão de compras e negociação.
"""

import pandas as pd

def gerar_curva_abc(data):
    """
    Gera a classificação ABC a partir de uma lista de insumos.
    
    Args:
        data (list of dict): Lista contendo dicionários com 'name' (nome do insumo) e 'total_cost' (custo total).
                             Ex: [{'name': 'Cimento', 'total_cost': 5000}, ...]
    
    Returns:
        pd.DataFrame: DataFrame com as colunas 'Insumo', 'Custo Total', '% Individual', '% Acumulado', 'Classe'.
    """
    
    # Criar DataFrame
    df = pd.DataFrame(data)
    
    # Verificar colunas necessárias
    if 'name' not in df.columns or 'total_cost' not in df.columns:
        raise ValueError("O input deve conter as chaves 'name' e 'total_cost'")
    
    # Ordenar por Custo Total Decrescente
    df = df.sort_values(by='total_cost', ascending=False)
    
    # Calcular custo total do orçamento
    total_orcamento = df['total_cost'].sum()
    
    # Calcular porcentagens
    df['percent_individual'] = (df['total_cost'] / total_orcamento) * 100
    df['percent_acumulado'] = df['percent_individual'].cumsum()
    
    # Classificar A, B, C
    # Regra Clássica de Pareto 80/20 adaptada para Construção Civil:
    # A: até 50% do custo acumulado
    # B: de 50% a 80% do custo
    # C: acima de 80%
    
    def classificar(acumulado):
        if acumulado <= 50:
            return 'A'
        elif acumulado <= 80:
            return 'B'
        else:
            return 'C'
    
    df['class'] = df['percent_acumulado'].apply(classificar)
    
    # Formatação para visualização
    df_output = df[['name', 'total_cost', 'percent_individual', 'percent_acumulado', 'class']].copy()
    df_output.columns = ['Insumo', 'Custo Total (R$)', '% Impacto', '% Acumulado', 'Classe ABC']
    
    return df_output

def imprimir_relatorio_abc(df_abc):
    """Imprime um resumo gerencial da Curva ABC"""
    print("\n" + "="*60)
    print("RELATÓRIO DE CURVA ABC - GESTÃO DE CUSTOS")
    print("="*60)
    
    total = df_abc['Custo Total (R$)'].sum()
    print(f"VALOR TOTAL DO ORÇAMENTO: R$ {total:,.2f}")
    
    grupos = df_abc.groupby('Classe ABC')['Custo Total (R$)'].agg(['count', 'sum'])
    grupos['% Valor'] = (grupos['sum'] / total) * 100
    
    print("\nRESUMO POR CLASSE:")
    print("-" * 60)
    print(f"{'Classe':<10} {'Qtd Itens':<12} {'Valor Total (R$)':<20} {'% do Custo':<12}")
    print("-" * 60)
    
    for classe in ['A', 'B', 'C']:
        if classe in grupos.index:
            row = grupos.loc[classe]
            print(f"{classe:<10} {int(row['count']):<12} R$ {row['sum']:<17,.2f} {row['% Valor']:<10.1f}%")
            
    print("-" * 60)
    print("\nITENS CLASSE A (Foco de Negociação):")
    itens_a = df_abc[df_abc['Classe ABC'] == 'A']
    for idx, row in itens_a.iterrows():
        print(f" - {row['Insumo']}: R$ {row['Custo Total (R$)']:,.2f}")
    print("="*60 + "\n")

# Exemplo de uso (se rodar o script diretamente)
if __name__ == "__main__":
    exemplo_insumos = [
        {'name': 'Porcelanato 80x80', 'total_cost': 15000},
        {'name': 'Cimento CP-II', 'total_cost': 1200},
        {'name': 'Areia Média', 'total_cost': 400},
        {'name': 'Mão de Obra Pedreiro', 'total_cost': 12000},
        {'name': 'Tinta Acrílica', 'total_cost': 2500},
        {'name': 'Lâmpadas LED', 'total_cost': 300},
        {'name': 'Argamassa AC-III', 'total_cost': 1800},
        {'name': 'Tomadas e Interruptores', 'total_cost': 800},
        {'name': 'Mão de Obra Pintor', 'total_cost': 3500},
        {'name': 'Prego', 'total_cost': 50}
    ]
    
    df_abc = gerar_curva_abc(exemplo_insumos)
    imprimir_relatorio_abc(df_abc)

"""
Skill: Sanitização de DataFrames (Pandas)
Descrição: Limpa e padroniza dados brutos importados (CSV/Excel), removendo espaços extras, unificando unidades de medida e tratando caracteres especiais.
"""

import pandas as pd
import numpy as np

def sanitizar_dataframe(df):
    """
    Aplica rotinas de limpeza padrão em um DataFrame de engenharia/orçamento.
    """
    df_clean = df.copy()
    
    # 1. Remover espaços em branco de strings (Trim)
    # Aplica em todas as colunas do tipo object (string)
    for col in df_clean.select_dtypes(['object']).columns:
        df_clean[col] = df_clean[col].str.strip()
        
    # 2. Padronizar Unidades de Medida
    # Ex: 'M2', 'm2 ', 'M²' -> 'm²'
    if 'Unit' in df_clean.columns:
        mapa_unidades = {
            'M2': 'm²', 'm2': 'm²', 'MQ': 'm²',
            'M': 'm', 'm': 'm', 'ML': 'm',
            'KG': 'kg', 'Kg': 'kg',
            'UN': 'un', 'Un': 'un', 'PC': 'un',
            'H': 'h', 'h': 'h', 'HR': 'h'
        }
        df_clean['Unit'] = df_clean['Unit'].replace(mapa_unidades)
        
    # 3. Tratar Preços (String -> Float)
    # Remove 'R$', espaços e troca vírgula por ponto
    cols_preco = [col for col in df_clean.columns if 'Price' in col or 'Preço' in col or 'Custo' in col]
    
    for col in cols_preco:
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].astype(str).str.replace('R$', '', regex=False)
            df_clean[col] = df_clean[col].astype(str).str.replace(' ', '', regex=False)
            df_clean[col] = df_clean[col].astype(str).str.replace('.', '', regex=False) # Tira separador de milhar (PT-BR)
            df_clean[col] = df_clean[col].astype(str).str.replace(',', '.', regex=False) # Vírgula decimal
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
    # 4. Remover linhas totalmente vazias
    df_clean.dropna(how='all', inplace=True)
    
    return df_clean

if __name__ == "__main__":
    # Teste
    data = {
        'Name': [' Cimento ', 'Areia   '],
        'Unit': ['KG', 'm3'],
        'Price': ['R$ 50,00', '120,00']
    }
    df = pd.DataFrame(data)
    print("Original:\n", df)
    print("\nSanitizado:\n", sanitizar_dataframe(df))

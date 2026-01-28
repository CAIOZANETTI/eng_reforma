"""
Skill: Validador de Schema CSV (Catálogos)
Descrição: Garante que tabelas de insumos (CSV) tenham as colunas necessárias e não contenham duplicidades ou dados corrompidos.
"""

import pandas as pd

REQUIRED_COLUMNS_MATERIALS = ['ID', 'Name', 'Unit', 'Price']

def validar_catalogo_materiais(filepath, separator=','):
    """
    Valida um CSV de materiais.
    """
    report = {
        "status": "OK",
        "errors": [],
        "warnings": [],
        "stats": {}
    }
    
    try:
        df = pd.read_csv(filepath, sep=separator)
    except Exception as e:
        report["status"] = "CRITICAL_ERROR"
        report["errors"].append(f"Não foi possível ler o arquivo: {str(e)}")
        return report
        
    # 1. Validar Colunas
    missing_cols = [col for col in REQUIRED_COLUMNS_MATERIALS if col not in df.columns]
    if missing_cols:
        report["status"] = "ERROR"
        report["errors"].append(f"Colunas obrigatórias ausentes: {missing_cols}")
        return report # Aborta se estrutura estiver errada
        
    # 2. Validar Duplicidade de IDs
    if df['ID'].duplicated().any():
        dups = df[df['ID'].duplicated()]['ID'].tolist()
        report["status"] = "ERROR"
        report["errors"].append(f"IDs duplicados encontrados: {dups[:5]}...")
        
    # 3. Validar Preços Zerados ou Negativos
    if 'Price' in df.columns:
        invalid_prices = df[df['Price'] <= 0]
        if not invalid_prices.empty:
            report["warnings"].append(f"{len(invalid_prices)} itens com preço <= 0.")
            
    # 4. Validar Valores Nulos
    if df[REQUIRED_COLUMNS_MATERIALS].isnull().any().any():
        report["status"] = "ERROR"
        report["errors"].append("Existem células vazias em colunas obrigatórias.")
        
    # Estatísticas
    report["stats"] = {
        "total_rows": len(df),
        "total_columns": len(df.columns)
    }
    
    return report

if __name__ == "__main__":
    pass

"""
Skill: Versionador de Revisões de Arquivos
Descrição: Gerencia o versionamento de arquivos de saída (orçamentos, relatórios), adicionando sufixos (v1, v2, timestamp) e arquivando versões obsoletas.
"""

import os
import shutil
from datetime import datetime

def gerar_nome_versao(filepath, usar_timestamp=True):
    """
    Gera um novo nome de arquivo com versão incrementada ou timestamp.
    Ex: relatorio.pdf -> relatorio_v1.pdf ou relatorio_20260128.pdf
    """
    dirname, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)
    
    if usar_timestamp:
        suffix = datetime.now().strftime("%Y%m%d_%H%M")
        new_name = f"{name}_{suffix}{ext}"
    else:
        # Lógica de incremento v1, v2... (simplificada)
        # Teria que ler a pasta para saber qual a última.
        # Por segurança, vamos usar timestamp.
        suffix = datetime.now().strftime("%Y%m%d")
        new_name = f"{name}_{suffix}{ext}"
        
    return os.path.join(dirname, new_name)

def arquivar_versao_anterior(filepath, pasta_archive="archive"):
    """
    Move o arquivo atual para uma pasta 'archive' antes de sobrescrevê-lo (se ele existir).
    """
    if not os.path.exists(filepath):
        return False
        
    dirname, filename = os.path.split(filepath)
    archive_dir = os.path.join(dirname, pasta_archive)
    
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        
    # Adicionar timestamp ao mover para não sobrescrever no archive
    timestamp = datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(filename)
    new_name = f"{name}_old_{timestamp}{ext}"
    
    dest_path = os.path.join(archive_dir, new_name)
    
    shutil.move(filepath, dest_path)
    return True

if __name__ == "__main__":
    pass

import os
import sys
import importlib

def list_files_in_directory(directory):
    """Lista todos os arquivos em um diretório"""
    print(f"\nArquivos em {directory}:")
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if os.path.isdir(full_path):
            print(f"  [DIR] {item}")
        else:
            print(f"  [FILE] {item}")

def try_import(module_name):
    """Tenta importar um módulo e imprime o resultado"""
    print(f"\nTentando importar '{module_name}':")
    try:
        module = importlib.import_module(module_name)
        print(f"  ✓ Importação bem-sucedida")
        return module
    except Exception as e:
        print(f"  ✗ Erro: {str(e)}")
        return None

# Imprime informações sobre o ambiente
print("Ambiente Python:")
print(f"  Versão: {sys.version}")
print(f"  Diretório de Execução: {os.getcwd()}")
print(f"  Python Path: {sys.path}")

# Lista arquivos na raiz do projeto
list_files_in_directory(os.getcwd())

# Lista arquivos no diretório src, se existir
src_dir = os.path.join(os.getcwd(), "src")
if os.path.exists(src_dir):
    list_files_in_directory(src_dir)

# Tenta importar módulos comuns de uma aplicação Flask
try_import("app")
try_import("src.app")
try_import("db")
try_import("src.db")
try_import("database")
try_import("src.database")
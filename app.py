import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    print("="*40)
    print("Lychee")
    print("="*40)

def get_modules():
    return {
        "1": ("Preparar Tabela", "table_fix.py", "csv"),
        "2": ("Substituir Caracteres", "regex_replace.py", "csv"),
        "3": ("Verificar NCM's", "ncm_check.py", "csv"),
        "4": ("Gerar lista de NCM's validos", "ncm_valid_generator.py", "json"),
        "5": ("Altera formatacao de data", "date_fix.py", "csv"),
        "6": ("Prepara p/ importacao", "table_out.py", "csv")
    }

def show_menu():
    modules = get_modules()
    print("\nModulos disponiveis:")
    print("-" * 30)
    for key, (name, script, file_type) in modules.items():
        print(f"{key}. {name} ({file_type.upper()})")
    print("7. Abrir pasta de saida")
    print("8. Sair")
    print("-" * 30)

def get_file_input(file_type):
    while True:
        print(f"\nDigite o caminho o arquivo {file_type.upper()}:")
        print("Dica: voce pode arrastar e soltar o arquivo no terminal")
        file_path = input("Caminho do arquivo: ").strip()
        if not file_path:
            print("Digite o caminho do arquivo")
            continue
        file_path = clean_file_path(file_path)
        if not os.path.exists(file_path):
            print("O arquivo nao existe")
            print(f"Tried: {file_path}")
            continue
        if not file_path.lower().endswith(f'.{file_type}'):
            print(f"Extensao de arquivo deve ser {file_type.upper()}")
            continue
        return file_path

def clean_file_path(file_path):
    file_path = file_path.strip('\'"')
    file_path = file_path.replace('\\ ', ' ')
    
    if file_path.startswith('file://'):
        file_path = file_path[7:]
    
    if os.name == 'nt' and '/' in file_path:
        file_path = file_path.replace('/', '\\')
    
    file_path = os.path.expanduser(file_path)
    file_path = os.path.abspath(file_path)
    
    return file_path

def run_module(module_name, script_name, file_path):
    print(f"\nExecutando {module_name}...")
    print("-" * 40)
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(base_dir, "modules", script_name)
        if not os.path.exists(script_path):
            print(f"Modulo {script_name} nao encontrado")
            return
        try:
            rel_file_path = os.path.relpath(file_path, base_dir)
        except Exception:
            rel_file_path = file_path
        result = subprocess.run(
            ["python", script_path, rel_file_path],
            cwd=base_dir,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print(f"{module_name} finalizado")
        else:
            print(f"{module_name} o processo falhou: {result.returncode}")
    except subprocess.TimeoutExpired:
        print(f"{module_name} encerramento forcado")
    except KeyboardInterrupt:
        print(f"{module_name} foi interrompido pelo usuario")
    except Exception as e:
        print(f"Erro de execucao {module_name}: {str(e)}")

def open_files_folder():
    files_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
    try:
        if not os.path.exists(files_path):
            os.makedirs(files_path)
            print(f"Criado pasta para saida de arquivos: {files_path}")
        if os.name == 'nt':
            os.startfile(files_path)
        elif os.name == 'posix':
            if sys.platform == 'darwin':
                subprocess.run(['open', files_path])
            else:
                subprocess.run(['xdg-open', files_path])
        else:
            print(f"Arquivos salvos em: {files_path}")
            return
        print(f"diretorio de arquivos aberto em: {files_path}")
    except Exception as e:
        print(f"Nao foi possivel abrir o diretorio de arquivos: {str(e)}")
        print(f"Os arquivos estao salvos em: {files_path}")


def main():
    print_banner()
    modules = get_modules()
    while True:
        show_menu()
        try:
            choice = input("\nSelecione uma opcao (1-8): ").strip()
            if choice == "8":
                break
            elif choice == "7":
                open_files_folder()
                input("\nPressione enter para continuar...")
                continue
            elif choice in modules:
                module_name, script_name, file_type = modules[choice]
                file_path = get_file_input(file_type)
                run_module(module_name, script_name, file_path)
                input("\nPressione enter para continuar...")
            else:
                print("Opcao invalida, escolha entre 1-8.")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

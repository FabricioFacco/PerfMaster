import os
import shutil
import glob
import psutil
import subprocess
import win32com.client
import winshell
import pythoncom
import ctypes

ctypes.windll.kernel32.SetConsoleTitleW("PerfMaster | V1.2")

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def print_centered(text):
    terminal_width = os.get_terminal_size().columns
    print(text.center(terminal_width))

def print_welcome_message():
    clear_console()
    print_centered("╔══════════════════════════════════════╗")
    print_centered("║        PermMaster - Otimizador       ║")
    print_centered("║            para Windows 10           ║")
    print_centered("╚══════════════════════════════════════╝")
    print()
    print_centered("Make by FabricioFacco | github.com/FabricioFacco")
    print()

def print_options():
    print()
    print_centered("1. Limpar arquivos temporários")
    print_centered("2. Desfragmentar o disco")
    print_centered("3. Verificar erros no disco")
    print_centered("4. Esvaziar a lixeira")
    print_centered("5. Sair")
    print()

def get_user_choice():
    while True:
        try:
            choice = int(input("Digite o número da opção desejada: "))
            if choice in range(1, 5):
                return choice
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.\n")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.\n")

def clean_temp_files():
    print("Executando limpeza de arquivos temporários...")
    temp_folders = [
        os.environ["TEMP"],
        os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Temp"),
        os.path.join(os.environ["WINDIR"], "Temp"),
        os.path.join(os.environ["WINDIR"], "Prefetch"),
        os.path.join(os.environ["WINDIR"], "SoftwareDistribution")
    ]
    for folder in temp_folders:
        files = glob.glob(os.path.join(folder, "*"))
        for file in files:
            try:
                if os.path.isfile(file):
                    os.remove(file)
                elif os.path.isdir(file):
                    shutil.rmtree(file)
            except Exception as e:
                print(f"Erro ao limpar o arquivo/pasta: {file}")
                print(f"Erro: {str(e)}")
    print("Limpeza de arquivos temporários concluída.")
    input("Pressione Enter para continuar...")

def defragment_disk():
    print("Executando desfragmentação do disco...")
    drives = psutil.disk_partitions()
    for drive in drives:
        drive_name = drive.device
        try:
            subprocess.run(["defrag", drive_name, "/C", "/V"], capture_output=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao desfragmentar o disco {drive_name}:")
            print(f"Erro: {e.stderr}")
        else:
            print(f"Desfragmentação do disco {drive_name} concluída.")
    input("Pressione Enter para continuar...")


def check_disk_errors():
    print("Executando verificação e correção de erros no disco...")
    drives = psutil.disk_partitions()
    for drive in drives:
        drive_name = drive.device
        try:
            subprocess.run(["chkdsk", drive_name, "/F", "/R", "/X"], capture_output=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao verificar e corrigir erros no disco {drive_name}:")
            print(f"Erro: {e.stderr}")
        else:
            print(f"Verificação e correção de erros no disco {drive_name} concluídas.")
    input("Pressione Enter para continuar...")


def clean_recycle_bin():
    try:
        recycle_bin = winshell.recycle_bin()
        if recycle_bin:
            print("Esvaziando a Lixeira...")
            recycle_bin.empty(confirm=False, show_progress=False)
            print("Lixeira esvaziada.")
        else:
            print("A Lixeira está vazia.")
    except pythoncom.com_error as e:
        print(f"Erro ao acessar a lixeira: {e}")
    except Exception as e:
        print(f"Ocorreu um erro ao limpar a lixeira: {e}")
    
    input("Pressione Enter para continuar...")

def optimize(choice):
    if choice == 1:
        clean_temp_files()
    elif choice == 2:
        defragment_disk()
    elif choice == 3:
        check_disk_errors()
    elif choice == 4:
        clean_recycle_bin()
    elif choice == 5:
        print("Encerrando o otimizador...")
        input("Pressione Enter para sair.")
        exit()

def main():
    print_welcome_message()
    while True:
        print_options()
        user_choice = get_user_choice()
        optimize(user_choice)

if __name__ == "__main__":
    main()

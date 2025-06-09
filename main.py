import datetime
import os
import sys

ARQUIVO="todo.txt"

def verifica_se_git_dir() -> bool:
    arquivos = set(os.listdir())
    return '.git' in arquivos


def verifica_se_todo_em_gitignore() -> bool:
    git_dir = verifica_se_git_dir()
    if git_dir:
        with open('.gitignore') as f:
            registros_ignorados = set(f.read().split(os.linesep))
            return ARQUIVO in registros_ignorados
    return False


def inclui_em_gitignore():
    git_dir = verifica_se_git_dir()
    in_gitignore = verifica_se_todo_em_gitignore()
    if git_dir and not in_gitignore:
        with open('.gitignore', 'a') as f:
            f.write(os.linesep*2)
            f.write('#Arquivo 2do cli'+os.linesep)
            f.write(ARQUIVO)



def adicionar(info, n, tags='all'):
    yyyy = str(datetime.datetime.today().year).zfill(2)
    mm = str(datetime.datetime.today().month).zfill(2)
    dd = str(datetime.datetime.today().day).zfill(2)
    h = str(datetime.datetime.today().hour).zfill(2)
    m = str(datetime.datetime.today().minute).zfill(2)
    s = str(datetime.datetime.today().second).zfill(2)

    with open(ARQUIVO, 'a') as f:
        f.write(f'{n}--[{yyyy}-{mm}-{dd}_{h}:{m}:{s}][*{tags}*][ ]{info}\n')


def filtrar_registros(linhas, filtro=False):
    if not filtro:
        linhas_ver = [l for l in linhas]
    elif filtro == 'ld':
        linhas_ver = list(filter(lambda l: True if l.find('[ ]') == -1 else False, linhas))
    elif filtro == 'lp':
        linhas_ver = list(filter(lambda l: True if l.find('[x]') == -1 else False, linhas))

    return linhas_ver


def contar_linhas():
    linhas = None
    try:
        with open(ARQUIVO) as f:
            linhas = f.read().split('\n')
    except FileNotFoundError:
        return 0
    return len(tuple(filter(None, linhas)))


def ler(filtro=False):
    linhas = None
    no_info=False
    try:
        with open(ARQUIVO) as f:
            linhas = f.read().split('\n')
    except FileNotFoundError:
        no_info = True

    linhas_ver = filtrar_registros(linhas, filtro=filtro)
       
    print("\033[2J", end="")  # Limpa toda a tela
    print("")
    if no_info:
        print("\nSem registros...", sep='\n')
    else:
        for l in linhas_ver:
            try:
                idx = int(l.split('--')[0])+1
                print(f"{str(idx).zfill(2)}: [{l.split('*][')[1]}")
            except IndexError:
                pass
            except ValueError:
                pass

        #linhas_ver = ['['+l.split('*][')[1] for l in linhas_ver]
        #print(*linhas_ver, sep='\n')
    print("\033[H", end="")   # Coloca cursor no topo


def concluida(lista_numeros, filtro=False):
    nums = lista_numeros.strip().split(',')
    nums = map(int, filter(None, nums))
    nums = set(map(lambda x: x-1, nums))
    
    with open(ARQUIVO) as f:
        linhas = f.read().split('\n')
    
    linhas_ver = filtrar_registros(linhas, filtro=filtro)

    for i, l in enumerate(linhas_ver):
        if i in nums:
            idx = int(l.split('--')[0])
            linhas[idx] = linhas[idx].replace('[ ]', '[x]')


    with open(ARQUIVO, 'w') as f:
        f.write('\n'.join(linhas))


def nao_concluida(lista_numeros, filtro=False):
    nums = lista_numeros.strip().split(',')
    nums = map(int, filter(None, nums))
    nums = set(map(lambda x: x-1, nums))
    with open(ARQUIVO) as f:
        linhas = f.read().split('\n')

    linhas_ver = filtrar_registros(linhas, filtro=filtro)

    for i, l in enumerate(linhas_ver):
        if i in nums:
            idx = int(l.split('--')[0])
            linhas[idx] = linhas[idx].replace('[x]', '[ ]')

    with open(ARQUIVO, 'w') as f:
        f.write('\n'.join(linhas))


def sair():
    if sys.platform == 'linux': os.system('clear')
    else: os.system('cls')
    print("\nFinalizando programa...\n")
   


def main():
    if sys.platform == 'linux': os.system('clear')
    else: os.system('cls')

    inclui_em_gitignore()

    filtro=False
    n=0
    first_pass = True

    while True:
        n=contar_linhas()

        if first_pass: 
            print("")
            first_pass = False

        ler(filtro)
        try:
            cmd_args = input('$: ').split()
            if cmd_args[0] == 'a':
                info = ' '.join(filter(None, cmd_args[1:]))
                adicionar(info, n)
            elif cmd_args[0] == 'q':
                sair()
                break
            elif cmd_args[0] == 'c':
                info = ''.join(cmd_args[1:])
                concluida(info)
            elif cmd_args[0] == 'p':
                info = ''.join(cmd_args[1:])
                nao_concluida(info)
            elif cmd_args[0] == 'lc':
                filtro='ld'
            elif cmd_args[0] == 'lp':
                filtro='lp'
            elif cmd_args[0] == 'la':
                filtro=False
            else:
                continue
        except IndexError:
            pass
        except KeyboardInterrupt:
            sair()
            break



if __name__ == "__main__":
    main()

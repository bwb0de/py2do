import datetime
import os
import sys
import pyperclip

ARQUIVO="todo.txt"


class ToDo:
    def __init__(self, registro_2do: str):
        # Parser
        index, restante = registro_2do.split('--')
        timestamp, tags, restante = restante.split('][')
        timestamp, tags = timestamp[1:], tags.replace('*','').split(',')
        status, info = restante.split(']')

        self.__timestamp = timestamp
        self.__index = int(index)
        self.__tags = set(tags)
        self.__concluida = True if status == 'x' else False
        self.__info = info

    def __str__(self):
        concluida = 'x' if self.__concluida else ' '
        return f'[{concluida}]{self.__info}'

    def update(self, registro_2do: str):
        self.__init__(registro_2do)

    @property
    def concluida(self):
        return self.__concluida

    @property
    def tags(self):
        return self.__tags

    @property
    def info(self):
        return self.__info

    @property
    def index(self):
        return self.__index



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


def verifica_se_arquivo_todo_existe() -> bool:
    arquivos = set(os.listdir())
    return ARQUIVO in arquivos


def inclui_em_gitignore() -> None:
    git_dir = verifica_se_git_dir()
    in_gitignore = verifica_se_todo_em_gitignore()
    if git_dir and not in_gitignore:
        with open('.gitignore', 'a') as f:
            f.write(os.linesep*2)
            f.write('#Arquivo 2do cli'+os.linesep)
            f.write(ARQUIVO)

def cria_arquivo_todo_se_nao_existir() -> None:
    todo_existe = verifica_se_arquivo_todo_existe()
    if not todo_existe:
        with open(ARQUIVO, 'w') as f:
            pass

def carrega_registros_na_memoria() -> list:
    with open(ARQUIVO) as f:
        linhas = f.read().split(os.linesep)
        return linhas
   
def expansor_lista_numerica(lista_numerica: str) -> list:
    nums = set(filter(None, lista_numerica.strip().split(',')))
    nums_intervalo = set(filter(lambda x: bool(x.find('-')+1), nums))
    nums_isolados = nums.difference(nums_intervalo)
    nums_expandidos = []
    for npairs in nums_intervalo:
        ni, nf = npairs.split('-')
        ni, nf = int(ni), int(nf)
        nums_expandidos += [*list(range(ni, nf+1))]
    nums_convertidos = list(map(int, nums_isolados)) + nums_expandidos
    print(nums_convertidos)
    return nums_convertidos




def adicionar(info: str, n: int, tags: str='all') -> str:
    yyyy = str(datetime.datetime.today().year).zfill(2)
    mm = str(datetime.datetime.today().month).zfill(2)
    dd = str(datetime.datetime.today().day).zfill(2)
    h = str(datetime.datetime.today().hour).zfill(2)
    m = str(datetime.datetime.today().minute).zfill(2)
    s = str(datetime.datetime.today().second).zfill(2)

    with open(ARQUIVO, 'a') as f:
        registro = f'{n}--[{yyyy}-{mm}-{dd}_{h}:{m}:{s}][*{tags}*][ ]{info}{os.linesep}' 
        f.write(registro)
        return registro


def filtrar_registros(linhas: list, filtro=False) -> list:
    if not filtro:
        linhas_ver = [l for l in linhas]
    elif filtro == 'ld':
        linhas_ver = list(filter(lambda l: True if l.find('[ ]') == -1 else False, linhas))
    elif filtro == 'lp':
        linhas_ver = list(filter(lambda l: True if l.find('[x]') == -1 else False, linhas))

    return linhas_ver


def contar_linhas(linhas: list) -> int:
    return len(tuple(filter(None, linhas)))


def ler(linhas: list, filtro=False):
    no_info = not bool(linhas)

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
    print("\033[H", end="")   # Coloca cursor no topo


def concluida(lista_numeros: str, linhas: list, filtro=False) -> None:
    nums = expansor_lista_numerica(lista_numeros)
    nums = set(map(lambda x: x-1, nums))

    linhas_ver = filtrar_registros(linhas, filtro=filtro)
    info_selecionada = []

    for i, l in enumerate(linhas_ver):
        if i in nums:
            idx = int(l.split('--')[0])
            linhas[idx] = linhas[idx].replace('[ ]', '[x]')
            selecao = linhas[idx].split('[x]')[1]
            info_selecionada.append(selecao)
    
    pyperclip.copy('; '.join(info_selecionada))

    with open(ARQUIVO, 'w') as f:
        f.write('\n'.join(linhas))


def nao_concluida(lista_numeros: str, linhas: list,  filtro=False) -> None:
    nums = expansor_lista_numerica(lista_numeros)
    nums = set(map(lambda x: x-1, nums))

    linhas_ver = filtrar_registros(linhas, filtro=filtro)

    for i, l in enumerate(linhas_ver):
        if i in nums:
            idx = int(l.split('--')[0])
            linhas[idx] = linhas[idx].replace('[x]', '[ ]')

    with open(ARQUIVO, 'w') as f:
        f.write('\n'.join(linhas))


def sair() -> None:
    if sys.platform == 'linux': os.system('clear')
    else: os.system('cls')
    print("\nFinalizando programa...\n")
   


def main() -> None:
    if sys.platform == 'linux': os.system('clear')
    else: os.system('cls')

    cria_arquivo_todo_se_nao_existir()
    inclui_em_gitignore()
    linhas = carrega_registros_na_memoria()

    filtro='lp'
    n=0
    first_pass = True

    while True:
        n=contar_linhas(linhas)

        if first_pass: 
            print("")
            first_pass = False

        ler(linhas, filtro=filtro)

        try:
            cmd_args = input('$: ').split()
            if cmd_args[0] == 'a':
                info = ' '.join(filter(None, cmd_args[1:]))
                registro = adicionar(info, n)
                linhas.append(registro)
            elif cmd_args[0] == 'q':
                sair()
                break
            elif cmd_args[0] == 'c':
                info = ''.join(cmd_args[1:])
                concluida(info, linhas)
            elif cmd_args[0] == 'p':
                info = ''.join(cmd_args[1:])
                nao_concluida(info, linhas)
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

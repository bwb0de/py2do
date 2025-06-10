import datetime
import os
import sys
#import pyperclip

from typing import List

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
        if not 'all' in self.__tags: self.__tags.add('all')

    def __repr__(self):
        concluida = 'x' if self.__concluida else ' '
        return f'[{concluida}]{self.__info}'

    def update(self, registro_2do: str):
        self.__init__(registro_2do)

    def concluir(self):
        self.__concluida = True

    def reverter(self):
        self.__concluida = False

    @property
    def todo_text(self):
        return f"{self.index}--[{self.__timestamp}][*{','.join(tuple(self.tags))}*][{'x' if self.__concluida else ' '}]{self.info}"

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

    @property
    def ts(self):
        return self.__timestamp



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




def adicionar(info: str, n: int) -> ToDo:
    yyyy = str(datetime.datetime.today().year).zfill(2)
    mm = str(datetime.datetime.today().month).zfill(2)
    dd = str(datetime.datetime.today().day).zfill(2)
    h = str(datetime.datetime.today().hour).zfill(2)
    m = str(datetime.datetime.today().minute).zfill(2)
    s = str(datetime.datetime.today().second).zfill(2)

    has_tags = len(info.split('t:')) == 2
    if has_tags:
        info, tags = info.split('t:')
        tags = tags.strip().replace(' ','')
    else:
        tags = 'all'

    if not 'all' in tags: tags += ',all'

    with open(ARQUIVO, 'a') as f:
        registro = f"{os.linesep}{n}--[{yyyy}-{mm}-{dd}_{h}:{m}:{s}][*{tags}*][ ]{info}" 
        f.write(registro)
        return ToDo(registro.strip())


def filtrar_por_tag(linhas: List[ToDo], filtro_tag='all') -> list:
    tags_selecionadas = set(filtro_tag.strip().split(','))

    lista_relevancia = {}
    linhas_ver = []

    for l in linhas:
        # n => set
        n = l.tags.intersection(tags_selecionadas)
        if len(n) > 0 and lista_relevancia.get(len(n)) is None:
            lista_relevancia[len(n)]=[l]
        elif len(n) > 0 and not lista_relevancia.get(len(n)) is None:
            lista_relevancia[len(n)].append(l)

    # n => int
    for n, ls in sorted(lista_relevancia.items(), key=lambda x: x[0], reverse=True):
        linhas_ver += [*ls]

    return linhas_ver



def filtrar_por_status_conclusao(linhas: List[ToDo], filtro_status=False) -> list:
    if not filtro_status:
        linhas_ver = linhas 
    elif filtro_status == 'ld':
        linhas_ver = list(filter(lambda l: l.concluida, linhas))
    elif filtro_status == 'lp':
        linhas_ver = list(filter(lambda l: not l.concluida, linhas))
    return linhas_ver


def contar_linhas(linhas: list) -> int:
    return len(tuple(filter(None, linhas)))


def ler(linhas: List[ToDo], filtro_status=False, filtro_tag='all'):
    no_info = not bool(linhas)

    linhas_ver = filtrar_por_status_conclusao(linhas, filtro_status=filtro_status)
    linhas_ver = filtrar_por_tag(linhas_ver, filtro_tag=filtro_tag)
       
    print("\033[2J", end="")  # Limpa toda a tela
    print("")
    if no_info:
        print("\nSem registros...", sep='\n')
    else:
        for l in linhas_ver:
            try:
                i = l.index + 1
                print(f"{str(i).zfill(2)}: {l}")
            except IndexError:
                pass
            except ValueError:
                pass
    print("\033[H", end="")   # Coloca cursor no topo


def concluida(lista_numeros: str, linhas: list, filtro_status=False, filtro_tag='all') -> None:
    nums = expansor_lista_numerica(lista_numeros)
    nums = set(map(lambda x: x-1, nums))

    linhas_ver = filtrar_por_status_conclusao(linhas, filtro_status=filtro_status)
    linhas_ver = filtrar_por_tag(linhas_ver, filtro_tag=filtro_tag)
  
    info_selecionada = []

    for i, l in enumerate(linhas_ver):
        if i in nums:          
            l.concluir()
    
    #pyperclip.copy('; '.join(info_selecionada))

    linhas_atualizadas = [l.todo_text for l in linhas]

    with open(ARQUIVO, 'w') as f:
        f.write('\n'.join(linhas_atualizadas))


def nao_concluida(lista_numeros: str, linhas: list,  filtro_status=False, filtro_tag='all') -> None:
    nums = expansor_lista_numerica(lista_numeros)
    nums = set(map(lambda x: x-1, nums))

    linhas_ver = filtrar_por_status_conclusao(linhas, filtro_status=filtro_status)
    linhas_ver = filtrar_por_tag(linhas_ver, filtro_tag=filtro_tag)

    for i, l in enumerate(linhas_ver):
        if i in nums:
            l.reverter()

    linhas_atualizadas = [l.todo_text for l in linhas]

    with open(ARQUIVO, 'w') as f:
        f.write('\n'.join(linhas_atualizadas))


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
    lista_2DOs = [ToDo(l) for l in filter(None, linhas)]

    filtro_status='lp'
    filtro_tag='all'

    n=0
    first_pass = True

    while True:
        n=contar_linhas(lista_2DOs)

        if first_pass: 
            print("")
            first_pass = False

        ler(lista_2DOs, filtro_status=filtro_status, filtro_tag=filtro_tag)

        try:
            cmd_args = input('$: ').split()
            if cmd_args[0] == 'a':
                info = ' '.join(filter(None, cmd_args[1:]))
                registro = adicionar(info, n)
                lista_2DOs.append(registro)
            elif cmd_args[0] == 'q':
                sair()
                break
            elif cmd_args[0] == 'c':
                info = ''.join(cmd_args[1:])
                concluida(info, lista_2DOs)
            elif cmd_args[0] == 'p':
                info = ''.join(cmd_args[1:])
                nao_concluida(info, lista_2DOs)
            elif cmd_args[0] == 'lc':
                filtro_status='ld'
            elif cmd_args[0] == 'lp':
                filtro_status='lp'
            elif cmd_args[0] == 'la':
                filtro_status=False
            elif cmd_args[0] == 'lt':
                info = ''.join(cmd_args[1:]).strip()
                filtro_tag=info
            else:
                continue
        except IndexError:
            pass
        except KeyboardInterrupt:
            sair()
            break



if __name__ == "__main__":
    main()

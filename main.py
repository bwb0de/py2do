import os
import sys

from procedures import *

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

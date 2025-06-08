import datetime
import os

arquivo="todo.txt"


def adicionar(info, tags='all'):
    yyyy = str(datetime.datetime.today().year).zfill(2)
    mm = str(datetime.datetime.today().month).zfill(2)
    dd = str(datetime.datetime.today().day).zfill(2)
    h = str(datetime.datetime.today().hour).zfill(2)
    m = str(datetime.datetime.today().minute).zfill(2)
    s = str(datetime.datetime.today().second).zfill(2)

    with open(arquivo, 'a') as f:
        f.write(f'[{yyyy}-{mm}-{dd}_{h}:{m}:{s}][*{tags}*][ ]{info}\n')



def ler():
    linhas = None
    with open(arquivo) as f:
        linhas = f.read().split('\n')
    
    linhas_ver = [l for l in linhas]
        
    print("\033[2J", end="")  # Limpa toda a tela
    print("")
    print(*linhas_ver, sep='\n')
    print("\033[H", end="")   # Coloca cursor no topo




def main():
    os.system('cls')
    while True:
        cmd_args = input('$: ').split()
        
        try:
            if cmd_args[0] == 'a':
                info = ' '.join(cmd_args[1:])
                adicionar(info)
            else:
                continue
        except:
            pass





if __name__ == "__main__":
    main()

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



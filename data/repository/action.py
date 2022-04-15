from .components import ComponentBase
from .regmodule import regmodule

class ActionManager(ComponentBase, regmodule):
    pass 

class Action():

    __manager = ActionManager()

    def __init__(self, name: str):
        self.name = name

    def register(self):
        self.__manager.register(self)


    def execute(self, *args, **kwargs):
        # execute action
        pass


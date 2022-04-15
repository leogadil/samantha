from data.repository.action import Action

class test(Action):

    def __init__(self):
        super().__init__("test")
        self.register()
        
    def execute(self, *args, **kwargs):
        print("test123123123123123")
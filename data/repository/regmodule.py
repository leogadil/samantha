

class regmodule:

    __subscribed = {}

    def register(self, cls):
        print(f'Registering "{cls.name}" in {self.__class__.__name__}')
        self.__subscribed[cls.name] = cls

    def deregister(self, cls):
        print(f'Deregistering "{cls.name}" in {self.__class__.__name__}')
        del self.__subscribed[cls.name]

    @classmethod
    def get_subscribed(cls):
        return cls.__subscribed
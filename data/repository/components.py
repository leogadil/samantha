

class ComponentBase:

    __components = {}

    def get_name(self) -> str:
        return self.__class__.__name__

    @classmethod
    def get_component(cls, name: str) -> 'ComponentBase':
        try:
            component = cls.__components[name]
        except KeyError:
            print(f'Component {name} not found')
            return cls

        return component

    @property
    def components(self) -> dict:
        return self.__components

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.__components[cls.__name__] = cls

    

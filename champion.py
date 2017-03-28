from modifier import Modifier

champions = {}


class Champion(Modifier):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        champions[cls.__name__] = cls
    pass


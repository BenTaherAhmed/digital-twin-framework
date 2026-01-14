class Component:
    def __init__(self, name: str):
        self.name = name

    def build(self, engine):
        """
        Register processes inside the engine
        """
        raise NotImplementedError

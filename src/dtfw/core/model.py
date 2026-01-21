class Model:
    def __init__(self, engine):
        self.engine = engine
        self.components = []

    def add(self, component):
        self.components.append(component)

    def build(self):
        for c in self.components:
            c.build(self.engine)

class Module:
    name: str
    description: str
    action = ()

    def __init__(self, name: str, description: str, action) -> None:
        self.name = name
        self.description = description
        self.action = action
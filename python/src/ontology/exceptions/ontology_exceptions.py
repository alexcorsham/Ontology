class OntologyException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidEdgeTypeException(OntologyException):
    pass

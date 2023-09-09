import random

class node:
    class Input:
        def __init__(self, _type:typing.Type, name:str = None) -> None:
            self._type = _type
            self.name = name

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type}, {self.name})'

    class Constant:
        def __init__(self, _type:typing.Type, name:str = None) -> None:
            self._type = _type
            self.name = name

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type}, {self.name})'

    class operator:
        class NAND:
            def __init__(self, *args) -> None:
                self.args = args
        
            def __repr__(self) -> str:
                return f'node.operator.{self.__class__.__name__}'
            
            
import random, typing, json

class node:
    class _val:
        def __init__(self, value) -> None:
            self.value = value

        def __repr__(self) -> str:
            return f'Value({self.value})'
        
    class Input:
        def __init__(self, _type:typing.Type, name:typing.Union[str, int] = None) -> None:
            self._type = _type
            self.name = name

        def __call__(self, val:typing.Any) -> '_val':
            if not isinstance(val, self._type):
                raise TypeError
            
            return node._val(val)

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type.__name__}, {self.name})'

    class Constant:
        def __init__(self, _type:typing.Type, name:typing.Union[str, int] = None) -> None:
            self._type = _type
            self.name = name

        def __call__(self, val:typing.Any) -> '_val':
            if not isinstance(val, self._type):
                raise TypeError
            
            return node._val(val)

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type.__name__}, {self.name})'

    class Output:
        def __init__(self, _type:typing.Type, name:typing.Union[int, float], _input:int) -> None:
            self._type = _type
            self.name = name
            self.input = _input

        def __call__(self, val:typing.Any) -> '_val':
            if not isinstance(val, self._type):
                raise TypeError
            
            return node._val(val)

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type.__name__}, {self.name})'

    class operator:
        class NAND:
            def __init__(self, name:typing.Union[str, int], inputs:typing.List = []) -> None:
                self.name = name
                self.inputs = inputs
        
            def __repr__(self) -> str:
                return f'node.operator.{self.__class__.__name__}({self.name}, inputs={self.inputs})'

class Genotype:
    def __init__(self, **kwargs:dict) -> None:
        self.kwargs = kwargs
    
    def __repr__(self) -> str:
        return json.dumps({a:[*map(repr, b)] for a, b in self.kwargs.items()}, indent=4)


if __name__ == '__main__':
    g = Genotype(
        inputs = [
            node.Input(int, 0),
            node.Input(int, 1),
            node.Input(int, 2)
        ],
        constants = [
            node.Constant(int, 3),
            node.Constant(int, 4)
        ],
        gates = [
            node.operator.NAND(5, inputs = [0, 1]),
            node.operator.NAND(6, inputs = [2, 3]),
            node.operator.NAND(7, inputs = [5, 1]),
            node.operator.NAND(8, inputs = [2, 4]),
            node.operator.NAND(9, inputs = [7, 7]),
            node.operator.NAND(10, inputs = [7, 8])
        ],
        outputs = [node.Output(int, 11, 10)]
    )
            
    print(g)
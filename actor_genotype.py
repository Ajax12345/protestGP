import random, typing

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
        def __init__(self, _type:typing.Type, name:typing.Union[str, int] = None) -> None:
            self._type = _type
            self.name = name

        def __call__(self, val:typing.Any) -> '_val':
            if not isinstance(val, self._type):
                raise TypeError
            
            return node._val(val)

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type.__name__}, {self.name})'

    class operator:
        class NAND:
            def __init__(self, name:typing.Union[str, int] = None, input_num:int, inputs:typing.List) -> None:
                self.name = name
                self.input_num = input_num
                self.inputs = inputs
        
            def __repr__(self) -> str:
                return f'node.operator.{self.__class__.__name__}({self.name})'

class Genotype:
    def __init__(self, **kwargs:dict) -> None:
        pass


if __name__ == '__main__':
    g = Genotype(

    )
            

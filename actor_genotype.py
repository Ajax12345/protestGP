import random, typing, json
import collections

class node:
    class Input:
        def __init__(self, _type:typing.Type, name:typing.Union[str, int], value:typing.Any = None) -> None:
            self._type = _type
            self.name = name
            self.value = None if value is None else self(value)

        def __call__(self, val:typing.Any) -> typing.Any:
            if not isinstance(val, self._type):
                raise TypeError
            
            return val

        def set_value(self, value) -> None:
            self.value = self(value)

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type.__name__}, {self.name})'

    class Constant:
        def __init__(self, _type:typing.Type, name:typing.Union[str, int], value:typing.Any = None) -> None:
            self._type = _type
            self.name = name
            self.value = None if value is None else self(value)

        def set_value(self, value) -> None:
            self.value = self(value)

        def __call__(self, val:typing.Any) -> typing.Any:
            if not isinstance(val, self._type):
                raise TypeError
            
            return val

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type.__name__}, {self.name})'

    class Output:
        def __init__(self, _type:typing.Type, name:typing.Union[int, float], _input:int) -> None:
            self._type = _type
            self.name = name
            self.input = _input
            self.value = None
            self.parent_path = None

        def set_value(self, value) -> None:
            self.value = self(value)

        def __call__(self, val:typing.Any) -> typing.Any:
            if not isinstance(val, self._type):
                raise TypeError
            
            return val

        def __repr__(self) -> str:
            return f'node.{self.__class__.__name__}({self._type.__name__}, {self.name})'

    class operator:
        class NAND:
            def __init__(self, name:typing.Union[str, int], inputs:typing.List = []) -> None:
                self.name = name
                self.inputs = inputs
                self.parents = []

            def __call__(self, *inputs) -> typing.Any:
                assert len(inputs) == len(self.inputs)
                return not all(inputs)
        
            def __repr__(self) -> str:
                return f'node.operator.{self.__class__.__name__}({self.name}, inputs={self.inputs}, parents={self.parents})'

class Genotype:
    def __init__(self, **kwargs:dict) -> None:
        self.kwargs = kwargs
        self.gate_bindings = {j.name:j for j in kwargs['gates']}
        self.value_bindings = None    

    def __enter__(self) -> 'Genotype':
        return

    def __exit__(self, *_) -> None:
        self.value_bindings = None
        for i in self.gate_bindings.values():
            i.parents = []

        for i in self.kwargs['inputs']:
            i.value = None


    def __call__(self, *traits) -> typing.Any:
        assert len(traits) == len(self.kwargs['inputs'])

        for val, inp in zip(traits, self.kwargs['inputs']):
            inp.set_value(val)

        self.traverse()
        return [self.value_bindings[i.input] for i in self.kwargs['outputs']]

    @property
    def complexity(self) -> int:
        if self.value_bindings is None:
            self.traverse()
        
        parent_gates = set()
        for i in self.kwargs['outputs']:
            if i.input in self.gate_bindings:
                for j in self.gate_bindings[i.input].parents:
                    parent_gates.add(j)

        print('parent gates', parent_gates)

        return len(parent_gates)


    def traverse(self) -> None:
        values = {**{i.name:i.value for i in self.kwargs['inputs']}, 
                **{i.name:i.value for i in self.kwargs['constants']}}
        
        print(values)
        seen = []
        while (queue:=[gate for gate in self.kwargs['gates'] if all(i in values for i in gate.inputs) and gate.name not in seen]):
            for gate in queue:
                seen.append(gate.name)
                values[gate.name] = gate(*[values[i] for i in gate.inputs])
                for i in gate.inputs:
                    if i in self.gate_bindings:
                        gate.parents = {*gate.parents, *self.gate_bindings[i].parents, i}
                    else:
                        gate.parents = {*gate.parents, i}
            
        self.value_bindings = values
        print(self.value_bindings)
        
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
            node.Constant(int, 3, value = 0),
            node.Constant(int, 4, value = 1)
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

    with g:     
        print(g(0, 0, 1))
        print('complexity', g.complexity)


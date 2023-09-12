import random, typing, json
import collections, networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt

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
            INPUT_NUM = 2
            def __init__(self, name:typing.Union[str, int], inputs:typing.List = []) -> None:
                self.name = name
                self.inputs = inputs
                self.parents = []
                self.layer = None

            def __call__(self, *inputs) -> typing.Any:
                assert len(inputs) == len(self.inputs)
                return not all(inputs)
        
            def __repr__(self) -> str:
                return f'node.operator.{self.__class__.__name__}({self.name}, inputs={self.inputs}, parents={self.parents})'

        class OR:
            INPUT_NUM = 2
            def __init__(self, name:typing.Union[str, int], inputs:typing.List = []) -> None:
                self.name = name
                self.inputs = inputs
                self.parents = []
                self.layer = None

            def __call__(self, *inputs) -> typing.Any:
                assert len(inputs) == len(self.inputs)
                return any(inputs)
        
            def __repr__(self) -> str:
                return f'node.operator.{self.__class__.__name__}({self.name}, inputs={self.inputs}, parents={self.parents})'

        class AND:
            INPUT_NUM = 2
            def __init__(self, name:typing.Union[str, int], inputs:typing.List = []) -> None:
                self.name = name
                self.inputs = inputs
                self.parents = []
                self.layer = None

            def __call__(self, *inputs) -> typing.Any:
                assert len(inputs) == len(self.inputs)
                return all(inputs)
        
            def __repr__(self) -> str:
                return f'node.operator.{self.__class__.__name__}({self.name}, inputs={self.inputs}, parents={self.parents})'

        class NOR:
            INPUT_NUM = 2
            def __init__(self, name:typing.Union[str, int], inputs:typing.List = []) -> None:
                self.name = name
                self.inputs = inputs
                self.parents = []
                self.layer = None

            def __call__(self, *inputs) -> typing.Any:
                assert len(inputs) == len(self.inputs)
                return not any(inputs)
        
            def __repr__(self) -> str:
                return f'node.operator.{self.__class__.__name__}({self.name}, inputs={self.inputs}, parents={self.parents})'


        class NOT:
            INPUT_NUM = 1
            def __init__(self, name:typing.Union[str, int], inputs:typing.List = []) -> None:
                self.name = name
                self.inputs = inputs
                self.parents = []
                self.layer = None

            def __call__(self, *inputs) -> typing.Any:
                assert len(inputs) == len(self.inputs)
                return not self.inputs[0]
        
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
        self.reset()

    def reset(self) -> None:
        self.value_bindings = None
        for i in self.gate_bindings.values():
            i.parents = []
            i.layer = None

        for i in self.kwargs['inputs']:
            i.value = None

    def __call__(self, *traits) -> typing.Any:
        assert len(traits) == len(self.kwargs['inputs'])

        for val, inp in zip(traits, self.kwargs['inputs']):
            inp.set_value(val)

        self.traverse()
        return [self.value_bindings[i.input] for i in self.kwargs['outputs']]

    def render(self, by_layer:bool = False) -> None:
        G, labels = nx.DiGraph(), {}
        for i in self.kwargs['inputs']:
            G.add_node(i.name, layer = 1)
            labels[i.name] = f'Input({i.name})'
        
        for i in self.kwargs['constants']:
            G.add_node(i.name, layer = 1)
            labels[i.name] = f'Constant({i.name})'

        values = {**{i.name:i.value for i in self.kwargs['inputs']}, 
                **{i.name:i.value for i in self.kwargs['constants']}}
        
        seen, layer = [], 2
        while (queue:=[gate for gate in self.kwargs['gates'] if all(i in values for i in gate.inputs) and gate.name not in seen]):
            for gate in queue:
                G.add_node(gate.name, layer = layer)
                labels[gate.name] = f'{gate.__class__.__name__}({gate.name},l={gate.layer})'
                seen.append(gate.name)
                values[gate.name] = gate(*[values[i] for i in gate.inputs])
                for i in gate.inputs:
                    G.add_edge(i, gate.name)

            layer += 1

        for i in self.kwargs['outputs']:
            G.add_node(i.name, layer = layer)
            labels[i.name] = f'Output({i.name})'
            G.add_edge(i.input, i.name)
        
        write_dot(G, 'test.dot')
        if by_layer:
            pos = nx.multipartite_layout(G, subset_key="layer")
        
        else:
            pos = graphviz_layout(G, prog='dot')

        nx.draw(G, pos, labels = labels, with_labels = True, arrows = True, node_shape = 's')
        plt.show()

    @property
    def complexity(self) -> int:
        if self.value_bindings is None:
            self.traverse()
        
        parent_gates = set()
        for i in self.kwargs['outputs']:
            if i.input in self.gate_bindings:
                for j in self.gate_bindings[i.input].parents:
                    parent_gates.add(j)
            
            parent_gates.add(i.input)

        #print('parent gates', parent_gates)

        return len(parent_gates - {i.name for i in self.kwargs['constants']})

    def mutate(self, prob:float = 0.5,
            gates = [node.operator.NAND, node.operator.AND, 
                node.operator.OR, node.operator.NOR]) -> None:
        """
        mutation options:
            - add a new gate (1)
            - remove an existing gate (2)
            - change the origin of an existing input (rewire edge) (3)
            - update gate type (4)
        """
        if random.random() >= 1 - prob:
            print('mutating!!!')
            with self:
                if self.value_bindings is None:
                    self.traverse()

                choices = [1]+[2, 3, 4]*bool(self.gate_bindings)
  
                if (mutation:=random.choice(choices)) == 1:
                    #ADD NEW GATE
                    print('ADDING NEW GATE')
                    _gate = random.choice(gates)
                    gate = _gate(max([*self.value_bindings]+[i.name for i in self.kwargs['outputs']]) + 1, inputs = random.sample([*self.value_bindings], _gate.INPUT_NUM))
                    #print('chosen gate', gate)
                    parents, max_depth = set(), 1
                    for i in gate.inputs:
                        if i in self.gate_bindings:
                            max_depth = max(max_depth, self.gate_bindings[i].layer)
                            for j in self.gate_bindings[i].parents:
                                parents.add(j)

                        parents.add(i)

                    #print('parents', parents)
                    #print('max_depth', max_depth)

                    if (child_options:=[self.gate_bindings[i] for i in {*self.value_bindings} - parents if i in self.gate_bindings and self.gate_bindings[i].layer > max_depth]):
                        child = random.choice(child_options)
                        child.inputs[random.choice(range(len(child.inputs)))] = gate.name
                        #print('new child chosen', child)

                    else:
                        #print('rewiring output instead')
                        output = random.choice(self.kwargs['outputs'])
                        output.input = gate.name

                    self.gate_bindings[gate.name] = gate
                    self.kwargs['gates'].append(gate)

                elif mutation == 2:
                    #REMOVE EXISTING GATE
                    print('REMOVING EXISTING GATE')
                    gate = self.gate_bindings[random.choice([*self.gate_bindings])]
                    #print('removing gate', gate)
                    for i in self.gate_bindings:
                        if gate.name in self.gate_bindings[i].inputs:
                            #print('updating gate', self.gate_bindings[i])
                            for x, a in enumerate(self.gate_bindings[i].inputs):
                                if a == gate.name:
                                    self.gate_bindings[i].inputs[x] = random.choice(gate.inputs)
                            
                            #print('updated gate', self.gate_bindings[i])
                    
                    for i in self.kwargs['outputs']:
                        if i.input == gate.name:
                            i.input = random.choice(gate.inputs)
                            #print('updated output', i)

                    del self.gate_bindings[gate.name]
                    self.kwargs['gates'] = [i for i in self.kwargs['gates'] if i.name != gate.name]
        
                elif mutation == 3:
                    #REWIRING EDGES
                    print("REWIRING EDGES")
                    for i in self.gate_bindings:
                        parents = [j.name for j in self.kwargs['inputs']] + \
                            [j.name for j in self.kwargs['constants']] + \
                            [self.gate_bindings[j].name for j in self.gate_bindings if self.gate_bindings[j].layer < self.gate_bindings[i].layer]
                        
                        for x, a in enumerate(self.gate_bindings[i].inputs):
                            if random.random() >= 1 - 0.1:
                                #print('mutating gate connection', self.gate_bindings[i])
                                self.gate_bindings[i].inputs[x] = random.choice(parents)
                                #print('after rewiring', self.gate_bindings[i])

                elif mutation == 4:
                    #UPDATE GATE TYPE
                    print('UPDATING GATE TYPE')
                    gate = self.gate_bindings[random.choice([*self.gate_bindings])]
                    new_gate = random.choice([i for i in gates if not isinstance(gate, i)])(gate.name, inputs = gate.inputs)
                    #print('gate to be updated', gate, new_gate.__class__.__name__)
                    self.gate_bindings[gate.name] = new_gate
                    self.kwargs['gates'] = [i if i.name != new_gate.name else new_gate for i in self.kwargs['gates']]
                    

    def traverse(self) -> None:
        values = {**{i.name:i.value for i in self.kwargs['inputs']}, 
                **{i.name:i.value for i in self.kwargs['constants']}}
        
        #print(values)
        seen, layer = [], 1
        while (queue:=[gate for gate in self.kwargs['gates'] if all(i in values for i in gate.inputs) and gate.name not in seen]):
            for gate in queue:
                seen.append(gate.name)
                values[gate.name] = gate(*[values[i] for i in gate.inputs])
                for i in gate.inputs:
                    if i in self.gate_bindings:
                        gate.parents = {*gate.parents, *self.gate_bindings[i].parents, i}
                    else:
                        gate.parents = {*gate.parents, i}

                    gate.layer = layer
            
            layer += 1
            
        self.value_bindings = values
        #print(self.value_bindings)
        
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
    
    '''
    for a, b in [([0, 0, 0], False), ([0, 0, 1], False), ([0, 1, 0], True), ([0, 1, 1], False), ([1, 0, 0], True), ([1, 0, 1], True), ([1, 1, 0], True), ([1, 1, 1], True)]:
        with g:
            assert g(*a[::-1]) == [b]  
    '''  
    g.mutate()
    g.mutate()
    g.mutate()
    print(g.complexity)
    g.render()
    
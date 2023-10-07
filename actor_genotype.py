import random, typing, json, copy
import collections, networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt, itertools

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
            return f'node.{self.__class__.__name__}({self._type.__name__}, {self.name}, input={self.input})'

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

    def mutate(self, choice:typing.Union[None, int] = None,
            gates = [node.operator.NAND, node.operator.AND, 
                node.operator.OR, node.operator.NOR]) -> None:
        """
        mutation options:
            - add a new gate (1)
            - remove an existing gate (2)
            - change the origin of an existing input (rewire edge) (3)
            - update gate type (4)
        """
        #if random.random() >= 1 - prob:
            #print('mutating!!!')
        with self:
            if self.value_bindings is None:
                self.traverse()

            choices = [1]+[2, 3, 4]*bool(self.gate_bindings)
            if choice is not None:
                choices = [choice]

            if (mutation:=random.choice(choices)) == 1:
                #ADD NEW GATE
                #print('ADDING NEW GATE')
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
                #print('REMOVING EXISTING GATE')
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
                #print("REWIRING EDGES")
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
                #print('UPDATING GATE TYPE')
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

    @classmethod
    def random_genotype_m1(cls, inputs:int, constants:int, depth:int, outputs:int, levels_back:int = 1) -> 'Genotype':
        I = itertools.count(0)
        inp = [node.Input(int, next(I)) for _ in range(inputs)]
        constants = [node.Constant(int, next(I), value = 0) for _ in range(constants)]
        gates, levels = [], [inp+constants]
        for _ in range(depth):
            new_level, possible_parents = [], [j for k in levels[-1*levels_back:] for j in k]
            for _ in range(inputs):
                _gate = random.choice([node.operator.NAND, node.operator.AND, 
                    node.operator.OR, node.operator.NOR])

                new_gate = _gate(next(I), inputs = [i.name for i in random.sample(possible_parents, 2)])
                new_level.append(new_gate)
                gates.append(new_gate)

            levels.append(new_level)

        return cls(
            inputs = inp,
            constants = constants,
            gates = gates,
            outputs = [node.Output(int, next(I), i.name) for i in random.sample(levels[-1], outputs)]
        )


    @classmethod
    def random_genotype(cls, inputs:int, constants:int, depth:int, outputs:int = 1) -> 'Genotype':
        I = itertools.count(0)
        inp = [node.Input(int, next(I)) for _ in range(inputs)]
        constants = [node.Constant(int, next(I), value = 0) for _ in range(constants)]
        all_nodes = [i.name for i in inp] + [i.name for i in constants]
        gates, all_parents = [], collections.defaultdict(set)
        last_level = all_nodes
        for j in range(depth):
            level_gates = []
            for _ in range(len(last_level) - 1):
                _gate = random.choice([node.operator.NAND, node.operator.AND, 
                    node.operator.OR, node.operator.NOR])
                
                _inputs = []
                for _ in range(2):
                    while (input_node:=(random.choice(last_level) if random.random() >= 0.5 - j*0.5/depth else random.choice(all_nodes))) in _inputs:
                        pass
                    
                    _inputs.append(input_node)

                level_gates.append(_gate(gate_id:=next(I), inputs = _inputs))
                
                for _i in _inputs:
                    all_parents[gate_id].add(_i)
                    for p_i in all_parents.get(_i, []):
                        all_parents[gate_id].add(p_i)
                        
            if j:
                all_nodes.extend(last_level)
            
            last_level = [i.name for i in level_gates]
            gates.extend(level_gates)
        
        random.shuffle(last_level)
        inactive = [i for i in all_parents if all(i not in all_parents[j] for j in last_level) and i not in last_level]
        random.shuffle(inactive)
        remainder = [i for i in all_parents if i not in last_level + inactive]
        random.shuffle(remainder)
        all_output_options = last_level + inactive + remainder
        #print(all_output_options)
        return cls(
            inputs = inp,
            constants = constants,
            gates = gates,
            outputs = [node.Output(int, next(I), i) for i in all_output_options[:outputs]]
        )
        
    def __repr__(self) -> str:
        return json.dumps({a:[*map(repr, b)] for a, b in self.kwargs.items()}, indent=4)


if __name__ == '__main__':
    def DEFAULT_GENOTYPE_1():
        return Genotype(
            inputs = [
                node.Input(int, 0),
                node.Input(int, 1),
                node.Input(int, 2),
                node.Input(int, 3)
            ],
            constants = [
                node.Constant(int, 4, 1),
                node.Constant(int, 5, 0)
            ],
            gates = [
                node.operator.NOR(6, inputs=[3, 4]),
                node.operator.AND(7, inputs=[0, 3]),
                node.operator.NAND(8, inputs=[2, 2]),
                node.operator.OR(9, inputs=[2, 2]),
                node.operator.NAND(10, inputs=[4, 2]),
                node.operator.AND(11, inputs=[8, 6]),
                node.operator.NAND(12, inputs=[1, 10]),
                node.operator.NOR(13, inputs=[5, 9]),
                node.operator.NOR(14, inputs=[9, 7]),
                node.operator.AND(15, inputs=[11, 4]),
                node.operator.NAND(16, inputs=[14, 12]),
                node.operator.OR(17, inputs=[12, 14]),
                node.operator.OR(18, inputs=[17, 15]),
                node.operator.NOR(19, inputs=[17, 16])
            ],
            outputs = [
                node.Output(int, 20, 18)
            ]
        )

    def test_mutation_effect(G):
        complexity_changes = collections.defaultdict(list)
        for i in range(1,5):
            for _ in range(1000):
                g = copy.deepcopy(G)
                c1 = g.complexity
                g.mutate(i)
                c2 = g.complexity
                complexity_changes[i].append(c2 - c1)
                #print(g.complexity)

        #print(complexity_changes)

        plt.bar(['Add node', 'Remove node', 'Rewire', 'Update'], [sum(b)/len(b) for b in complexity_changes.values()])
        plt.show()

    def test_mutation_over_random(method, *args) -> None:
        complexity_changes = collections.defaultdict(list)
        for I in range(100):
            G = method(*args)
            for i in range(1,5):
                for _ in range(1000):
                    g = copy.deepcopy(G)
                    c1 = g.complexity
                    g.mutate(i)
                    c2 = g.complexity
                    complexity_changes[i].append(c2 - c1)
            #print(I)

        plt.bar(['Add node', 'Remove node', 'Rewire', 'Update'], [sum(b)/len(b) for b in complexity_changes.values()])
        plt.show()
    
    
    #test_mutation_over_random(Genotype.random_genotype, 5, 2, 5, 1)
    #test_mutation_over_random(Genotype.random_genotype, 5, 2, 5, 4)
    #test_mutation_over_random(Genotype.random_genotype_m1, 4, 0, 4, 4, 1)
    
    
    test_mutation_effect(Genotype.random_genotype(5, 2, 5, 1))
    test_mutation_effect(DEFAULT_GENOTYPE_1())
    test_mutation_effect(Genotype.random_genotype(5, 2, 5, 4))
    test_mutation_effect(Genotype.random_genotype_m1(5, 2, 5, 4, 1))
    
    
    #g = Genotype.random_genotype_m1(4, 0, 4, 4, 1)
    #g.mutate(4)
    #g.render()
    
    
    #test_block_layers()

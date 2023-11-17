import random, typing, json, copy
import collections, networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt, itertools
import functools

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

def VALIDATE_GENOTYPE(max_attempts = 5) -> typing.Callable:
    def main_wrapper(_f:typing.Callable):
        @functools.wraps(_f)
        def random_genotype(cls, *args:typing.Tuple[int]) -> 'Genotype':
            r_genotype, counter = _f(cls, *args), -1
            while any(all(i.name not in j.inputs for j in r_genotype.kwargs['gates']) for i in r_genotype.kwargs['inputs']) and (counter:=counter + 1) < max_attempts:
                r_genotype = _f(cls, *args)
            
            return r_genotype
        
        return random_genotype
    
    return main_wrapper

class Genotype:
    def __init__(self, **kwargs:dict) -> None:
        self.kwargs = kwargs
        self.gate_bindings = {j.name:j for j in kwargs['gates']}
        self.value_bindings = None    

    @property
    def levels_back(self) -> int:
        return self.kwargs.get('params', {}).get('levels_back')

    @levels_back.setter
    def levels_back(self, l_b:int) -> None:
        self.kwargs['params']['levels_back'] = l_b

    @property
    def depth(self) -> int:
        return self.kwargs.get('params', {}).get('depth')

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


        return len(parent_gates - {i.name for i in self.kwargs['constants']})


    @classmethod
    def parents_and_levels(cls, G:'Genotype') -> dict:
        parents = collections.defaultdict(set)
        levels = collections.defaultdict(list)
        if G.value_bindings is not None:
            levels[1] = [i.name for i in G.kwargs['inputs']] + [i.name for i in G.kwargs['constants']]
            for gate in G.kwargs['gates']:
                for i in gate.parents:
                    parents[gate.name].add(i)
                levels[gate.layer].append(gate.name)

            return parents, levels

        levels[1] = [i.name for i in G.kwargs['inputs']] + [i.name for i in G.kwargs['constants']]
        all_seen_nodes, level_count = [*levels[1]], 2
        while (queue:=[i for i in G.kwargs['gates'] if i.name not in all_seen_nodes and all(j in all_seen_nodes for j in i.inputs)]):
            for gate in queue:
                levels[level_count].append(gate.name)
                all_seen_nodes.append(gate.name)
                for i in gate.inputs:
                    parents[gate.name].add(i)
                    for j in parents.get(i, []):
                        parents[gate.name].add(j)

            level_count += 1

        return parents, levels

    @classmethod
    def g_complexity(cls, G:'Genotype') -> int:
        parents, levels = cls.parents_and_levels(G)
        vals = {j for i in G.kwargs['outputs'] for j in [i.input, *parents[i.input]]}
        return len(vals - {i.name for i in G.kwargs['constants']})

    @classmethod
    def activate_node(cls, G:'Genotype') -> 'Genotype':
        parents, levels = cls.parents_and_levels(G)
        node_levels = {j:a for a, b in levels.items() for j in b}
        active = {j for i in G.kwargs['outputs'] for j in [i.input, *parents.get(i.input, [])]}
        active = {i for i in active if not any(j.name == i for j in G.kwargs['inputs'])}
        inactive = {j for a, b in parents.items() for j in [a, *b] if max(levels) != node_levels[j] and min(levels) != node_levels[j]} - active
        if not inactive:
            #print('no inactive nodes, creating node')
            _gate = random.choice([node.operator.NAND, node.operator.AND, 
                node.operator.OR, node.operator.NOR])
            n_g_ID = max(max(i.name for i in G.kwargs['inputs']),
                        max([i.name for i in G.kwargs['constants']]+[0]),
                        max(i.name for i in G.kwargs['gates']),
                        max(i.name for i in G.kwargs['outputs'])) + 1
            
            if not (t_l:=[i for i in levels if i != min(levels) and i != max(levels)]):
                return G

            n_g_level = random.choice(t_l)
            inputs = random.sample([a for a, b in node_levels.items() if b < n_g_level and n_g_level - b <= G.levels_back], 2)
            new_gate = _gate(n_g_ID, inputs = inputs)
            G.kwargs['gates'].append(new_gate)
            parents[n_g_ID] = {*inputs, *[j for i in inputs for j in parents.get(i, [])]}
            levels[n_g_level].append(n_g_ID)
            node_levels[n_g_ID] = n_g_level
            inactive.add(n_g_ID)

        to_activate = random.choice([*inactive])
        #print('activating this node', to_activate)
        if not (t_l:=[i for i in active if node_levels[i] > node_levels[to_activate] and node_levels[i] - node_levels[to_activate] <= G.levels_back]):
            return G

        link_to = random.choice(t_l)
        #print('linking to', link_to)
        for gate in G.kwargs['gates']:
            if gate.name == link_to:
                gate.inputs.append(to_activate)
        
        return G

    @classmethod
    def deactivate_node(cls, G:'Genotype') -> 'Genotype':
        parents, levels = cls.parents_and_levels(G)
        node_levels = {j:a for a, b in levels.items() for j in b}
        active = {j for i in G.kwargs['outputs'] for j in [i.input, *parents.get(i.input, [])]}
        active = {i for i in active if node_levels[i] != min(levels) and node_levels[i] != max(levels) and not any(k.input == i for k in G.kwargs['outputs'])}
        if active:
            to_deactivate = random.choice([*active])
            #print('deactivating this node', to_deactivate)
            for gate in G.kwargs['gates']:
                for x, a in enumerate(gate.inputs):
                    if a == to_deactivate:
                        rewire_options = {*G.gate_bindings[to_deactivate].inputs} - {*gate.inputs}
                        if not rewire_options:
                            rewire_options = {max(parents[to_deactivate])}
                        gate.inputs[x] = random.choice([*rewire_options])
                        #print('rewriting', gate.name, 'input to', gate.inputs[x])
        return G

    @classmethod
    def rewire_node(cls, G:'Genotype') -> 'Genotype':
        parents, levels = cls.parents_and_levels(G)
        node_levels = {j:a for a, b in levels.items() for j in b}
        active = {j for i in G.kwargs['outputs'] for j in [i.input, *parents.get(i.input, [])]}
        active = {i for i in active if node_levels[i] != min(levels)}
        for _ in range(10):
            to_rewire = random.choice([*active])
            c_ind = random.choice([*range(len(G.gate_bindings[to_rewire].inputs))])
            if not (s_options:=[*{a for a, b in node_levels.items() if b < node_levels[to_rewire] and node_levels[to_rewire] - b <= G.levels_back and a not in G.gate_bindings[to_rewire].inputs}]):
                continue

            #print('to rewire', to_rewire)
            new_source = random.choice(s_options)
            for gate in G.kwargs['gates']:
                if gate.name == to_rewire:
                    #print('c_ind', c_ind, 'c_ind value', gate.inputs[c_ind], 'and new_source', new_source)
                    gate.inputs[c_ind] = new_source
            break

        return G

    def mutate_v2(self, choice:typing.Union[None, int] = None, gates = [node.operator.NAND, node.operator.AND, 
                node.operator.OR, node.operator.NOR]) -> None:
    
        self.reset()
        choices = [1, 2, 3, 4] if choice is None else [choice]

        '''
        if random.random() <= 0.25:
            self.levels_back = random.choice([*range(1, self.depth)])
        '''
            
        #TODO: cut down on nuisance and noise mutations (https://jbiomedsci.biomedcentral.com/articles/10.1186/s12929-023-00959-7)
        #https://www.annualreviews.org/doi/full/10.1146/annurev.micro.57.030502.090855
        if (mutation:=random.choice(choices)) == 1:
            count = 0
            while count < 10:
                g = self.__class__.activate_node(copy.deepcopy(self))
                if self.__class__.g_complexity(g) > self.__class__.g_complexity(self):
                    #print('complexity change', self.__class__.g_complexity(self), self.__class__.g_complexity(g))
                    self.kwargs['gates'] = g.kwargs['gates']
                    self.gate_bindings = {}
                    for i in g.kwargs['gates']:
                        self.gate_bindings[i.name] = i

                    break

                count += 1

        elif mutation == 2:
            #print("REMOVE NODE")
            #when deactivating, the odds are high of strong effects, since the act of rewiring signifcantly increases the probability that the chosen parent of the targt node will have fewer nodes in its active branch
            #thus, deactivation probabilities should decrease as the number of levels increases
            g = self.__class__.deactivate_node(copy.deepcopy(self))
            #print('complexity change', self.__class__.g_complexity(self), self.__class__.g_complexity(g))
            self.kwargs['gates'] = g.kwargs['gates']
            self.gate_bindings = {}
            for i in g.kwargs['gates']:
                self.gate_bindings[i.name] = i

        elif mutation == 3:
            #print('REWIRE EDGE')
            #over 10 rewiring actions, track the change in complexity, and choose the result that has the maximum positive increase in complexity
            #if possible, choose 0 change in complexity
            #if change => exists, chose it, else, skip mutation
            original_complexity = self.__class__.g_complexity(self)
            for _ in range(10):
                g = self.__class__.rewire_node(copy.deepcopy(self))
                if (c1:=self.__class__.g_complexity(g)) >= original_complexity:
                    #print('successful rewire', original_complexity, c1)
                    self.kwargs['gates'] = g.kwargs['gates']
                    self.gate_bindings = {}
                    for i in g.kwargs['gates']:
                        self.gate_bindings[i.name] = i
                
                    break

        elif mutation == 4:
            #print('UPDATE NODE')
            gate = self.gate_bindings[random.choice([*self.gate_bindings])]
            new_gate = random.choice([i for i in gates if not isinstance(gate, i)])(gate.name, inputs = gate.inputs)
            self.gate_bindings[gate.name] = new_gate
            self.kwargs['gates'] = [i if i.name != new_gate.name else new_gate for i in self.kwargs['gates']]

        

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

        with self:
            if self.value_bindings is None:
                self.traverse()

            choices = [1]+[2, 3, 4]*bool(self.gate_bindings)
            if choice is not None:
                choices = [choice]

            if (mutation:=random.choice(choices)) == 1:
                #ADDING NEW NODE
                _gate = random.choice(gates)
                gate = _gate(max([*self.value_bindings]+[i.name for i in self.kwargs['outputs']]) + 1, inputs = random.sample([*self.value_bindings], _gate.INPUT_NUM))
                parents, max_depth = set(), 1
                for i in gate.inputs:
                    if i in self.gate_bindings:
                        max_depth = max(max_depth, self.gate_bindings[i].layer)
                        for j in self.gate_bindings[i].parents:
                            parents.add(j)

                    parents.add(i)

                if (child_options:=[self.gate_bindings[i] for i in {*self.value_bindings} - parents if i in self.gate_bindings and self.gate_bindings[i].layer > max_depth]):
                    child = random.choice(child_options)
                    child.inputs[random.choice(range(len(child.inputs)))] = gate.name

                else:
                    output = random.choice(self.kwargs['outputs'])
                    output.input = gate.name

                self.gate_bindings[gate.name] = gate
                self.kwargs['gates'].append(gate)

            elif mutation == 2:
                #REMOVING EXISTING NODE
                gate = self.gate_bindings[random.choice([*self.gate_bindings])]
                for i in self.gate_bindings:
                    if gate.name in self.gate_bindings[i].inputs:
                        for x, a in enumerate(self.gate_bindings[i].inputs):
                            if a == gate.name:
                                self.gate_bindings[i].inputs[x] = random.choice(gate.inputs)
                        
                
                for i in self.kwargs['outputs']:
                    if i.input == gate.name:
                        i.input = random.choice(gate.inputs)

                del self.gate_bindings[gate.name]
                self.kwargs['gates'] = [i for i in self.kwargs['gates'] if i.name != gate.name]
    
            elif mutation == 3:
                #REWIRING EDGE
                for i in self.gate_bindings:
                    parents = [j.name for j in self.kwargs['inputs']] + \
                        [j.name for j in self.kwargs['constants']] + \
                        [self.gate_bindings[j].name for j in self.gate_bindings if self.gate_bindings[j].layer < self.gate_bindings[i].layer]
                    
                    for x, a in enumerate(self.gate_bindings[i].inputs):
                        if random.random() >= 1 - 0.1:
                            self.gate_bindings[i].inputs[x] = random.choice(parents)

            elif mutation == 4:
                #UPDATING NODE
                gate = self.gate_bindings[random.choice([*self.gate_bindings])]
                new_gate = random.choice([i for i in gates if not isinstance(gate, i)])(gate.name, inputs = gate.inputs)
                self.gate_bindings[gate.name] = new_gate
                self.kwargs['gates'] = [i if i.name != new_gate.name else new_gate for i in self.kwargs['gates']]
                

    def traverse(self) -> None:
        values = {**{i.name:i.value for i in self.kwargs['inputs']}, 
                **{i.name:i.value for i in self.kwargs['constants']}}
        
        seen, layer = [], 2
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

    @classmethod
    @VALIDATE_GENOTYPE(max_attempts = 10)
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
            outputs = [node.Output(int, next(I), i.name) for i in random.sample(levels[-1], outputs)],
            params = {'inputs':inputs, 
                'constants':constants, 
                'depth':depth, 
                'outputs':outputs, 
                'levels_back':levels_back}
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
            outputs = [node.Output(int, next(I), i) for i in all_output_options[:outputs]],
            params = {'inputs':inputs, 
                'constants':constants, 
                'depth':depth, 
                'outputs':outputs}
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
            ],
            params = {
                'levels_back':5
            }
        )

    def DEFAULT_GENOTYPE_2():
        return Genotype(
            inputs = [
                node.Input(int, 0),
                node.Input(int, 1),
                node.Input(int, 2),
                node.Input(int, 3)
            ],
            constants = [],
            gates = [
                node.operator.NOR(4, inputs=[0, 2]),
                node.operator.AND(5, inputs=[0, 3]),
                node.operator.NAND(6, inputs=[0, 3]),
                node.operator.AND(7, inputs=[0, 1]),
                node.operator.NOR(8, inputs=[6, 4]),
                node.operator.NAND(9, inputs=[7, 5]),
                node.operator.AND(10, inputs=[5, 4]),
                node.operator.OR(11, inputs=[6, 4]),
                node.operator.NAND(12, inputs=[8, 11]),
                node.operator.NOR(13, inputs=[10, 8]),
                node.operator.NAND(14, inputs=[9, 11]),
                node.operator.OR(15, inputs=[11, 8]),
                node.operator.AND(16, inputs=[15, 12]),
                node.operator.OR(17, inputs=[13, 15]),
                node.operator.OR(18, inputs=[13, 12]),
                node.operator.NOR(19, inputs=[15, 14])
            ],
            outputs = [
                node.Output(int, 20, 16),
                node.Output(int, 21, 17),
                node.Output(int, 22, 18),
                node.Output(int, 23, 19)
            ],
            params = {
                'inputs':4,
                'constants':0,
                'depth':4,
                'outputs':4,
                'levels_back':1
            }
        )

    def DEFAULT_GENOTYPE_3():
        return Genotype(
            inputs = [
                node.Input(int, 0),
                node.Input(int, 1),
                node.Input(int, 2),
                node.Input(int, 3)
            ],
            constants = [],
            gates = [
                node.operator.NOR(4, inputs=[3, 1]),
                node.operator.AND(5, inputs=[3, 1]),
                node.operator.OR(6, inputs=[1, 0]),
                node.operator.AND(7, inputs=[1, 0]),
                node.operator.OR(8, inputs=[2, 6]),
                node.operator.NOR(9, inputs=[2, 4]),
                node.operator.NOR(10, inputs=[4, 7]),
                node.operator.NOR(11, inputs=[4, 6]),
                node.operator.NAND(12, inputs=[11, 2]),
                node.operator.NAND(13, inputs=[0, 1]),
                node.operator.OR(14, inputs=[5, 9]),
                node.operator.AND(15, inputs=[4, 6]),
                node.operator.NAND(16, inputs=[15, 9]),
                node.operator.NOR(17, inputs=[5, 14]),
                node.operator.OR(18, inputs=[8, 6]),
                node.operator.AND(19, inputs=[13, 7])
            ],
            outputs = [
                node.Output(int, 20, 16),
                node.Output(int, 21, 17)
            ],
            params = {
                'inputs':4,
                'constants':0,
                'depth':4,
                'outputs':2,
                'levels_back':3
            }
        )

    def test_mutation_effect(G, mutation_method = 'mutate'):
        complexity_changes = collections.defaultdict(list)
        import time
        t = time.time()
        for i in range(1,5):
            for _ in range(1000):
                g = copy.deepcopy(G)
                c1 = g.complexity
                getattr(g, mutation_method)(i)
                c2 = g.complexity
                complexity_changes[i].append(c2 - c1)
                #print(g.complexity)

        #print(complexity_changes)
        print('final time', time.time() - t)
        plt.bar(['Add node', 'Remove node', 'Rewire', 'Update'], [sum(b)/len(b) for b in complexity_changes.values()])
        plt.show()

    def test_mutation_over_random(method, mutation_method, *args) -> None:
        complexity_changes = collections.defaultdict(list)
        for I in range(100):
            G = method(*args)
            for i in range(1,5):
                for _ in range(1000):
                    g = copy.deepcopy(G)
                    c1 = g.complexity
                    getattr(g, mutation_method)(i)
                    c2 = g.complexity
                    complexity_changes[i].append(c2 - c1)
            print(I)

        plt.bar(['Add node', 'Remove node', 'Rewire', 'Update'], [sum(b)/len(b) for b in complexity_changes.values()])
        plt.show()

    def compute_node_addition():
        c = []
        for _ in range(100):
            g = Genotype.random_genotype_m1(4, 0, 4, 4, 1)
            C_m = {'c':0}
            for _ in range(1000):
                g.mutate_v2(C_m = C_m)

            c.append(C_m['c'])

        print(c)
        print('C_m count', sum(c)/len(c))
        #16.79
        #19.01 on random levels back adjustment
    
    
    #test_mutation_over_random(Genotype.random_genotype, 5, 2, 5, 1)
    #test_mutation_over_random(Genotype.random_genotype, 5, 2, 5, 4)
    #test_mutation_over_random(Genotype.random_genotype_m1, 'mutate_v2', 4, 0, 4, 4, 3)
    
    
    #test_mutation_effect(Genotype.random_genotype(5, 2, 5, 1), 'mutate_v2')
    #test_mutation_effect(DEFAULT_GENOTYPE_1(), 'mutate_v2')
    #test_mutation_effect(Genotype.random_genotype(5, 2, 5, 4), 'mutate_v2')
    #test_mutation_effect(Genotype.random_genotype_m1(5, 2, 5, 4, 1), 'mutate_v2')
    
    #g = DEFAULT_GENOTYPE_3()
    #g = Genotype.random_genotype_m1(6, 0, 6, 4, 3)
    #g = Genotype.random_genotype_m1(9, 0, 9, 4, 3)
    #g = DEFAULT_GENOTYPE_2()
    #g.render()
    #g.mutate_v2(choice = 1)
    #g.render()
    '''
    g = Genotype.random_genotype_m1(4, 0, 4, 4, 3)
    print(g.complexity)
    print(g)
    g.render()
    '''
    #compute_node_addition()
    g = Genotype.random_genotype_m1(4, 0, 4, 4, 1)
    g.render()

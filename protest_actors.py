import random, typing, copy
import warnings, networkx as nx
import matplotlib.pyplot as plt
from actor_genotype import Genotype, node
import statistics, collections, numpy as np
import json, datetime, itertools
from sympy.logic import POSform
from sympy import symbols
import sympy

TRAITS = [
    'empathy',
    'aggression',
    'narcissism',
    'leadership',
    'honesty',
    'resilience',
    'assertiveness',
    'persuasiveness',
    'agreeableness'
]

ALL_TRAITS = [*itertools.product(*[range(2) for _ in range(len(TRAITS))])]

assert len(ALL_TRAITS) == 512

class Actor:
    """
    Traits derived in part from https://www.annualreviews.org/doi/pdf/10.1146/annurev-polisci-051010-111659

    empathy
    aggression
    narcissism
    leadership
    honesty
    resilience
    assertiveness
    persuasiveness
    agreeableness
    """
    def __init__(self) -> None:
        self.traits = self.__class__.random_trait()
        self.genotype = self.build_genotype()
        self._outputs = {}
        self.score = 0

    def reset(self) -> 'Actor':
        self.genotype = self.build_genotype()
        self._outputs = {}
        self.score = 0
        return self

    def mutate(self, prob:float = 0.1) -> None:
        if random.random() >= 1 - prob:
            for ind in random.sample([*range(len(self.traits))], random.randint(1, 2)):
                self.traits[ind] = int(not self.traits[ind])

            self.genotype.mutate()

    def complexity(self, min_circuit:bool = False) -> int:
        if not min_circuit:
            return self.genotype.complexity

        def traverse(expr:sympy, d:dict) -> None:
            if isinstance(expr, int):
                return 

            if isinstance(expr, sympy.core.symbol.Symbol):
                d[1].add(str(expr))
                return
            
            if isinstance(expr, sympy.logic.boolalg.Not):
                d[0].append('Not')
            
            else:
                d[0].extend([type(expr).__name__ for _ in range(len(expr.args) - 1)])
            
            for i in expr.args:
                traverse(i, d)

        minterms = []
        for trait in ALL_TRAITS:
            if trait in self._outputs:
                if self._outputs[trait]:
                    minterms.append([*trait])
            
            else:
                with self.genotype:
                    if self.genotype(*trait)[0]:
                        minterms.append([*trait])

        print('in here')
        expr = POSform([*symbols(f'a:{len(TRAITS)}')], minterms, [])
        d = {1:set(), 0:[]}
        traverse(expr, d)
        return len(d[1]) + len(d[0])

    @classmethod
    def random_trait(cls) -> typing.List[int]:
        return [int(random.random() >= 1 - float(i.split(': ')[1])) for i in filter(None, cls.__doc__.split('\n')) if i.strip().lstrip()]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.traits})'


def DEFAULT_GENOTYPE():
    return Genotype(
        inputs = [
            node.Input(int, 0),
            node.Input(int, 1),
            node.Input(int, 2),
            node.Input(int, 3),
            node.Input(int, 4),
            node.Input(int, 5),
            node.Input(int, 6),
            node.Input(int, 7),
            node.Input(int, 8)
        ],
        constants = [
            node.Constant(int, 9),
            node.Constant(int, 10)
        ],
        gates = [
            node.operator.OR(11, inputs=[9, 4]),
            node.operator.OR(12, inputs=[0, 9]),
            node.operator.NAND(13, inputs=[9, 3]),
            node.operator.OR(14, inputs=[2, 1]),
            node.operator.AND(15, inputs=[5, 5]),
            node.operator.OR(16, inputs=[10, 4]),
            node.operator.NOR(17, inputs=[5, 8]),
            node.operator.OR(18, inputs=[3, 7]),
            node.operator.NAND(19, inputs=[7, 7]),
            node.operator.NOR(20, inputs=[0, 9]),
            node.operator.OR(21, inputs=[16, 12]),
            node.operator.NAND(22, inputs=[20, 5]),
            node.operator.NAND(23, inputs=[14, 16]),
            node.operator.OR(24, inputs=[11, 13]),
            node.operator.OR(25, inputs=[2, 5]),
            node.operator.NOR(26, inputs=[18, 3]),
            node.operator.NAND(27, inputs=[12, 5]),
            node.operator.OR(28, inputs=[10, 9]),
            node.operator.NAND(29, inputs=[17, 19]),
            node.operator.OR(30, inputs=[21, 27]),
            node.operator.OR(31, inputs=[18, 29]),
            node.operator.NOR(32, inputs=[28, 27]),
            node.operator.AND(33, inputs=[21, 25]),
            node.operator.NOR(34, inputs=[21, 16]),
            node.operator.AND(35, inputs=[12, 25]),
            node.operator.NAND(36, inputs=[14, 29]),
            node.operator.NAND(37, inputs=[26, 24]),
            node.operator.OR(38, inputs=[31, 8]),
            node.operator.NOR(39, inputs=[37, 24]),
            node.operator.NOR(40, inputs=[35, 34]),
            node.operator.NOR(41, inputs=[34, 33]),
            node.operator.NOR(42, inputs=[32, 32]),
            node.operator.NOR(43, inputs=[35, 33]),
            node.operator.NAND(44, inputs=[36, 31])
        ],
        outputs = [
            node.Output(int, 45)
        ]
    )


class Protestor(Actor):
    """
    empathy: 0
    aggression: 0
    narcissism: 0
    leadership: 1
    honesty: 1
    resilience: 1
    assertiveness: 1
    persuasiveness: 0
    agreeableness: 0
    """

    def build_genotype(self) -> typing.Any:
        return Genotype.random_genotype(9, 2, 8)
    

class Police(Actor):
    """
    empathy: 0
    aggression: 1
    narcissism: 1
    leadership: 1
    honesty: 0
    resilience: 0
    assertiveness: 1
    persuasiveness: 0
    agreeableness: 0
    """

    def build_genotype(self) -> typing.Any:
        return Genotype.random_genotype(9, 2, 8)

class CounterProtestor(Actor):
    """
    empathy: 0
    aggression: 1
    narcissism: 0
    leadership: 0
    honesty: 0
    resilience: 1
    assertiveness: 1
    persuasiveness: 0
    agreeableness: 0
    """

    def build_genotype(self) -> typing.Any:
        return Genotype.random_genotype(9, 2, 8)


class Public(Actor):
    """
    empathy: 1
    aggression: 0
    narcissism: 0
    leadership: 0
    honesty: 1
    resilience: 0
    assertiveness: 0
    persuasiveness: 1
    agreeableness: 1
    """

    def build_genotype(self) -> typing.Any:
        return Genotype.random_genotype(9, 2, 8)


class Environment:
    def __init__(self) -> None:
        self.agents = {}
        self.interactions = {}
        self.generation = 1
        self.generation_complexities = {}


    def run_interactions(self) -> None:
        print('-'*40)
        for (a1, a2), [agent1, agent2, matrix] in self.interactions.items():
            for actor1 in agent1.population:
                for actor2 in agent2.population:
                    [a1_decision] = actor1.genotype(*actor2.traits)
                    [a2_decision] = actor2.genotype(*actor1.traits)
                    actor1._outputs[tuple(actor2.traits)] = a1_decision
                    actor2._outputs[tuple(actor1.traits)] = a2_decision
                    a1_payout, a2_payout = matrix[a1_decision][a2_decision]
                    actor1.score += a1_payout
                    actor2.score += a2_payout
                    #print('score after', [actor1.score, actor2.score])

    def increment_generation(self) -> None:
        self.generation += 1

    def compute_complexities(self, c_func:typing.Callable = statistics.median) -> None:
        self.generation_complexities[self.generation] = {a:c_func(sorted([i.complexity() for i in b.population])) for a, b in self.agents.items()}

    def reproduction(self, control:bool = False) -> None:
        for a_name, agent in self.agents.items():
            min_score = min(i.score for i in agent.population)
            sum_fitness = sum(i.score + (abs(min_score) if min_score < 0 else 0) for i in agent.population)
            if not sum_fitness:
                return 0, a_name

            #print(a_name, [i.score for i in agent.population])
            fitness_probability = [(i.score + (abs(min_score) if min_score < 0 else 0))/sum_fitness for i in agent.population]
            new_population = []
            for _ in range(agent.size):
                if not control:
                    parent = copy.deepcopy(agent.population[np.random.choice(agent.size, p = fitness_probability)])
                else:
                    parent = copy.deepcopy(random.choice(agent.population))

                parent.mutate()
                parent.score = 0
                new_population.append(parent)

            agent.population = new_population

        return 1, None
                
    def plot_complexities(self, proc:int, cached:bool = False, suppress_plot:bool = False) -> None:
        if cached:
            with open('run_complexities.json') as f:
                self.generation_complexities = json.load(f)

        else:
            with open(f"run_complexities_{proc}_{str(datetime.datetime.now()).replace(' ', 'T').replace('.', '')}.json", 'a') as f:
                json.dump(self.generation_complexities, f)

        agent_complexities = collections.defaultdict(list)
        all_generations = []
        for generation, agents in self.generation_complexities.items():
            all_generations.append(generation)
            for agent, complexity in agents.items():
                agent_complexities[agent].append(complexity)
            

        if not suppress_plot:
            for agent, complexities in agent_complexities.items():
                plt.plot(all_generations, complexities, label = agent)
            
            plt.xlabel('Generation')
            plt.ylabel('Median complexity')
            plt.legend()
            plt.show()

    def graph(self) -> None:
        G = nx.Graph()
        for a, b in self.interactions:
            G.add_node(a)
            G.add_node(b)
            G.add_edge(a, b)
        
        nx.draw(G, with_labels = True, arrows = True)
        plt.show()

    def __enter__(self) -> 'Environment':
        return self
    
    def __exit__(self, *_) -> None:
        self.interactions = {}
        self.generation = 1
        for agent in self.agents.values():
            agent.population = [i.reset() for i in agent.population]
            agent.interactions = []

        return
    
    def agent(self, a_func:typing.Callable) -> 'Agent':
        _env_self = self
        class Agent:
            def __init__(self, a_func) -> None:
                self.name = a_func.__name__
                self.agent_details = a_func()
                self.interactions = []

            @property
            def population(self) -> typing.List['Actor']:
                return self.agent_details['population']

            @population.setter
            def population(self, new_population:typing.List['Actor']) -> None:
                self.agent_details['population'] = new_population

            @property
            def size(self) -> int:
                return self.agent_details['size']

            def __iter__(self) -> typing.Iterator:
                yield from self.population

            def interaction(self, agent:'Agent', payoff_matrix) -> None:
                self.interactions.append(agent)
                _env_self.interactions[(self.name, agent.name)] = [self, agent, payoff_matrix]
                _env_self.agents[self.name] = self
                _env_self.agents[agent.name] = agent
                 
            
            def __repr__(self) -> str:
                return f'<agent "{self.name}" pop_size={len(self.agent_details["population"])}>'

        return Agent(a_func)

if __name__ == '__main__':
    print('Protestor random trait', Protestor.random_trait())
    print('Police random trait', Police.random_trait())
    print('CounterProtestor random trait', CounterProtestor.random_trait())
    print('Public random trait', Public.random_trait())
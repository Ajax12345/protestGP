import random, typing
import warnings, networkx as nx
import matplotlib.pyplot as plt
from actor_genotype import Genotype, node

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
    empathy: 0.6
    aggression: 0.6
    narcissism: 0.5
    leadership: 0.7
    honesty: 0.5
    resilience: 0.8
    assertivness: 0.8
    persuasiveness: 0.6
    agreeableness: 0.3
    """

    def build_genotype(self) -> typing.Any:
        return Genotype.random_genotype(9, 2, 2)
    

class Police(Actor):
    """
    empathy: 0.3
    aggression: 0.85
    narcissism: 0.7
    leadership: 0.6
    honesty: 0.5
    resilience: 0.8
    assertivness: 0.9
    persuasiveness: 0.6
    agreeableness: 0.2
    """

    def build_genotype(self) -> typing.Any:
        return Genotype.random_genotype(9, 2, 2)

class CounterProtestor(Actor):
    """
    empathy: 0.4
    aggression: 0.7
    narcissism: 0.7
    leadership: 0.4
    honesty: 0.4
    resilience: 0.6
    assertivness: 0.7
    persuasiveness: 0.4
    agreeableness: 0.3
    """

    def build_genotype(self) -> typing.Any:
        return Genotype.random_genotype(9, 2, 2)


class Public(Actor):
    """
    empathy: 0.5
    aggression: 0.5
    narcissism: 0.5
    leadership: 0.5
    honesty: 0.5
    resilience: 0.5
    assertivness: 0.5
    persuasiveness: 0.5
    agreeableness: 0.5
    """

    def build_genotype(self) -> typing.Any:
        return Genotype.random_genotype(9, 2, 2)


class Environment:
    def __init__(self) -> None:
        self.agents = {}
        self.interactions = {}

    def graph(self) -> None:
        G = nx.Graph()
        for a, b in self.interactions:
            G.add_node(a)
            G.add_node(b)
            G.add_edge(a, b)
        
        nx.draw(G, with_labels = True, arrows = True)
        plt.show()
    
    def agent(self, a_func:typing.Callable) -> 'Agent':
        _env_self = self
        class Agent:
            def __init__(self, a_func) -> None:
                self.name = a_func.__name__
                self.agent_details = a_func()
                self.interactions = []

            def interaction(self, agent:'Agent', payoff_matrix) -> None:
                self.interactions.append(agent)
                _env_self.interactions[(self.name, agent.name)] = [self, agent, payoff_matrix]
            
            def __repr__(self) -> str:
                return f'<agent "{self.name}" pop_size={len(self.agent_details["population"])}>'

        agent = Agent(a_func)
        self.agents[a_func.__name__] = agent

        return agent

if __name__ == '__main__':
    print(Public.random_actor())
import random, typing
import warnings

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
        pass
    

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
        pass

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
        pass


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
        pass


class Environment:
    def __init__(self) -> None:
        self.agents = {}
        self.interactions = {}
    
    def agent(self, a_func:typing.Callable) -> typing.Any:
        _env_self = self
        class Agent:
            def __init__(self, a_func) -> None:
                self.name = a_func.__name__
                self.agent_details = a_func()
                self.interactions = []

            def __call__(self, agent:'Agent', payoff_matrix) -> None:
                self.interactions.append(agent)
                _env_self.interactions[(self.name, agent.name)] = [self, agent, payoff_matrix]
            
            def __repr__(self) -> str:
                return f'<agent "{self.name}" pop_size={len(self.agent_details["population"])}>'

        agent = Agent(a_func)
        self.agents[a_func.__name__] = agent

        return agent

if __name__ == '__main__':
    print(Public.random_actor())
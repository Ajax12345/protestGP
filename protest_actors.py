import random, typing

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
    def __init__(self, traits:typing.List[int], genotype = None) -> None:
        self.traits = traits
        self.genotype = genotype if genotype is not None else None

    @classmethod
    def random_actor(cls) -> 'Actor':
        return cls([int(random.random() >= 1 - float(i.split(': ')[1])) for i in filter(None, cls.__doc__.split('\n')) if i.strip().lstrip()])

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

class CounterProtestors(Actor):
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

if __name__ == '__main__':
    print(Public.random_actor())
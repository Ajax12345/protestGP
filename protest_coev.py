import protest_actors as pa

env = pa.Environment()

@env.agent
def Protestors():
    return {'population': [pa.Protestor() for _ in range(1000)]}

@env.agent
def Police():
    return {'population': [pa.Police() for _ in range(1000)]}

@env.agent
def CounterProtestors():
    return {'population': [pa.CounterProtestor() for _ in range(1000)]}

@env.agent
def Public():
    return {'population': [pa.Public() for _ in range(1000)]}

Protestors.interaction(Police, None)
Protestors.interaction(Public, None)
Protestors.interaction(CounterProtestors, None)
Public.interaction(CounterProtestors, None)
CounterProtestors.interaction(Police, None)


if __name__ == '__main__':
    env.graph()

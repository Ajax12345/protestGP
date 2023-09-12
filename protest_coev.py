import protest_actors as pa

env = pa.Environment()

@env.agent
def Protestors():
    return {'population': [pa.Protestor() for _ in range(1000)], 'size':1000}

@env.agent
def Police():
    return {'population': [pa.Police() for _ in range(1000)], 'size':1000}

@env.agent
def CounterProtestors():
    return {'population': [pa.CounterProtestor() for _ in range(1000)], 'size':1000}

@env.agent
def Public():
    return {'population': [pa.Public() for _ in range(1000)], 'size':1000}

Protestors.interaction(Police, [[(2, 2), (-1, 2)], [(2, 0), (0, 0)]])
Protestors.interaction(Public, [[(-1, 0), (-2, 1)], [(1, 0), (2, 2)]])
Protestors.interaction(CounterProtestors, [[(1, 1), (-1, 1)], [(1, -1), (0, 0)]])
Public.interaction(CounterProtestors, [[(0, 0), (1, 0)], [(1, -1), (1, 1)]])
CounterProtestors.interaction(Police, [[(0, 0), (-1, 1)], [(1, -1), (2, 2)]])


if __name__ == '__main__':
    #print(Protestors.agent_details['population'][0].genotype)
    print(env.interactions)

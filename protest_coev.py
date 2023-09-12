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

if __name__ == '__main__':
    print(Public)

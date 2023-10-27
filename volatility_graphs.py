import matplotlib.pylot as plt
import collections, typing, copy

def test_mutation_over_random(method:typing.Callable, mutation_method:str, *args) -> None:
    '''
    @method: the function that randomly generates a circuit
        - here, @method can be either Genotype.random_genotype or Genotype.random_genotype_m1
        - Genotype.random_genotype is the original circuit with several constant nodes and (usually) only one output
        - Genotype.random_genotype_m1 is the latest circuit with an output layer and an explicit number of levels back for the connections of each node
    
    @mutation_method: a string name of the mutation function
        - either 'mutate', which implements original set of four operators, including addition and removal
        - or 'mutate_v2', containing the latest set of mutations, where addition and removal is replaced by inactive node activation and active node deactivation
    
    @args: the parameters of the random genotype i.e the number of input nodes, output nodes, levels back, etc.
    '''
    complexity_changes = collections.defaultdict(list)
    for I in range(100): #generate 100 random circuits
        G = method(*args) #create random circuits
        for i in range(1,5): #for each possible mutation operator: 1 => 'addition/activation', 2 => 'removal/deactivation', 3 => rewiring, 4 => node function change i.e NAND to OR
            for _ in range(1000): #perform the mutation 1000 times on the original circuit 
                g = copy.deepcopy(G) #create a deepcopy of the original (the parent), so we have a clean slate each time
                c1 = g.complexity #record the complexity before mutation
                getattr(g, mutation_method)(i) #perform the mutation
                c2 = g.complexity #compute the complexity post mutation
                complexity_changes[i].append(c2 - c1) #log the total change in complexity for that specific mutation operator (1, 2, 3, or 4)
        print(I)

    #below: plot the averages for each operation
    plt.bar(['Add node', 'Remove node', 'Rewire', 'Update'], [sum(b)/len(b) for b in complexity_changes.values()])
    plt.show()
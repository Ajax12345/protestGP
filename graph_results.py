import matplotlib.pyplot as plt
import collections, json, os, math

def plot_main_complexities(folder = 'comp_matrices_mutations', min_y = None, max_y = None):
    results = collections.defaultdict(dict)
    fitness_results = collections.defaultdict(dict)
    for i in os.listdir(folder):
        if i.endswith('.json') and i.startswith('run_complexities'):
            with open(os.path.join(folder, i)) as f:
                data = json.load(f)
                for generation, actors in data.items():
                    for actor, metrics in actors.items():
                        if actor not in results[int(generation)]:
                            results[int(generation)][actor] = [float(metrics if not isinstance(metrics, dict) else metrics['complexity'])]
                        else:
                            results[int(generation)][actor].append(float(metrics if not isinstance(metrics, dict) else metrics['complexity']))

                        if isinstance(metrics, dict):
                            if actor not in fitness_results[int(generation)]:
                                fitness_results[int(generation)][actor] = [float(metrics['fitness'])]
                            else:
                                fitness_results[int(generation)][actor].append(float(metrics['fitness']))
                        
    final = collections.defaultdict(list)
    for generation, actors in results.items():
        for a, b in actors.items():
            final[a].append(sum(b)/len(b))
    
    for actor, complexities in final.items():
        plt.plot([*results], complexities, label = actor)
            
    plt.xlabel('Generation')
    plt.ylabel('Median complexity')
    plt.title('Complexity')
    plt.legend()
    min_y_lim = min(min(b) for _, b in final.items())
    max_y_lim = math.ceil(max(max(b) for _, b in final.items()))
    if min_y is not None:
        min_y_lim = max(min_y_lim, min_y)
    
    if max_y is not None:
        max_y_lim = max(max_y_lim, max_y)


    plt.ylim(min_y_lim, max_y_lim)
    plt.show()

    if fitness_results:
        final_fitness = collections.defaultdict(list)
        for generation, actors in fitness_results.items():
            for a, b in actors.items():
                final_fitness[a].append(sum(b)/len(b))
        
        for actor, fitnesses in final_fitness.items():
            plt.plot([*results], fitnesses, label = actor)
                
        plt.xlabel('Generation')
        plt.ylabel('Median complexity')
        plt.title('Fitness')
        plt.legend()
        plt.show()

    return min_y_lim, max_y_lim


if __name__ == '__main__':
    #plot_main_complexities('complexity_100_graphs')
    #plot_main_complexities('comp_control_matrices_mutations')
    #plot_main_complexities('comp_matrices_mutations')
    #plot_main_complexities('o1')
    #plot_main_complexities('o3')
    #plot_main_complexities('o7')
    '''
    y1, y2 = plot_main_complexities('o14')
    y1, y2 = plot_main_complexities('o13')
    _ = plot_main_complexities('o9')
    '''
    '''
    plot_main_complexities('o9')
    plot_main_complexities('o13')
    plot_main_complexities('o14')
    '''
    '''
    plot_main_complexities('o15')
    plot_main_complexities('o16')
    plot_main_complexities('o17')
    '''
    plot_main_complexities('o18')
    plot_main_complexities('o19')
    #_ = plot_main_complexities('o11', y1, y2)
    #plot_main_complexities('control_graphs')
    '''
    comp_matrices_mutations
        - latest run Oct 1 2023 on 1000 generation, mutations, new payoff matrices
        - fitness proportional selection
    '''
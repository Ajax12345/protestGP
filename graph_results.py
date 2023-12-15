import matplotlib.pyplot as plt
import collections, json, os, math
import numpy as np, csv

def plot_main_complexities(comp_titles, fitness_titles, comp_ax, fit_ax, c_ind, f_ind, folder = 'comp_matrices_mutations', min_y = None, max_y = None):
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
    
    complexity_table_stats = {}
    for actor, complexities in final.items():
        comp_ax.plot(_R:=[*results], complexities, label = actor)
        R = np.array(_R)
        A = np.vstack([R, np.ones(len(R))]).T
        m, c = np.linalg.lstsq(A, np.array(complexities), rcond=None)[0]
        complexity_table_stats[actor] = {'final_complexity':complexities[-1], 'max_complexity':max(complexities), 'slope':m, 'y_intercept':c}
            

    print('complexity_stats below')
    with open(os.path.join(folder, 'complexity_stats.csv'), 'a') as f:
        pass

    with open(os.path.join(folder, 'complexity_stats.csv'), 'w') as f:
        write = csv.writer(f)
        write.writerows([['actor', 'final_complexity', 'max_complexity', 'slope', 'y_intercept'], *[[a, *b.values()] for a, b in complexity_table_stats.items()]])

    
    print(json.dumps(complexity_table_stats, indent=4))
    comp_ax.set_xlabel('Generation')
    comp_ax.set_ylabel('Average complexity')
    comp_ax.title.set_text(comp_titles[c_ind])
    comp_ax.legend()
    min_y_lim = min(min(b) for _, b in final.items())
    max_y_lim = math.ceil(max(max(b) for _, b in final.items()))
    if min_y is not None:
        min_y_lim = max(min_y_lim, min_y)
    
    if max_y is not None:
        max_y_lim = max(max_y_lim, max_y)


    comp_ax.set_ylim(13, 21)
    #plt.show()

    if fitness_results:
        final_fitness = collections.defaultdict(list)
        for generation, actors in fitness_results.items():
            for a, b in actors.items():
                final_fitness[a].append(sum(b)/len(b))
        

        fitness_table_stats = {}
        for actor, fitnesses in final_fitness.items():
            fit_ax.plot(_R:=[*results], fitnesses, label = actor)
            R = np.array(_R[100:])
            A = np.vstack([R, np.ones(len(R))]).T
            m, c = np.linalg.lstsq(A, np.array(fitnesses[100:]), rcond=None)[0]
            fitness_table_stats[actor] = {'final_fitness':fitnesses[-1], 'max_fitness':max(fitnesses[100:]), 'slope':m, 'y_intercept':c}


        print('fitness_stats below')
        with open(os.path.join(folder, 'fitness_stats.csv'), 'a') as f:
            pass

        with open(os.path.join(folder, 'fitness_stats.csv'), 'w') as f:
            write = csv.writer(f)
            write.writerows([['actor', 'final_fitness', 'max_fitness', 'slope', 'y_intercept'], *[[a, *b.values()] for a, b in fitness_table_stats.items()]])

        print(json.dumps(fitness_table_stats, indent=4))

        fit_ax.set_xlabel('Generation')
        fit_ax.set_ylabel('Average fitness')
        fit_ax.title.set_text(f_titles[f_ind])
        fit_ax.set_ylim(0, 1.01)
        fit_ax.legend()
        #plt.show()

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
    fig, (ax1, ax2) = plt.subplots(1, 2,  sharey=True)
    fig, (ax11, ax21) = plt.subplots(1, 2,  sharey=True)
    
    c_titles = ['Complexity (fitness-proportionate)', 'Complexity (control)']
    f_titles = ['Fitness (fitness-proportionate)', 'Fitness (control)']
    plot_main_complexities(c_titles, f_titles, ax2, ax21, 0, 0, 'o18')
    plot_main_complexities(c_titles, f_titles, ax1, ax11, 1, 1, 'o19')
    plt.show()
    plt.show()
    #plot_main_complexities('o19')
    #_ = plot_main_complexities('o11', y1, y2)
    #plot_main_complexities('control_graphs')
    '''
    comp_matrices_mutations
        - latest run Oct 1 2023 on 1000 generation, mutations, new payoff matrices
        - fitness proportional selection
    '''
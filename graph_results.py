import matplotlib.pyplot as plt
import collections, json, os

def plot_main_complexities(folder = 'complexity_graphs'):
    results = collections.defaultdict(dict)
    for i in os.listdir(folder):
        if i.endswith('.json'):
            with open(os.path.join(folder, i)) as f:
                data = json.load(f)
                for generation, actors in data.items():
                    for actor, val in actors.items():
                        if actor not in results[int(generation)]:
                            results[int(generation)][actor] = [float(val)]
                        else:
                            results[int(generation)][actor].append(float(val))

    final = collections.defaultdict(list)
    for generation, actors in results.items():
        for a, b in actors.items():
            final[a].append(sum(b)/len(b))
    
    for actor, complexities in final.items():
        plt.plot([*results], complexities, label = actor)
            
    plt.xlabel('Generation')
    plt.ylabel('Median complexity')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    plot_main_complexities('complexity_100_graphs')
    #plot_main_complexities('control_graphs')
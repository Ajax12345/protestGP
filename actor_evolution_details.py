import json, collections
import matplotlib.pyplot as plt
import itertools, string, pandas as pd
import numpy as np, os

TRAITS = {str(list(a)):b for a, b in zip(itertools.product(*[[0, 1] for _ in range(4)]), string.ascii_uppercase)}

COLORS = {
    'Police':'orange',
    'CounterProtestors': 'red',
    'Protestors': 'blue',
    'Public': 'green'
}
def plot_stacked_bar(data, series_labels, category_labels=None, 
                     show_values=False, value_format="{}", y_label=None, 
                     colors=None, grid=True, reverse=False):
    """Plots a stacked bar chart with the data and labels provided.

    Keyword arguments:
    data            -- 2-dimensional numpy array or nested list
                       containing data for each series in rows
    series_labels   -- list of series labels (these appear in
                       the legend)
    category_labels -- list of category labels (these appear
                       on the x-axis)
    show_values     -- If True then numeric value labels will 
                       be shown on each bar
    value_format    -- Format string for numeric value labels
                       (default is "{}")
    y_label         -- Label for y-axis (str)
    colors          -- List of color labels
    grid            -- If True display grid
    reverse         -- If True reverse the order that the
                       series are displayed (left-to-right
                       or right-to-left)
    """

    ny = len(data[0])
    ind = list(range(ny))

    axes = []
    cum_size = np.zeros(ny)

    data = np.array(data)

    if reverse:
        data = np.flip(data, axis=1)
        category_labels = reversed(category_labels)

    for i, row_data in enumerate(data):
        color = colors[i] if colors is not None else None
        p = plt.bar(ind, row_data, bottom=cum_size, 
                    label=series_labels[i], color=color)
        cum_size += row_data
        if show_values:
            plt.bar_label(p, label_type='center', fmt=value_format)

    if category_labels:
        plt.xticks(ind, category_labels)

    if y_label:
        plt.ylabel(y_label)

    plt.legend()

    if grid:
        plt.grid()

def evolution_exploration() -> None:
    with open('generation_evolutions_1_2023-11-18T14:39:15689721.json') as f:
        raw_data = json.load(f)
        data = collections.defaultdict(dict)
        for a, b in raw_data['trait_actor_associations'].items():
            if a == '1':
                for trait, vals in raw_data['trait_actor_associations']['1'].items():
                    for actor, c in vals.items():
                        if actor not in data[trait]:
                            data[trait][actor] = []
                        
                        data[trait][actor].append(c)
        
        data = {a:{j:sum(k)/len(k) for j, k in b.items()} for a, b in data.items()}
        
        last = np.zeros(len(TRAITS))
        for a, b in COLORS.items():
            n_l = [data.get(j, {}).get(a, 0) for j in TRAITS]
            plt.bar([*TRAITS.values()], n_l, bottom = last, color = b, label = a)

            last += np.array(n_l)

        plt.legend()
        plt.show()
    
        '''
        plot_stacked_bar(
            [[data[j][i] for j in TRAITS] for i in COLORS], 
            [*COLORS], 
            category_labels=[*TRAITS.values()], 
            colors=[*COLORS.values()],
            y_label="count",
            grid = False
        )
        plt.show()
        '''

def merge_vals(seed:dict, d:dict) -> None:
    for a, b in d.items():
        if isinstance(b, dict):
            n_seed = seed.get(a, {})
            merge_vals(n_seed, b)
            seed[a] = n_seed
        else:
            seed[a] = seed.get(a, []) + [b]


def compute_avg(d:dict) -> None:
    for a, b in d.items():
        if isinstance(b, dict):
            compute_avg(b)
            continue
        
        d[a] = round(sum(b)/len(b))

        
def actor_decisions(folder:str) -> None:
    merged_results = {}
    for f_name in os.listdir(folder):
        if f_name.startswith('generation_evolutions'):
            with open(os.path.join(folder, f_name)) as f:
                data = json.load(f)['actor_decision_evolutions']
                merge_vals(merged_results, data)

    
    compute_avg(merged_results)

    full_counter = []
    for a in merged_results.values():
        for b in a.values():
            for c in b.values():
                full_counter.append(int(c.get('true', 0)) > int(c.get('false', 0)))

    print(sum(full_counter)/len(full_counter))
    print(json.dumps(merged_results, indent=4)[:20000])
    return merged_results

def row_result(a, b):
    return [(a/(a+b))*100, (b/(a+b))*100]

def graph_results(folder:str) -> None:
    merged_results = actor_decisions(folder)
    _generations = [*merged_results][:-1]
    generations = [*map(int, _generations)]
    pairings = [('Protestors', 'Police'), ('Protestors', 'Public'), ('Protestors', 'CounterProtestors'), ('Public', 'CounterProtestors'), ('CounterProtestors', 'Police')]
    for a1, a2 in pairings:
        print((a1, a2))
        #print(min(int(i) for i in _generations if (a1 not in merged_results[i] or a2 not in merged_results[i][a1]) or (a2 not in merged_results[i] or a1 not in merged_results[i][a2])))
        tr, fl = zip(*[row_result(merged_results[i][a1][a2].get('true', 0), merged_results[i][a1][a2].get('false', 0)) for i in _generations])
        fig, (ax1, ax2) = plt.subplots(1, 2,  sharey=True)
        ax1.plot(generations, tr, label = 'True', color = 'cadetblue')
        ax1.plot(generations, fl, label = 'False', color = 'sandybrown')
        ax1.title.set_text(a1)
        ax1.set_xlabel('Generation')
        ax1.set_ylabel('Decision Percentage')
        ax1.legend()
        tr, fl = zip(*[row_result(merged_results[i][a2][a1].get('true', 0), merged_results[i][a2][a1].get('false', 0)) for i in _generations])

        ax2.plot(generations, tr, label = 'True', color = 'cadetblue')
        ax2.plot(generations, fl, label = 'False', color = 'sandybrown')
        ax2.title.set_text(a2)
        ax2.legend()
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Decision Percentage')

        fig.suptitle(f'{a1} vs {a2}')
        plt.show()


if __name__ == '__main__':
    #actor_decisions('o18')
    graph_results('o18')
    '''
    Protestors v Police
    Protestors v CounterProtestors
    Protestors v Public
    Public v CounterProtestors
    Police v Counterprotestors


    Protestors.interaction(Police, [[(2, 1), (-1, 2)], [(2, -2), (-1, 2)]])
    Protestors.interaction(Public, [[(-2, -1), (-2, 2)], [(2, -2), (3, 3)]])
    Protestors.interaction(CounterProtestors, [[(1, 1), (-1, 2)], [(2, -1), (2, 1)]])
    Public.interaction(CounterProtestors, [[(2, 1), (0, 1)], [(-1, -1), (-1, 2)]])
    CounterProtestors.interaction(Police, [[(-1, -1), (-1, 1)], [(2, -1), (2, 2)]])

    for each relationship above, draw separate line-graphs showing average true-false outputs as different lines over the 5000 iterations
        moves['Police']['Protestors'], moves['Protestors']['Police']

    '''
import json, collections
import matplotlib.pyplot as plt
import itertools, string, pandas as pd
import numpy as np

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
    with open('generation_evolutions_1_2023-11-17T22:10:59387742.json') as f:
        raw_data = json.load(f)
        data = collections.defaultdict(dict)
        for a, b in raw_data['trait_actor_associations'].items():
            for trait, vals in b.items():
                for actor, c in vals.items():
                    if actor not in data[trait]:
                        data[trait][actor] = []
                    
                    data[trait][actor].append(c)
        
        data = {a:{j:sum(k)/len(k) for j, k in b.items()} for a, b in data.items()}
        
        last = np.zeros(len(TRAITS))
        for a, b in COLORS.items():
            n_l = [data[j][a] for j in TRAITS]
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
        
     


if __name__ == '__main__':
    evolution_exploration()
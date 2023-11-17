import json, collections


def evolution_exploration() -> None:
    with open('generation_evolutions_1_2023-11-17T16:59:25796377.json') as f:
        data = json.load(f)


if __name__ == '__main__':
    evolution_exploration()
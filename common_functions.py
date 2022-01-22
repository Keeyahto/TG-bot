def lower_list(items: list):
    types = []
    for i in range(len(items)):
        types.append(type(items[i]))
        items[i] = str(items[i]).lower()
    return [types[i](items[i]) for i in range(len(items))]


def print_dict(dct):
    for key, value in dct.items():
        print(key, ':', value)

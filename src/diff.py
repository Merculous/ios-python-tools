
def getDifferences(orig, new):
    with open(orig, 'rb') as o:
        o_data = o.read()

    with open(new, 'rb') as n:
        n_data = n.read()

    stuff = list()

    for i, n_value in enumerate(n_data):
        if n_value != o_data[i]:
            data = (hex(o_data[i]), hex(n_value), i)
            stuff.append(data)

    o_str = ''

    for x in stuff:
        tmp = x[0].split('0x')[1]  # FIXME
        o_str += tmp

        if len(o_str) == 8:
            oof = ''

test = lambda x: x+1

foo = lambda _: 2 ** _

bar = lambda a, b, c, *_, **__: [a, b, c, [x for x in _], [(y, z) for y, z in __]]
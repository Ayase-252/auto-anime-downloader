"""
Command dispatcher module
"""

import main


def dispatcher(*args):
    lookup = {
        'add': main.add,
        'update': main.update
    }
    if len(args) == 0:
        main.main()
    else:
        lookup[args[0]](*(args[1:]))

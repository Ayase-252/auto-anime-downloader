"""
Command dispatcher module
"""

import main
import manage


def dispatcher(*args):
    lookup = {
        'add': main.add,
        'update': main.update,
        'check': main.check_database,
        'manage': manage.entry,
    }
    if len(args) == 0:
        main.main()
    else:
        lookup[args[0]](*(args[1:]))

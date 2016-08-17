"""
Management System Module

This module provides user-friendly method to manage database via CLI.
"""

from manage_plugins import Add

_registed_plugins = {'add': Add}


def entry(*args):
    """
    Entry point of management system. This method handles user input.
    """
    print('Welcome to Management System')
    print('Following commands are available:')
    for key, value in _registed_plugins.items():
        print(key + ': ' + value.get_description())
    print('\nIf you have nothing to do, input exit')
    user_input = input('')
    if user_input == 'exit':
        return
    _registed_plugins[user_input].func()

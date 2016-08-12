"""
Plugin Base Class of Management System
"""


class ManagePluginBase:
    """
    Abstract base class for all plugins of management system

    attributes:
    description     Discription for command function
    """
    description = 'No description is provided for this command.'

    @classmethod
    def get_description(cls):
        return cls.description

    @classmethod
    def func(cls, *args, **kargs):
        """
        Main function is defined here. Subclass should override the method.

        error:
        NotImplementedError     Any subclass which doesn't override the method
                                raises NotImplementedError while the function
                                is called directly or indirectly
        """
        raise NotImplementedError('Command is not implemented yet.')

    @classmethod
    def __call__(cls, *args, **kargs):
        """
        Shorthand to call func
        """
        return cls.func(*args, **kargs)

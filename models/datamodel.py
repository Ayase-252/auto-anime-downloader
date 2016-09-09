"""Abstract base class for all data models."""


class DataModel:
    """Abstract base class for all data models.

    Attributes:
    primary_key: (Read Only)Primary key for the DataModel
    """
    _primary_key = ''

    @property
    def primary_key(cls):
        """Primary key.

        Returns:
            Primary key of the model.

        Raisea:
            ArributeError: If _primary_key is not set, namely, _primary_key is
                still '', AttributeError will be raised.
        """
        print('primary_key is', cls._primary_key)
        if cls._primary_key == '':
            raise AttributeError('Primary key for {} is not set'.format(
                cls.__name__
            ))

        return cls._primary_key

    def to_dict(self):
        """Convert instance into dictionary. All child class should implement
        their own to_dict method.

        Raises:
            NotImplementedError: If child class didn't override this method
        """
        raise NotImplementedError('to_dict() is not implemented yet.')

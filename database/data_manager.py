class DataManager:
    """Manages data object that implements DataInterface
    """
    @classmethod
    def save(cls):
        """Save object in database.
        Args:
            data   Object of class you want to store
        """
        raise NotImplementedError()

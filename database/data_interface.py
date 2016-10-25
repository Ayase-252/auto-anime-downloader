class DataInterface:
    def get_data_to_store(self):
        """Get data to store in dictionary.
        """
        raise NotImplementedError()

    def get_factory(self):
        """Get a factory function to produce object based on stored dictionary.
        """
        raise NotImplementedError()

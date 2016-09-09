import unittest

from models.datamodel import DataModel


class DataModelTest(unittest.TestCase):

    def test_primary_key_not_set(self):
        instance = DataModel()
        self.assertRaises(AttributeError,
                          lambda: instance.primary_key)

    def test_primary_key_set(self):
        class TestModel(DataModel):
            _primary_key = 'helloworld'

        instance = TestModel()
        result = instance.primary_key
        self.assertEqual(result, 'helloworld')

    def test_to_dict(self):
        instance = DataModel()

        self.assertRaises(NotImplementedError,
                          lambda: instance.to_dict())

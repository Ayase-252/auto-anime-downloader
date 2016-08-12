import unittest

import manage_base


class ManagePluginBaseClassTests(unittest.TestCase):

    def setUp(self):
        self.mpbc = manage_base.ManagePluginBase()

    def test_get_description(self):
        self.assertEqual('No description is provided for this command.',
                         self.mpbc.get_description())

    def test_func(self):
        self.assertRaises(
            NotImplementedError,
            self.mpbc.func,
            ()
        )

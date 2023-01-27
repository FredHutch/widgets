import unittest
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.resource import Resource


class TestResources(unittest.TestCase):

    def test_missing_id(self):

        # Resources must have an id defined
        self.assertRaises(
            ResourceConfigurationException,
            lambda: Resource()
        )


if __name__ == '__main__':
    unittest.main()

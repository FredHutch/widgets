import unittest
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.resource import Resource
from widgets.base.resource_list import ResourceList


class TestResources(unittest.TestCase):

    def test_missing_id(self):

        # Resources must have an id defined
        self.assertRaises(
            ResourceConfigurationException,
            lambda: Resource()
        )

    def test_value_assignment(self):

        # Define a resource
        r = Resource(id="test")

        # Set a value
        r.set_value("foo")

        # Get the value
        self.assertEqual(r.get_value(), "foo")

        # Modify the value
        r.set_value("bar")
        self.assertEqual(r.get_value(), "bar")

        # Set another attribute
        r.set("options", ["foo", "bar"])
        self.assertEqual(r.get("options"), ["foo", "bar"])


class TestResourceList(unittest.TestCase):

    def test_value_assignment(self):

        # Define a ResourceList
        r = ResourceList(
            id='top_list',
            resources=[
                Resource(id='first_resource', value='foo'),
                ResourceList(
                    id='second_list',
                    resources=[
                        Resource(id='second_resource', value='bar'),
                        ResourceList(
                            id='third_list',
                            resources=[
                                Resource(id='third_resource', value='howdy')
                            ]
                        )
                    ]
                )
            ]
        )

        self.assertEqual(r.get_value('first_resource'), 'foo')
        self.assertEqual(r.get_value('second_list', 'second_resource'), 'bar')
        self.assertEqual(r.get_value('second_list', 'third_list', 'third_resource'), 'howdy') # noqa

        # Change the values
        r.set_value('first_resource', 'FOO')
        r.set_value('second_list', 'second_resource', 'BAR')
        r.set_value('second_list', 'third_list', 'third_resource', 'HOWDY')

        self.assertEqual(r.get_value('first_resource'), 'FOO')
        self.assertEqual(r.get_value('second_list', 'second_resource'), 'BAR')
        self.assertEqual(r.get_value('second_list', 'third_list', 'third_resource'), 'HOWDY') # noqa

        # Get all of the values
        v = r.all_values()

        self.assertEqual(v['first_resource'], 'FOO')
        self.assertEqual(v['second_list']['second_resource'], 'BAR')
        self.assertEqual(v['second_list']['third_list']['third_resource'], 'HOWDY') # noqa


if __name__ == '__main__':
    unittest.main()

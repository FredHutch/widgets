import unittest
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.exceptions import ResourceExecutionException
from widgets.base.resource import Resource
from widgets.base.widget import Widget
import widgets


class TestModule(unittest.TestCase):

    def test_version_string(self):

        self.assertIsInstance(widgets.__version__, str)


class TestResources(unittest.TestCase):

    def test_missing_id(self):

        # Default id is "resource"
        r = Resource()
        self.assertEqual(r.id, "resource")

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
        r.set(attr="options", value=["foo", "bar"])
        self.assertEqual(r.get(attr="options"), ["foo", "bar"])

    def test_missing_attribute(self):

        # Define a resource
        r = Resource(id="test")

        self.assertRaises(
            ResourceExecutionException,
            lambda: r.get("missing_attribute")
        )

    def test_isinstance(self):

        # Define a resource
        r = Resource(id="test")

        try:
            r._assert_isinstance(Resource)
        except ResourceConfigurationException:
            self.fail("Should not have raised ResourceConfigurationException")

        self.assertRaises(
            ResourceConfigurationException,
            lambda: r._assert_isinstance(Resource, case=False)
        )

    def test_child_value_assignment(self):

        # Define a Resource
        r = Resource(
            id='top_list',
            children=[
                Resource(id='first_resource', value='foo'),
                Resource(
                    id='second_list',
                    children=[
                        Resource(id='second_resource', value='bar'),
                        Resource(
                            id='third_list',
                            children=[
                                Resource(id='third_resource', value='howdy')
                            ]
                        )
                    ]
                )
            ]
        )

        self.assertEqual(r.get(path=['first_resource']), 'foo')
        self.assertEqual(r.get(path=['second_list', 'second_resource']), 'bar')
        self.assertEqual(r.get(path=['second_list', 'third_list', 'third_resource']), 'howdy') # noqa

        # Change the values
        r.set(path=['first_resource'], value='FOO')
        self.assertEqual(r.get(path=['first_resource']), 'FOO')

        r.set(path=['second_list', 'second_resource'], value='BAR')
        self.assertEqual(r.get(path=['second_list', 'second_resource']), 'BAR')

        r.set(path=['second_list', 'third_list', 'third_resource'], value='HOWDY') # noqa
        self.assertEqual(r.get(path=['second_list', 'third_list', 'third_resource']), 'HOWDY') # noqa

        # Get all of the values
        v = r.all_values()

        self.assertEqual(v['first_resource'], 'FOO')
        self.assertEqual(v['second_list']['second_resource'], 'BAR')
        self.assertEqual(v['second_list']['third_list']['third_resource'], 'HOWDY') # noqa

    def test_init_exceptions(self):

        # Child elements must actually be Resources
        self.assertRaises(
            ResourceConfigurationException,
            lambda: Resource(children=['foo'])
        )

        # Elements in resources cannot have repeated ids
        self.assertRaises(
            ResourceConfigurationException,
            lambda: Resource(
                children=[
                    Resource(id="foo"),
                    Resource(id="foo")
                ]
            )
        )

    def test_nested_isinstance(self):

        # Define a nested set of resources
        r = Resource(
            id="top",
            children=[
                Resource(
                    id="middle",
                    children=[
                        Resource(id="last")
                    ]
                )
            ]
        )

        try:
            r._get_child(
                "middle"
            )._assert_isinstance(
                Resource,
                parent=True
            )
        except ResourceConfigurationException:
            self.fail("Should not have raised ResourceConfigurationException")

        self.assertRaises(
            ResourceConfigurationException,
            lambda: r._get_child("middle")._assert_isinstance(Resource, parent=True, case=False) # noqa
        )

    def test_run(self):

        # Define a nested set of resources
        r = Resource(
            id="top",
            children=[
                Resource(
                    id="middle",
                    children=[
                        Resource(id="last")
                    ]
                )
            ]
        )

        # Make sure that the run method doesn't raise an exception
        try:
            r.run()
        except Exception as e:
            self.fail(f"w.run() raised: {str(e)}")

    def test_new(self):
        """Test the functionality to make a new Resource."""

        rl = Resource(id='new')

        self.assertIsInstance(
            rl.new_child(id='new'),
            Resource
        )

    def test_append(self):
        """Test the functionality to append a Resource to the list."""

        rl = Resource(id='append')

        self.assertEqual(len(rl.children), 0)
        self.assertEqual(len(rl._children_dict), 0)

        rl.append_child(id='append')

        self.assertEqual(len(rl.children), 1)
        self.assertEqual(len(rl._children_dict), 1)

        rl.remove_child(0)

    def test_remove(self):
        """Test the functionality to remove a Resource from the list."""

        rl = Resource(id='remove')
        self.assertEqual(
            len(rl.children),
            0,
            list(map(lambda r: r.source(), rl.children))
        )
        rl.append_child()

        self.assertEqual(len(rl.children), 1)
        self.assertEqual(len(rl._children_dict), 1)

        try:
            rl.remove_child(0)
        except Exception as e:
            self.fail(str(e))

        self.assertEqual(len(rl.children), 0)
        self.assertEqual(len(rl._children_dict), 0)


class TestWidget(unittest.TestCase):

    def test_init(self):

        w = Widget(
            children=[
                Resource(
                    id="first_list",
                    children=[
                        Resource(id="first_value")
                    ]
                )
            ]
        )

        # Make sure that the run method doesn't raise an exception
        try:
            w.run()
        except Exception as e:
            self.fail(f"w.run() raised: {str(e)}")

        # Make sure that the run_cli method doesn't raise an exception
        try:
            w.run_cli()
        except Exception as e:
            self.fail(f"w.run() raised: {str(e)}")


if __name__ == '__main__':
    unittest.main()

import unittest
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.exceptions import ResourceExecutionException
from widgets.base.exceptions import WidgetConfigurationException
from widgets.base.resource import Resource
from widgets.base.resource_list import ResourceList
from widgets.base.widget import Widget
import widgets


class TestModule(unittest.TestCase):

    def test_version_string(self):

        self.assertIsInstance(widgets.__version__, str)


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

    def test_init_exceptions(self):

        # Elements in resources must actually be Resources
        self.assertRaises(
            WidgetConfigurationException,
            lambda: ResourceList(resources=['foo'])
        )

        # Elements in resources cannot have repeated ids
        self.assertRaises(
            WidgetConfigurationException,
            lambda: ResourceList(
                resources=[
                    Resource(id="foo"),
                    Resource(id="foo")
                ]
            )
        )

    def test_isinstance(self):

        # Define a nested set of resources
        r = ResourceList(
            id="top",
            resources=[
                ResourceList(
                    id="middle",
                    resources=[
                        Resource(id="last")
                    ]
                )
            ]
        )

        try:
            r._get_resource(
                "middle"
            )._assert_isinstance(
                ResourceList,
                parent=True
            )
        except ResourceConfigurationException:
            self.fail("Should not have raised ResourceConfigurationException")

        self.assertRaises(
            ResourceConfigurationException,
            lambda: r._get_resource("middle")._assert_isinstance(ResourceList, parent=True, case=False) # noqa
        )


class TestWidget(unittest.TestCase):

    def test_init(self):

        w = Widget(
            resources=[
                ResourceList(
                    id="first_list",
                    resources=[
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

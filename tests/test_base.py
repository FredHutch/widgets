from copy import deepcopy
import unittest
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.exceptions import WidgetFunctionException
from widgets.base.exceptions import ResourceExecutionException
from widgets.base.resource import Resource
from widgets.base.widget import Widget
import widgets


class TestModule(unittest.TestCase):

    def test_version_string(self):

        self.assertIsInstance(widgets.__version__, str)

    def test_imports(self):

        try:
            import widgets.streamlit # noqa
        except ImportError as e:
            self.fail(f"Could not import widgets.streamlit: {str(e)}")


class TestResources(unittest.TestCase):

    def test_missing_id(self):

        # Default id is "resource"
        r = Resource()
        self.assertEqual(r.id, "resource")

        self.assertRaises(
            ResourceConfigurationException,
            lambda: Resource(id="")
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

        self.assertRaises(
            ResourceConfigurationException,
            lambda: r._assert_isinstance(str, case=True)
        )

    def setup_example_resource(self):

        return deepcopy(
            Resource(
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
                                    Resource(id='third_resource', value='howdy') # noqa
                                ]
                            )
                        ]
                    )
                ]
            )
        )

    def test_child_value_assignment(self):

        # Define a Resource
        r = self.setup_example_resource()

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

        # Test the _path_to_root method
        self.assertEqual(
            r._get_child('second_list', 'third_list', 'third_resource')._path_to_root(), # noqa
            ['third_resource', 'third_list', 'second_list', 'top_list']
        )

        # Test the _root method
        self.assertEqual(
            r._get_child('second_list', 'third_list', 'third_resource')._root().id, # noqa
            'top_list'
        )

        # Test the exception raised when an attribute doesn't exist
        self.assertRaises(
            ResourceExecutionException,
            lambda: r.get(attr='missing_attribute')
        )

    def test_find_child(self):
        """Test the _find_child method."""

        # Define a Resource
        r = self.setup_example_resource()

        for id, val in [
            ('first_resource', 'foo'),
            ('second_resource', 'bar'),
            ('third_resource', 'howdy')
        ]:
            all_matching = list(r._find_child(id))

            self.assertEqual(len(all_matching), 1, id)
            self.assertEqual(all_matching[0].get_value(), val)

    def test_all_values(self):

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

        # Change the values
        r.set(path=['first_resource'], value='FOO')
        r.set(path=['second_list', 'second_resource'], value='BAR')
        r.set(path=['second_list', 'third_list', 'third_resource'], value='HOWDY') # noqa

        # Get all of the values
        v = r.all_values()

        self.assertEqual(v['first_resource'], 'FOO')
        self.assertEqual(v['second_list']['second_resource'], 'BAR')
        self.assertEqual(v['second_list']['third_list']['third_resource'], 'HOWDY') # noqa

        # Get all of the values after the first one
        v = r.all_values(path=['second_list'])
        self.assertEqual(v['second_resource'], 'BAR')
        self.assertEqual(v['third_list']['third_resource'], 'HOWDY')

        # Get the flat values
        v = r.all_values(flatten=True)
        self.assertEqual(v['first_resource'], 'FOO')
        self.assertEqual(v['second_resource'], 'BAR')
        self.assertEqual(v['third_resource'], 'HOWDY')

        # Define a resource which cannot be flattened
        r = Resource(
            children=[
                Resource(
                    id='list_a',
                    children=[
                        Resource(
                            id='duplicated_id',
                            value='foo'
                        )
                    ]
                ),
                Resource(
                    id='list_b',
                    children=[
                        Resource(
                            id='duplicated_id',
                            value='bar'
                        )
                    ]
                )
            ]
        )

        self.assertRaises(
            ResourceExecutionException,
            lambda: r.all_values(flatten=True)
        )

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

    def test_attach_children(self):

        r = Resource()
        self.assertRaises(
            ResourceConfigurationException,
            lambda: r._attach_children("foo")
        )

    def test_attach_child(self):

        r = Resource()
        self.assertRaises(
            ResourceConfigurationException,
            lambda: r._attach_child("foo")
        )


class ExampleWidget(Widget):

    children = [Resource(id="elem_0"), Resource(id="elem_1")]


class ExampleSubWidget(ExampleWidget):

    label = "FOOBAR"


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

    def test_stubs(self):
        w = Widget()

        try:
            w.to_html()
        except Exception as e:
            self.fail(f"Command fails: to_html - {str(e)}")

        try:
            w.to_script()
        except Exception as e:
            self.fail(f"Command fails: to_script - {str(e)}")

        try:
            w.download_html_button()
        except Exception as e:
            self.fail(f"Command fails: download_html_button - {str(e)}")

        try:
            w.download_script_button()
        except Exception as e:
            self.fail(f"Command fails: download_script_button - {str(e)}")

    def test_exceptions(self):
        w = ExampleWidget()
        w.children = []

        self.assertRaises(
            WidgetFunctionException,
            lambda: w._to_file(w.source_init(), fp=0)
        )

    def test_parent_class_chain(self):

        w = ExampleSubWidget()

        self.assertEqual(
            w.__class__.__name__,
            "ExampleSubWidget"
        )

        self.assertEqual(
            w._parent_class().__name__,
            "ExampleWidget"
        )

        self.assertEqual(
            list([c.__name__ for c in w._parent_class_chain()]),
            ["ExampleWidget", "Widget", "Resource"]
        )

    def test_source_attributes(self):

        w = ExampleSubWidget(id='foo')
        w.label = 'BAR'

        self.assertTrue(
            'label = "BAR"' in w._source_attributes(),
            w._source_attributes()
        )


if __name__ == '__main__':
    unittest.main()

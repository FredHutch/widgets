from pathlib import Path
from tempfile import NamedTemporaryFile
import pandas as pd
import unittest
from widgets.base.exceptions import ResourceConfigurationException
from widgets.base.io import load_widget
import widgets.streamlit as wist


class TestStreamlitResources(unittest.TestCase):

    def test_dataframe(self):

        df = pd.DataFrame(dict(a=[1, 2, 3], b=['a', 'b', 'c']))

        res = wist.StDataFrame(
            id="test_dataframe",
            value=df
        )

        # Check the default value
        msg = "Default DataFrame does not match"
        self.assertTrue(df.equals(res.value), msg)

        # Make sure that an error is raised for an inappropriate type
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDataFrame(id="test_dataframe", value="foo")
        )

        # Try an empty value
        res = wist.StDataFrame(id="test_dataframe")
        msg = "Empty value not created correctly"
        self.assertTrue(pd.DataFrame().equals(res.value), msg)

    def test_dataframe_fromdict(self):

        df = pd.DataFrame(dict(a=[1, 2, 3], b=['a', 'b', 'c']))

        # Make an StDataFrame based on the dict of that DataFrame
        res = wist.StDataFrame(
            id="test_dataframe",
            value=df.to_dict(orient="list")
        )

        # Make sure that the values are equal
        self.assertTrue(df.equals(res.value))

    def test_dataframe_fromsplit(self):

        df = pd.DataFrame(dict(a=[1, 2, 3], b=['a', 'b', 'c']))
        split_dict = df.to_dict(orient='split')

        # Make an StDataFrame based on the dict of that DataFrame
        res = wist.StDataFrame(
            id="test_dataframe",
            value=split_dict
        )

        # Make sure that the values are equal
        self.assertTrue(df.equals(res.value))

    def test_dataframe_exception(self):

        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDataFrame(id="invalid_dataframe", value=0)
        )

    def test_string(self):

        s = wist.StString(
            id="test_string",
            value="value"
        )

        # Check the default value
        msg = "Default string does not match"
        self.assertEqual(s.get_value(), "value", msg)

        # Try an empty value
        s = wist.StString(id="test_string")
        msg = "Empty value not created correctly"
        self.assertIsNone(s.get_value(), msg)

    def test_integer(self):

        s = wist.StInteger(
            id="test_integer",
            value=1
        )

        # Check the default value
        self.assertEqual(s.get_value(), 1, "Default integer does not match")

        # Try an empty value
        s = wist.StInteger(id="test_integer")
        self.assertEqual(int(), s.get_value(), "Empty value not created")

    def test_float(self):

        s = wist.StFloat(
            id="test_float",
            value=1.0
        )

        # Check the default value
        msg = "Default float does not match"
        self.assertEqual(s.get_value(), 1.0, msg)

        # Try an empty value
        s = wist.StFloat(id="test_float")

        msg = "Empty value not created correctly"
        self.assertEqual(float(), s.get_value(), msg)

    def test_float_exception(self):

        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StFloat(id="invalid_float", value='foobar')
        )

    def test_slider(self):

        s = wist.StSlider(
            id="test_slider",
            value=1.0,
            min_value=0.0,
            max_value=1.0
        )

        # Check the default value
        msg = "Default float does not match"
        self.assertEqual(s.get_value(), 1.0, msg)


class ExampleStreamlitWidget(wist.StreamlitWidget):
    """Simple widget used for testing purposes"""

    children = [
        wist.StString(id="s", value="s", label="String"),
        wist.StInteger(id="i", value=0, label="Integer"),
        wist.StFloat(id="f", value=0.0, label="Float"),
        wist.StMultiSelect(
            id='multi',
            value=['a'],
            options=pd.Series(['a', 'b', 'c']).values
        )
    ]


class TestStreamlitWidget(unittest.TestCase):

    def test_import(self):
        """Test whether the default resource values are set correctly."""

        # Create a widget with default values
        w_def = ExampleStreamlitWidget()
        self.assertEqual(w_def.get(path=["s"]), "s")
        self.assertEqual(w_def.get(path=["i"]), 0)
        self.assertEqual(w_def.get(path=["f"]), 0.0)

    def test_script(self):
        """Test whether widgets can be saved to a file and loaded again."""

        # Create a widget with default values
        w = ExampleStreamlitWidget(label="FOOBAR")

        # Make sure that the label attribute was set
        self.assertEqual(w.label, "FOOBAR")

        # Change the data value
        w.set(path=["s"], value="t", update=False)
        self.assertEqual(w.get(["s"]), "t")
        w.set(path=["i"], value=1, update=False)
        w.set(path=["f"], value=1.0, update=False)

        # Make a tempfile for the script
        with NamedTemporaryFile(suffix=".py") as tmp:

            # Save the file
            w.to_script(Path(tmp.name))

            # Load the script
            try:
                saved_widget = load_widget(
                    Path(tmp.name),
                    "ExampleStreamlitWidget"
                )
            except Exception as e:
                error_str = f"{str(e)}\n{w._render_script()}"
                msg = f"Could not load ExampleStreamlitWidget\n{error_str}"
                self.fail(msg)

            # Instantiate the widget
            s = saved_widget()

            # Make sure that the label attribute was saved
            msg = s._source_attributes()
            self.assertEqual(s.label, "FOOBAR", msg)

            # Make sure that the data values were changed
            self.assertEqual(s.get(path=["s"]), "t", w.to_script())
            self.assertEqual(s.get(path=["i"]), 1)
            self.assertEqual(s.get(path=["f"]), 1.0)

            # Make sure that the StMultiSelect values were serialized correctly
            self.assertEqual(s.get(path=["multi"]), ["a"])
            self.assertEqual(
                s.get(path=["multi"], attr="options"),
                ["a", "b", "c"]
            )

    def test_select_string(self):

        # Options must be a list
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StSelectString(id='test', options="foo")
        )

        # Must provide value or index
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StSelectString(id='test', value=None, index=None)
        )

        # Index must be a positive integer
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StSelectString(id='test', value=None, index=-1)
        )

        # Set the value from the index
        r = wist.StSelectString(options=['foo', 'bar'], index=1, id='test')
        self.assertEqual(r.get_value(), 'bar')

        # To select by value, the value must be in the list
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StSelectString(id='t', options=['foo'], value='FOO')
        )

        # Set the index from the value
        r = wist.StSelectString(options=['foo', 'bar'], value='bar', id='test')
        self.assertEqual(r.index, 1)

    def test_html(self):
        # Test if the to_html method returns a non-zero length string

        # Create a simple widget
        w = ExampleStreamlitWidget()

        # Render HTML as a string
        html = w.to_html()

        self.assertIsInstance(html, str)
        self.assertGreater(len(html), 0)

    def test_StDownloadDataFrame(self):

        # StDownloadDataFrame must have a target
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StDownloadDataFrame()
        )

    def test_StSelector(self):

        # Must define options
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StSelector()
        )

        # options must be a list
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StSelector(options='foo')
        )

        # options must be a list of Resources
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StSelector(options=['foo'])
        )

        # options must be a list of unique Resources
        self.assertRaises(
            ResourceConfigurationException,
            lambda: wist.StSelector(options=[wist.StResource(), wist.StResource()]) # noqa
        )

        # Make a Selector
        w = ExampleSelectorWidget()

        # Test all_values
        self.assertEqual(
            w.all_values(),
            {"selector": "foo"}
        )

        # Change the selected value
        w.set(["selector"], value='Option 2', update=False)

        # Make sure that the selected option has changed
        self.assertEqual(
            w.all_values(),
            {"selector": "bar"}
        )

        # Make a tempfile for the script
        with NamedTemporaryFile(suffix=".py") as tmp:

            # Save the file
            w.to_script(Path(tmp.name))

            # Load the script
            try:
                saved_widget = load_widget(
                    Path(tmp.name),
                    "ExampleSelectorWidget"
                )
            except Exception as e:
                error_str = f"{str(e)}\n{w._render_script()}"
                msg = f"Could not load ExampleSelectorWidget\n{error_str}"
                self.fail(msg)

            # Instantiate the widget
            s = saved_widget()

            # Make sure that the selected element was saved
            self.assertEqual(s.all_values(), {"selector": "bar"})


class ExampleSelectorWidget(wist.StreamlitWidget):

    children = [
        wist.StSelector(
            options=[
                wist.StResource(
                    id='option_1',
                    label="Option 1",
                    value='foo'
                ),
                wist.StResource(
                    id='option_2',
                    label="Option 2",
                    value='bar'
                )
            ]
        )
    ]


if __name__ == '__main__':
    unittest.main()

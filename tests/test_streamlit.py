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
        wist.StFloat(id="f", value=0.0, label="Float")
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
        w = ExampleStreamlitWidget()

        # Change the data value
        w.set(path=["s"], value="t", update=False)
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

            # Make sure that the data values were changed
            self.assertEqual(s.get(path=["s"]), "t", w.to_script())
            self.assertEqual(s.get(path=["i"]), 1)
            self.assertEqual(s.get(path=["f"]), 1.0)

    def test_html(self):
        # Test if the to_html method returns a non-zero length string

        # Create a simple widget
        w = ExampleStreamlitWidget()

        # Render HTML as a string
        html = w.to_html()

        self.assertIsInstance(html, str)
        self.assertGreater(len(html), 0)


if __name__ == '__main__':
    unittest.main()

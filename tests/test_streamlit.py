from pathlib import Path
from tempfile import NamedTemporaryFile
import pandas as pd
import unittest
from widgets.base.io import load_widget
from widgets.streamlit.resources.dataframe import StDataFrame
from widgets.streamlit.resources.value import StString, StInteger, StFloat
from widgets.streamlit.widget import StreamlitWidget


class TestStreamlitResources(unittest.TestCase):

    def test_dataframe(self):

        df_default = pd.DataFrame(dict(a=[1, 2, 3], b=['a', 'b', 'c']))

        df = StDataFrame(
            id="test_dataframe",
            default=df_default
        )

        # Check the default value
        self.assertTrue(df_default.equals(df.default), "Default DataFrame does not match")

        # Use a different value to override the default
        df_saved = pd.DataFrame(dict(a=[1, 2, 3], b=['x', 'y', 'z']))
        df._setup_default(df_saved)
        
        # Check the saved value
        self.assertTrue(df_saved.equals(df.default), "Saved DataFrame does not match")

    def test_string(self):

        s = StString(
            id="test_string",
            default="default"
        )

        # Check the default value
        self.assertEqual(s.default, "default", "Default string does not match")

        # Use a different value to override the default
        s._setup_default("saved")

        # Check the saved value
        self.assertEqual(s.default, "saved", "Saved string does not match")

    def test_integer(self):

        s = StInteger(
            id="test_integer",
            default=0
        )

        # Check the default value
        self.assertEqual(s.default, 0, "Default integer does not match")

        # Use a different value to override the default
        s._setup_default(1)

        # Check the saved value
        self.assertEqual(s.default, 1, "Saved integer does not match")

    def test_float(self):

        s = StFloat(
            id="test_float",
            default=0.0
        )

        # Check the default value
        self.assertEqual(s.default, 0.0, "Default float does not match")

        # Use a different value to override the default
        s._setup_default(1.1)

        # Check the saved value
        self.assertEqual(s.default, 1.1, "Saved float does not match")


class ExampleStreamlitWidget(StreamlitWidget):
    """Simple widget used for testing purposes"""

    resources = [
        StString(id="s", default="s", label="String"),
        StInteger(id="i", default=0, label="Integer"),
        StFloat(id="f", default=0.0, label="Float")
    ]

    def viz(self):

        pass


class TestStreamlitWidget(unittest.TestCase):

    def test_import(self):
        """Test whether the default resource values are set correctly."""

        # Create a widget with default values
        w_def = ExampleStreamlitWidget()
        self.assertEqual(w_def.data["s"], "s")
        self.assertEqual(w_def.data["i"], 0)
        self.assertEqual(w_def.data["f"], 0.0)

    def test_script(self):
        """Test whether widgets can be saved to a file and loaded again."""

        # Create a widget with default values
        w = ExampleStreamlitWidget()
        
        # Change the data value
        w.data["s"] = "t"
        w.data["i"] = 1
        w.data["f"] = 1.0

        # Make a tempfile for the script
        with NamedTemporaryFile(suffix=".py") as tmp:

            # Save the file
            w.to_script(Path(tmp.name))

            # Load the script
            saved_widget = load_widget(Path(tmp.name), "ExampleStreamlitWidget")

            # Instantiate the widget
            s = saved_widget()

            # Make sure that the data values were changed
            self.assertEqual(s.data["s"], "t")
            self.assertEqual(s.data["i"], 1)
            self.assertEqual(s.data["f"], 1.0)

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
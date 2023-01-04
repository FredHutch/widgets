import pandas as pd
import unittest
from widgets.streamlit.resources.dataframe import DataFrame
from widgets.streamlit.resources.value import String, Integer, Float
from widgets.streamlit.widget import StreamlitWidget


class TestStreamlitResources(unittest.TestCase):

    def test_dataframe(self):

        df_default = pd.DataFrame(dict(a=[1, 2, 3], b=['a', 'b', 'c']))

        df = DataFrame(
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

        s = String(
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

        s = Integer(
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

        s = Float(
            id="test_float",
            default=0.0
        )

        # Check the default value
        self.assertEqual(s.default, 0.0, "Default float does not match")

        # Use a different value to override the default
        s._setup_default(1.1)

        # Check the saved value
        self.assertEqual(s.default, 1.1, "Saved float does not match")


class StreamlitWidget(StreamlitWidget):
    """Simple widget used for testing purposes"""

    resources = [
        String(id="s", default="s", label="String"),
        Integer(id="i", default=0, label="Integer"),
        Float(id="f", default=0.0, label="Float")
    ]

    def viz(self):

        pass


class TestStreamlitWidget(unittest.TestCase):

    def test_html(self):

        # Create a simple widget
        w = StreamlitWidget()

        # Render HTML as a string
        html = w.to_html()

        self.assertIsInstance(html, str)
        self.assertGreater(len(html), 0)


if __name__ == '__main__':
    unittest.main()
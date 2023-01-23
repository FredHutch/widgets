import unittest
from widgets.base.io import load_widget
from widgets.base.exceptions import IOException, WidgetInitializationException
from widgets.base.widget import Widget
from widgets.streamlit.widget import StreamlitWidget


class TestIO(unittest.TestCase):

    def test_load_widget(self):

        # Load the test widget
        w = load_widget("tests/assets/app.py", "SimpleWidget")
        self.assertIsInstance(w(), Widget)

    def test_load_streamlit_widget(self):

        # Load the test streamlit widget
        w = load_widget("tests/assets/app.py", "SimpleStWidget")
        self.assertIsInstance(w(), StreamlitWidget)

    def test_load_widget_errors(self):

        self.assertRaises(
            IOException,
            lambda: load_widget("tests/assets/wrong_path.py", "SimpleWidget")
        )

        self.assertRaises(
            IOException,
            lambda: load_widget("tests/assets/app.py", "WrongName")
        )

        self.assertRaises(
            WidgetInitializationException,
            lambda: load_widget("tests/assets/app.py", "SimpleWidgetNoBase")
        )


if __name__ == '__main__':
    unittest.main()

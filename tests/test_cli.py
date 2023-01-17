import os
from click.testing import CliRunner
import unittest
from widgets.cli.main import main


class TestCLI(unittest.TestCase):

    def test_primary(self):

        runner = CliRunner()
        result = runner.invoke(main, [])
        self.assertEqual(result.exit_code, 0)

    def test_tohtml(self):

        runner = CliRunner()
        result = runner.invoke(
            main,
            ["tohtml", "tests/st_simple_widget/app.py", "SimpleWidget"]
        )
        self.assertEqual(result.exit_code, 0, result.exception)
        self.assertTrue(os.path.exists("widget.html"), result.output)
        os.remove("widget.html")

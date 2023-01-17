from pathlib import Path
import click
import logging
from widgets.base.io import load_widget


@click.group()
@click.option('--debug/--no-debug', default=False)
def main(debug):
    """Command line utilities for widgets"""
    logging.basicConfig(
        format='%(process)d-%(levelname)s-%(message)s',
        level=logging.DEBUG if debug else logging.INFO
    )


@main.command()
@click.argument("path_or_url")
@click.argument("widget_name")
@click.option("-t", "--title", default="Widget")
def run(path_or_url, widget_name, title="Widget"):
    """
    Run a widget interactively

    Arguments:

        path_or_url     Local path or URL for file containing widget script
        widget_name     Name of the widget defined in that script

    """

    logging.debug("Subcommand: run")
    logging.debug(f"path_or_url: {path_or_url}")
    logging.debug(f"widget_name: {widget_name}")

    # Get the widget defined in the file
    widget = load_widget(path_or_url, widget_name)

    # Instantiate the widget
    w = widget()

    # Run the widget
    w.run_cli(title=title)


@main.command()
@click.argument("path_or_url")
@click.argument("widget_name")
@click.option(
    "--filename",
    default="widget.html",
    help="Name of HTML file (default: widget.html)"
)
def tohtml(path_or_url, widget_name, filename):
    """
    Convert a widget script to an HTML file

    Arguments:

        path_or_url     Local path or URL for file containing widget script
        widget_name     Name of the widget defined in that script

    """

    logging.debug("Subcommand: tohtml")
    logging.debug(f"path_or_url: {path_or_url}")
    logging.debug(f"widget_name: {widget_name}")
    logging.debug(f"filename: {filename}")

    # Get the widget defined in the file
    widget = load_widget(path_or_url, widget_name)

    # Write out the widget as HTML
    widget().to_html(Path(filename))

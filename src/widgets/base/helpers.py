from jinja2 import Environment, PackageLoader


def render_template(template_name: str, **kwargs):
    """Return a jinja2 template defined in this library."""

    # Set up the jinja2 environment
    env = Environment(
        loader=PackageLoader("widgets")
    )

    # Get the template being used
    template = env.get_template(template_name)

    # Render the template
    return template.render(**kwargs)


def source_val(val):
    """
    Return a string representation of the value which can be used in source.
    """

    if isinstance(val, str):
        return f'"{val}"'
    else:
        return val

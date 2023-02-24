# Developers' Guide

The `widgets-lib` codebase defines a set of high-level objects which
can be used to construct interactive widgets.

## Core Concepts

At the heart of every widget is the set of 'Resources' which it uses.

### Data Resources

A resource could be a single value (string, float, etc.), a data table,
a file, or any other item of information.
Crucially, the value of a resource must be able to be serialized as
a string value which can then be embedded in a Python script.
This process of resource serialization is essential for the ability
of a widget to save itself after being modified in some way.

### Visualization Resources

A resource could also be a function for rendering visualizations which
are responsive to changes in the values of over resources.
Resources can contain other resources as child elements.
Widgets are built by combining logical units of resources together
to fulfill the intended purpose.

## Resource Attributes

The minimal attributes of a Resource are:

- `id`: A unique identifier not used by any other resource in the same widget
- `value`: The value being saved by the widget
- `children`: The list of resources contained as child elements
- `label`: (optional) label used when displaying the resource in the UI
- `help`: (optional) text string describing the resource

## Resource Functions

The minimal functions on the resource are:

- `get()`: Get the value of an attribute of the resource or its child
- `get_value()`: Get the value of the 'value' attribute of the resource
- `set()`: Set a new value for an attribute of the resource or its child
- `set_value()`: Set a new value for the 'value' attribute of the resource
- `all_values()`: Create a dict containing the results of `.get_value()` for each Resource in the list, keyed by `.id`.
- `source_init()`: Return a string with the source code needed to initialize the resource in its current state
- `source_self()`: Return a string with the source code needed to define the class of the resource
- `source_all()`: Combined results of source_self() for all child / parent elements which are defined outside of the widgets library
- `run()`: Run the three main functions: `prep()`, `run_children()`, and `run_self()`
- `prep()`: Stub used to perform any tasks which must happen before the children are run
- `run_children()`: Invoke `.run()` for all Resources in the `.children` list
- `run _self()`: Perform any visualization associated with the element

## Navigating Child Elements

Accessing and manipulating the resource attributes within nested
resource lists is accomplished with additional positional arguments
which provide the complete list of nested elements.
For example, consider a nested resource list with the following structure:

```
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
```

The following commands can be used to access the contents of `r`:

```
r.get(path=['first_resource']) -> 'foo'
r.get(path=['second_list', 'second_resource']) -> 'bar'
r.get(path=['second_list', 'third_list', 'third_resource']) -> 'howdy'

r.all_values() -> {
    'first_resource': 'foo',
    'second_list': {
        'second_resource': 'bar',
        'third_list': {
            'third_resource': 'howdy'
        }
    }
}
```

The contents of the nested elements can be manipulated by
including the full path to each element in the arguments to the `.set()` function.

```
r.set(
    path=['second_list', 'third_list', 'third_resource'],
    value='HOWDY'
)
```

### Widget

The Widget class is based on the ResourceList can use all of the same methods
for accessing and manipulating the attributes of the Resources which it contains.
However, the Resources are not populated at initialization time.
Instead, it is assumed that the contents of `self.children` will be defined
by the subclass of Widget itself.
This approach is used in order to provide the user with an easy way to
override the default functions associated with the widget.

To customize a widget, create a subclass of Widget which:
- 1. Overrides the `self.children` attribute to specify the Resources which are needed for functioning, and
- 2. Overrides the `.run_self()` method to provide interactivity based on the values provided to those Resources.
- 3. Optionally overrides the `.prep()` method to perform any tasks which must take place before the Resources are run.

To allow for a good amount of flexibility in creating Widgets which are
based on specific visualization suites (e.g., the StreamlitWidget described below),
the methods used in each Widget are as follows:

- `.run_cli()`: Used for functionality when being run from the command line
- `.to_html()`: Stub for authoring HTML with the live contents of the widget
- `.to_script()`: Stub for authoring a Python script with the live contents of the widget
- `.download_html_button()`: Render a button allowing the user to download the live widget as HTML
- `.download_script_button()`: Render a button allowing the user to download the live widget as a Python script

### Streamlit-Based Widgets

All of the framework provided for the `Widget` object above is intended to make
it easier to develop widgets which are based on different visualization frameworks.
By itself, the `Widget` object is likely useless, but it provides a base class
which can be overridden with platform-specific code.

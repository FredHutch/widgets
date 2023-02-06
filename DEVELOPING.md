# Developers' Guide

The `widgets-lib` codebase defines a set of high-level objects which
can be used to construct interactive widgets.

## Core Concepts

At the heart of every widget is the set of 'Resources' which it uses.
A resource could be a single value (string, float, etc.), a data table,
a file, or any other item of information.
Crucially, the value of a resource must be able to be serialized as
a string value which can then be embedded in a Python script.
This process of resource serialization is essential for the ability
of a widget to save itself after being modified in some way.

## Components

### Resource

The minimal attributes of a Resource are:

- `id`: A unique identifier not used by any other resource in the same widget
- `value`: The value being saved by the widget
- `label`: (optional) label used when displaying the resource in the UI
- `help`: (optional) text string describing the resource

The minimal functions on the resource are:

- `get(attr)`: Get the value of an attribute of the resource
- `get_value()`: Get the value of the 'value' attribute of the resource
- `set(attr, val)`: Set a new value for an attribute of the resource
- `set_value(val)`: Set a new value for the 'value' attribute of the resource
- `source()`: Return a string with the source code needed to initialize the resource in its current state
- `run(container)`: Set up the user interface for modifying the value of the resource within a provided container

### ResourceList

The ResourceList is provided for logical groupings of Resources.
An example of such a grouping might be a collapse element which contains
multiple resources, as well as a header and independent interactivity.
Note that the ResourceList element is intended to support arbitrary levels
of nesting.
In other words, any ResourceList should be able to wrap up a set of
elements which can be either base Resources or nested ResourceLists.

The minimal attributes of a ResourceList are:

- `id`: A unique identifier not used by any other resource in the same widget
- `label`: (optional) label used when displaying the resource list in the UI
- `help`: (optional) text string describing the resource list
- `resources`: The list of resources (or resource lists) contained within

The minimal functions of the resource list are similar to that of the
resource, but they contain one additional level of nesting to access values
within the resources in the list.

- `get(resource_id, attr)`: Get the value of an attribute for a resource in the list
- `get_value(resource_id)`: Get the value of the 'value' attribute for a resource in the list
- `set(resource_id, attr, val)`: Set a new value for an attribute for a resource in the list
- `set_value(resource_id, val)`: Set a new value for the 'value' attribute for a resource in the list
- `source()`: Return a string with the source code needed to initialize the resource list in its current state
- `all_values()`: Create a dict containing the results of `.get_value()` for each Resource in the list (or `.all_values()` for each ResourceList), keyed by `.id`.
- `run(container)`: The `run()` method of the ResourceList invokes three functions: `prep()`, `run_children(container)`, and `viz()`
- `prep()`: Stub used to perform any tasks which must happen before the children are run
- `run_children(container)`: Invoke `.run(container)` for all Resources in the `.resources` list
- `viz()`: Perform any visualization associated with this group of Resources


Accessing and manipulating the resource attributes within nested
resource lists is accomplished with additional positional arguments
which provide the complete list of nested elements.
For example, consider a nested resource list with the following structure:

```
r = ResourceList(
    id='top_list',
    resources=[
        Resource(id='first_resource', value='foo'),
        ResourceList(
            id='second_list',
            resources=[
                Resource(id='second_resource', value='bar'),
                ResourceList(
                    id='third_list',
                    resources=[
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
r.get_value('first_resource') -> 'foo'
r.get_value('second_list', 'second_resource') -> 'bar'
r.get_value('second_list', 'third_list', 'third_resource') -> 'howdy'

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
r.set_value('second_list', 'third_list', 'third_resource', 'HOWDY')

# or

r.set('second_list', 'third_list', 'third_resource', 'value', 'HOWDY')
```

### Widget

The Widget class is based on the ResourceList can use all of the same methods
for accessing and manipulating the attributes of the Resources which it contains.
However, the Resources are not populated at initialization time.
Instead, it is assumed that the contents of `self.resources` will be defined
by the subclass of Widget itself.
This approach is used in order to provide the user with an easy way to
override the default functions associated with the widget.

To customize a widget, create a subclass of Widget which:
- 1. Overrides the `self.resources` attribute to specify the Resources which are needed for functioning, and
- 2. Overrides the `.viz()` method to provide interactivity based on the values provided to those Resources.
- 3. Optionally overrides the `.prep()` method to perform any tasks which must take place before the Resources are run.

To allow for a good amount of flexibility in creating Widgets which are
based on specific visualization suites (e.g., the StreamlitWidget described below),
the methods used in each Widget are as follows:

- `.run_cli()`: Used for functionality when being run from the command line
- `.to_html()`: Stub for authoring HTML with the live contents of the widget
- `.to_script()`: Stub for authoring a Python script with the live contents of the widget
- `.download_html_button()`: Render a button allowing the user to download the live widget as HTML
- `.download_script_button()`: Render a button allowing the user to download the live widget as a Python script
- `._source()`: Return the source code for this live widget as a string

### Streamlit-Based Widgets

All of the framework provided for the `Widget` object above is intended to make
it easier to develop widgets which are based on different visualization frameworks.
By itself, the `Widget` object is likely useless, but it provides a base class
which can be overridden with platform-specific code.

#### StResource

The Streamlit-based Resource class presents the user with an updated interface
by:

- 1. Setting up an empty container inside the `container` passed to `run()`;
- 2. Defining an `update_ui()` method which populates that container;
- 3. Adding an `update=bool` flag to the `set()` method which will trigger the `update_ui()` method;
- 4. Adding a base `on_change()` method which assigns the value of the Streamlit session state to the `value` attribute of the object.

#### StResourceList

The Streamlit-based ResourceList class passes along the `update=` flag to
the `set()` and `set_value()` methods for the `StResource` objects that it
contains.

In addition, the `run(container, sidebar=True)` method has been overridden such that:
- If the `container` is `None`, a new `st.container()` will be set up (optionally in the sidebar)
- Otherwise, a new container will be created (`container.container()`)

The resulting container will be passed in to the `run()` method for
each of the Resources in the list.

#### StWidget

The Streamlit-based Widget class provides working examples of the methods for:

- `run_cli()`: Run the widget from the command line
- `download_html_button()`: Render a button which allows the user to download the widget as HTML
- `download_script_button()`: Render a button which allows the user to download the widget as code
- `to_html()`: Create an HTML file which will load this widget using the `stlite` library, based on `pyodide`
- `to_script()`: Create a python script which will be used to load this widget

In addition to the `resources` attribute and the `viz()` method, users can
override the `requirements` attribute to provide a list of packages which
should be loaded by `pyodide` prior to running the widget, as well as
`imports` which defines the way in which packages are loaded into the namespace
before running the widget code itself.

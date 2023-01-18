# widgets
Merging code and data in webpages

[![Build Python package](https://github.com/FredHutch/widgets/actions/workflows/package.yaml/badge.svg)](https://github.com/FredHutch/widgets/actions/workflows/package.yaml)

[![Lint and run tests](https://github.com/FredHutch/widgets/actions/workflows/lint.yaml/badge.svg)](https://github.com/FredHutch/widgets/actions/workflows/lint.yaml)

[![Coverage](https://github.com/FredHutch/widgets/actions/workflows/lint.yaml/coverage.svg)](https://github.com/FredHutch/widgets/actions/workflows/lint.yaml)

## Purpose

While the technical skills required for visualizing data have become vastly more
accessible in recent years, there are still a large number of people who would like
to be able to easily visualize their data without the need for writing any code
whatsoever.

To provide a no-code data visualization experience, we introduce "widgets" - a
flexible framework for merging data and code into a single standalone file which
can be rendered by a modern web browser into a wide array of data visualizations.

## How Widgets Work

Let's say that you're using a widget which is used to make volcano plots (a
commonly-used way to show which genes are expressed differently in two groups
of samples, for example).
When you open the widget, it loads directly in your web browser.
You don't need to install anything on your computer in order to open it.
The volcano plot widget needs a table of data to display, which you can upload
as a CSV or Excel spreadsheet.
Once you've uploaded your data and customized your plot, you can now download
a new copy of that widget _which has your data embedded in it_.
That new version of the widget will be an HTML file, which means that it can
be opened in a web browser.
When you open up that copy of the widget, your data will load directly and be
displayed in the same way as when you downloaded the copy.
Another way of thinking about widgets is that they are a way of taking your data
and embedding them directly into a customized visualization which can be opened
on any computer.

## How to Make a New Widget

To create your own widget, simply make a Python script which defines the
behavior of the widget, including the data provided by users, the Python
packages that it requires, and the visualization which will be displayed.

The interactivity of the widget shown below is based on the [Streamlit](https://streamlit.io/)
library.
Streamlit [provides support for Matplotlib, Plotly, Bokeh, Altair, and other plotting libraries](https://docs.streamlit.io/),
as well as flexible user inputs.

An example script is shown below:

```#!/usr/bin/env python3

# The import statement at the top of the script is used
# during local development and will not cause any modules
# to be imported after conversion to HTML

import pandas as pd
import streamlit as st
from widgets.streamlit.widget import StreamlitWidget
from widgets.streamlit.resources.dataframe import StDataFrame
from widgets.streamlit.resources.value import StString
import plotly.express as px


# Give the widget a descriptive name
class SimpleWidget(StreamlitWidget):

    # This app will prompt the user to provide four inputs,
    # one StDataFrame (which can be provided as CSV), and
    # three string values.
    # The data provided for each of these elements will be
    # available in the `viz()` scope using the `self.data` object

    resources = [
        StDataFrame(
            id="df",
            default=pd.DataFrame(dict(x=[], y=[], label=[])),
            label="Test CSV",
        ),
        StString(id="x_col", default="x", label="X-axis Column"),
        StString(id="y_col", default="y", label="Y-axis Column"),
        StString(id="label_col", default="label", label="Label Column")
    ]

    # Specify any packages which should be installed prior to loading

    requirements = [
        "widgets",
        "pandas",
        "plotly"
    ]

    # Specify any inputs statements which are needed by the widget
    # beyond the following (which will be executed by default):
    #   import streamlit as st
    #   from widgets.streamlit.resources.dataframe import StDataFrame
    #   from widgets.streamlit.resources.value import String, Integer, Float
    #   from widgets.streamlit.widget import StreamlitWidget

    extra_imports = [
        "import pandas as pd",
        "import plotly.express as px"
    ]

    # The visualization defined in the `viz` function will be run and
    # updated every time a user changes the inputs, showing a simple
    # scatterplot.
    def viz(self):

        if st.session_state.df is not None and self.data["df"].shape[0] > 0:

            fig = px.scatter(
                data_frame=self.data["df"],
                x=self.data["x_col"],
                y=self.data["y_col"],
                hover_name=self.data["label_col"]
            )

            st.plotly_chart(fig)

        else:

            st.write("Please provide data to plot")

```

### Developing Widgets Safely

**Extremely Important:**
When you execute any command on a file containing code (e.g. running
a widget or converting it to HTML), that code *will be run on your computer*.
Do not run any file that contains code which you do not trust.

### Local Testing

To test the widget locally (before converting to HTML), install
the `widgets` library (`pip3 install widgets-lib`) and run:

```#!/bin/bash
# Where app.py is the file containing the code for SimpleWidget
widgets run app.py SimpleWidget
```

When you edit the file `app.py`, the interactive display in your
web browser will give you the option to update with those changes.
This auto-update functionality (provided by Streamlit) makes it easy
to quickly tweak your code until it meets your needs.

### Create HTML

After testing locally, the widget code can be converted to an HTML
file.
To create that file, you must specify both the file containing the
code (in this case `app.py`) as well as the name of the widget which
you defined (in this case `SimpleWidget`).

```#!/bin/bash
# To create a file called widget.html
widgets tohtml app.py SimpleWidget

# The complete list of options provided can be seen with
widgets tohtml --help
```

## Under the Hood

The widgets created using this software library are only possible
due to the advances which have been make in running Python within
web browsers (IE, Chrome, Firefox, Safari, etc.) via the
[Pyodide project](https://pyodide.org/).

While Python is an amazingly popular and powerful programming
language, it still requires a basic familiarity with software
development which requires time and energy to develop.
Being able to run Python in the web browser opens up a whole
new world of opportunity for delivering software to an even
wider audience of users.

Special thanks goes to [Yuichiro Tachibana](https://github.com/whitphx),
who created an adapter which allows Streamlit-based apps to run
via Pyodide.
While the `widgets` concept is not unique to Streamlit, this
has provided the initial implementation which is enormously
useful.

When you open a widget in the web browser, the first step is
for Pyodide to load and install all of the packages which are
needed.
This can be a time-consuming process, and so you should expect
widgets to load extremely slowly when you first open them.
The loading process will hopefully speed up over time, but
you should definitely tell users to expect slow load times.

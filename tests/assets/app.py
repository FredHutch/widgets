from widgets.base.widget import Widget
from widgets.streamlit.widget import StreamlitWidget


class SimpleWidget(Widget):

    pass

class SimpleStWidget(StreamlitWidget):

    pass

class SimpleWidgetNoBase:
    """
    Used to make sure that an error is raised when a widget is imported
    which is not based on the Widget class.
    """

    pass

import os
from widgets.streamlit.resources.base import StreamlitResource


class Value(StreamlitResource):
    """Generic class used for value resources."""

    def read(self):
        """Read the saved value, if present."""

        # Define the filepath used by the saved value
        filepath = f"{self.id}.txt"

        if os.path.exists(filepath):
            with open(filepath) as handle:
                value = handle.readline()
            return self.datatype(value)
        else:
            return    


class String(Value):
    """String value resource used for Streamlit-based widgets."""

    datatype = str


class Integer(Value):
    """Integer value resource used for Streamlit-based widgets."""

    datatype = int


class Float(Value):
    """Float value resource used for Streamlit-based widgets."""

    datatype = float
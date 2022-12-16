import os
from typing import Union
import pandas as pd
from widgets.streamlit.resources.base import StreamlitResource


class DataFrame(StreamlitResource):
    """
    DataFrame resource used in a Streamlit-based widget.
    """

    datatype = pd.DataFrame

    def read(self) -> Union[pd.DataFrame, None]:
        """Read the saved DataFrame, if present."""

        # Define the filepath used by the saved value
        filepath = f"{self.id}.csv.gz"

        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        else:
            return
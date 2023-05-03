import binascii
from typing import Any
from jinja2 import Environment, PackageLoader
import json
import pandas as pd
from widgets.base.exceptions import ResourceConfigurationException
import zlib


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


def compress_string(string_to_compress: str):
    """Compress a string input."""

    # Compress the string with zlib
    compressed_bytes = zlib.compress(string_to_compress.encode())

    # Convert the compressed bytes to a bitshifted encoding
    # for compatibility with being saved in a text file
    bitshifted_encoding = binascii.b2a_hex(compressed_bytes)

    return bitshifted_encoding.decode()


def decompress_string(string_to_decompress: str):
    """Decompress a compressed input."""

    # Convert the bitshifted encoding to compressed bytes
    compressed_bytes = binascii.a2b_hex(string_to_decompress)

    # Decompress the bytes to retrieve the original string
    original_string = zlib.decompress(compressed_bytes)

    # Decode the original string from bytes to a string
    original_string = original_string.decode()

    return original_string


def parse_dataframe_string(value) -> pd.DataFrame:

    # If the value is a string, try to decompress it
    if isinstance(value, str):
        try:
            value = json.loads(decompress_string(value))
        except Exception as e:
            msg = f"value could not be decompressed from string ({str(e)})"
            raise ResourceConfigurationException(msg)

    # If the value is a dict, convert it
    if isinstance(value, dict):

        # If the dict appears to be a "split" DataFrame
        if all(
            [
                cname in value.keys()
                for cname in ['index', 'columns', 'data']
            ]
        ):
            try:
                value = pd.DataFrame(**value)
            except Exception as e:
                msg = f"value could not be converted to DataFrame ({str(e)})"
                raise ResourceConfigurationException(msg)

        # If not, just parse it as a normal DataFrame constructor
        else:
            try:
                value = pd.DataFrame(value)
            except Exception as e:
                msg = f"value could not be converted to DataFrame ({str(e)})"
                raise ResourceConfigurationException(msg)

    # If the value is a DataFrame, keep it
    elif isinstance(value, pd.DataFrame):
        pass
    # If the value is None, make an empty DataFrame
    elif value is None:
        value = pd.DataFrame()
    else:
        msg = f"value must be None, dict, or DataFrame, not {type(value)}"
        raise ResourceConfigurationException(msg)

    return value


def encode_dataframe_string(val: pd.DataFrame) -> str:

    # Convert to dict
    val_dict = val.to_dict(orient="split")
    # Convert to string
    val_str = json.dumps(val_dict)
    # Compress the string
    val_comp = compress_string(val_str)

    # If the compressed string is shorter
    if len(val_comp) < len(val_str):

        # Return the compressed version,
        # embedded in quotes
        return f'"{val_comp}"'
    # If the compressed string is longer
    else:
        # Return the JSON serialization
        return val_str


def decompress_json(vals) -> Any:

    # If the input is a string, try to decompress it
    if isinstance(vals, str):
        try:
            vals = json.loads(
                decompress_string(vals)
            )
        except Exception as e:
            msg = f"vals could not be decompressed from string ({str(e)})"
            raise ResourceConfigurationException(msg)

    # If the input is not a string, just return it

    return vals


def compress_json(vals) -> str:

    # Convert to string
    vals_str = json.dumps(vals)
    # Compress the string
    vals_comp = compress_string(vals_str)

    # Return the compressed version,
    # embedded in quotes
    return f'"{vals_comp}"'

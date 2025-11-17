# In rasp/__init__.py

from .parser import rasp_get, parse_ras_data

# Define the package version
__version__ = "0.1.0" 

# Optional: Define a simple usage function
def load(filepath):
    """Loads and parses RAS data from a file."""
    with open(filepath, 'r') as f:
        return parse_ras_data(f.read())


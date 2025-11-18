# In rasp/__init__.py

from .parser import get, parse_ras_data, convert
from typing import Any, Dict, List

# Define the package version
__version__ = "0.1.1" 

# Optional: Define a simple usage function
def load(filepath: str) -> Dict[str, List[List[Any]]]:
    """Loads and parses RAS data from a file."""
    with open(filepath, 'r') as f:
        return parse_ras_data(f.read())


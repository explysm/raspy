import csv
from io import StringIO
import os
import json
from typing import Any, Dict, List, Optional, Union

# --- Core Type Conversion Logic ---

def try_convert_to_type(value: str) -> Union[str, int, float, bool]:
    """
    Converts an unquoted value string to a Python type (Bool, Int, or Float).
    Handles quoted strings by stripping the quotes.
    
    Rules:
    - "True" / "False" (unquoted) -> Boolean
    - '123' (unquoted) -> Integer
    - '3.14' (unquoted) -> Float
    - '"text"' (quoted) -> String (without quotes)
    """
    if not isinstance(value, str):
        return value

    # 1. Handle Strings (Must be quoted in RAS format)
    # Note: csv.reader will strip surrounding whitespace, but we confirm quotes
    if value.startswith('"') and value.endswith('"') and len(value) > 1:
        return value.strip('"') 

    # 2. Handle Booleans (Unquoted keywords)
    if value == "True":
        return True
    if value == "False":
        return False
        
    # 3. Handle Numbers (Unquoted)
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        # 4. Handle Unquoted Identifiers (e.g., 'product1' which isn't a number/boolean)
        return value


# --- Main Parsing Function ---

def parse_ras_data(ras_content: str) -> Dict[str, List[List[Any]]]:
    """
    Parses RAS content into a dictionary where keys are list names.
    
    Format Rules:
    - List opening: listname-
    - List closing: +
    - Items are comma-separated, honoring quotes.
    """
    
    ras_data = {}
    current_list_name = None
    list_content = ""
    
    # Process line by line
    for line in ras_content.strip().split('\n'):
        line = line.strip()
        
        # Ignore comment lines
        if line.startswith('#'):
            continue
        
        # Check for list opening (e.g., "products-")
        if line.endswith('-') and not line.startswith('+') and len(line) > 1:
            # Finalize previous list if any
            if current_list_name and list_content:
                reader = csv.reader(StringIO(list_content), skipinitialspace=True)
                ras_data[current_list_name] = [
                    [try_convert_to_type(field) for field in item]
                    for item in reader if item
                ]
            
            # Start new list
            current_list_name = line[:-1]
            list_content = ""
        
        # Check for list closing (+)
        elif line == '+':
            if current_list_name and list_content:
                # Use the CSV reader to handle quoted strings and commas within lines
                # The 'skipinitialspace=True' argument helps with formatting
                reader = csv.reader(StringIO(list_content), skipinitialspace=True)
                
                # Convert the reader object into a list of items and apply type conversion
                ras_data[current_list_name] = [
                    [try_convert_to_type(field) for field in item]
                    for item in reader if item
                ]
            current_list_name = None
            list_content = ""
            
        # Data line within a list
        elif current_list_name and line:
            # Strip inline comments (assuming they start with # and are at the end of the line)
            if '#' in line:
                line = line.split('#', 1)[0].strip()
            if line: # Only add if line is not empty after stripping comment
                list_content += line + '\n' # Append data line for CSV reader

    # Handle the case where the file ends without a closing '+'
    if current_list_name and list_content:
        reader = csv.reader(StringIO(list_content), skipinitialspace=True)
        ras_data[current_list_name] = [
            [try_convert_to_type(field) for field in item]
            for item in reader if item
        ]
            
    return ras_data


# --- User-Facing Access Function ---

def get(file_path: str, list_name: str, item_index: int, sub_item_index: int, data_store: Optional[Dict[str, List[List[Any]]]] = None) -> Any:
    """
    Accesses a specific value using the RAS indexing logic.
    
    :param file_path: The path to the RAS data file (used only if data_store is None).
    :param list_name: The name of the top-level list (e.g., "products").
    :param item_index: The zero-based index of the line/record in the list.
    :param sub_item_index: The zero-based index of the field in the line (0 is the key).
    :param data_store: Optional. An already parsed RAS data dictionary. If None, the file_path will be used to parse the data.
    :return: The retrieved value with its correct Python type.
    """
    if data_store is None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"RAS Error: File not found at '{file_path}'.")

        with open(file_path, 'r') as f:
            ras_content = f.read()

        data_store = parse_ras_data(ras_content)

    if list_name not in data_store:
        raise KeyError(f"RAS Error: List '{list_name}' not found in data store.")
        
    item_list = data_store[list_name]
    
    if item_index >= len(item_list) or item_index < 0:
        raise IndexError(f"RAS Error: Item index {item_index} out of bounds for list '{list_name}'.")
        
    item = item_list[item_index]
    
    if sub_item_index >= len(item) or sub_item_index < 0:
        raise IndexError(f"RAS Error: Sub-item index {sub_item_index} out of bounds for item at index {item_index}.")
        
    return item[sub_item_index]

def convert(ras_file_path: str, data_type: str, output_file_path: str) -> None:
    """
    Converts a RAS file to a specified data format and saves it to an output file.

    :param ras_file_path: Path to the input RAS file.
    :param data_type: The target data type for conversion (e.g., "json").
    :param output_file_path: Path where the converted data will be saved.
    """
    if not os.path.exists(ras_file_path):
        raise FileNotFoundError(f"RAS Error: Input file not found at '{ras_file_path}'.")

    with open(ras_file_path, 'r') as f:
        ras_content = f.read()

    parsed_data = parse_ras_data(ras_content)

    if data_type.lower() == "json":
        try:
            with open(output_file_path, 'w') as outfile:
                json.dump(parsed_data, outfile, indent=4)
            print(f"Successfully converted '{ras_file_path}' to JSON and saved to '{output_file_path}'.")
        except IOError as e:
            raise IOError(f"RAS Error: Could not write to output file '{output_file_path}'. Reason: {e}")
    else:
        raise ValueError(f"RAS Error: Unsupported data type for conversion: '{data_type}'. Currently only 'json' is supported.")

# --- Usage Example (for testing) ---

if __name__ == '__main__':
    # Create a dummy RAS file for testing
    dummy_ras_content = """
products-
product1,"The first item",1,"tbh"
item_2,"Another Item, with a comma",42,"done"
+
status-
product1,True,45
item_2,False,100
+
prices-
milk,2.99
bread,3.50
+
"""
    dummy_file_path = "dummy_data.ras"
    with open(dummy_file_path, "w") as f:
        f.write(dummy_ras_content)

    print("--- Parsed Data Store (Internal View) ---")
    # For internal view, we still need to parse content directly
    data_store_internal = parse_ras_data(dummy_ras_content)
    print(data_store_internal)
    print("------------------------------------------")

    # Access Examples using the new rasp_get with file path
    print(f"Key for first product: {get(dummy_file_path, 'products', 0, 0)} (Type: {type(get(dummy_file_path, 'products', 0, 0)).__name__})")
    print(f"Boolean status: {get(dummy_file_path, 'status', 1, 1)} (Type: {type(get(dummy_file_path, 'status', 1, 1)).__name__})")
    print(f"Float price: {get(dummy_file_path, 'prices', 0, 1)} (Type: {type(get(dummy_file_path, 'prices', 0, 1)).__name__})")
    print(f"String with comma: {get(dummy_file_path, 'products', 1, 1)} (Type: {type(get(dummy_file_path, 'products', 1, 1)).__name__})")

    print("\n--- Convert Example ---")
    json_output_path = "dummy_data.json"
    convert(dummy_file_path, "json", json_output_path)
    print(f"Converted JSON content:\n{open(json_output_path).read()}")
    os.remove(json_output_path)

    # Clean up the dummy file
    os.remove(dummy_file_path)
    


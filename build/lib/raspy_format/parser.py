import csv
from io import StringIO
import os

# --- Core Type Conversion Logic ---

def try_convert_to_type(value):
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

def parse_ras_data(ras_content):
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

def rasp_get(file_path, list_name, item_index, sub_item_index):
    """
    Accesses a specific value using the RAS indexing logic from a file.
    
    :param file_path: The path to the RAS data file.
    :param list_name: The name of the top-level list (e.g., "products").
    :param item_index: The zero-based index of the line/record in the list.
    :param sub_item_index: The zero-based index of the field in the line (0 is the key).
    :return: The retrieved value with its correct Python type.
    """
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
    print(f"Key for first product: {rasp_get(dummy_file_path, 'products', 0, 0)} (Type: {type(rasp_get(dummy_file_path, 'products', 0, 0)).__name__})")
    print(f"Boolean status: {rasp_get(dummy_file_path, 'status', 1, 1)} (Type: {type(rasp_get(dummy_file_path, 'status', 1, 1)).__name__})")
    print(f"Float price: {rasp_get(dummy_file_path, 'prices', 0, 1)} (Type: {type(rasp_get(dummy_file_path, 'prices', 0, 1)).__name__})")
    print(f"String with comma: {rasp_get(dummy_file_path, 'products', 1, 1)} (Type: {type(rasp_get(dummy_file_path, 'products', 1, 1)).__name__})")

    # Clean up the dummy file
    os.remove(dummy_file_path)
    


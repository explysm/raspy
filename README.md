# raspy-format: A Lightweight RAS Data Parser

A Python library for parsing and accessing data from custom Raspberry (RAS) format files.

## 💡 Overview

`raspy-format` is a Python library designed for efficient parsing and retrieval of data from files structured in the custom Raspberry (RAS) format. This format is built around named, line-delimited lists, where each entry is a comma-separated record capable of distinguishing between quoted strings and unquoted numerical or boolean values.

## Key Features
 * Type Safe: Automatically converts unquoted values into native Python types (int, float, bool).
 * List-Indexed Access: Provides a powerful rasp_get() function for specific data retrieval via list name, item index, and sub-item index.
 * CSV Compliant: Correctly handles quoted strings that contain internal commas.

## 🛠️ Installation
You can install raspy-format using pip:
```bash
pip install raspy-format
```

## 📝 RAS Format Syntax

The RAS format defines data lists using specific opening and closing delimiters, with comma-separated fields within each list.

| Element | Syntax | Description |
|---|---|---|
| List Opening | `listname-` | Starts a named data list. |
| List Closing | `+` | Closes the current data list. |
| Item Separation | `,` | Separates fields within a data line. |

### Data Type Rules

| Type | Rule | Example in RAS | Python Type |
|---|---|---|---|
| String | MUST be double-quoted. | `"My Value"` | `str` |
| Integer | MUST NOT be quoted. | `42` | `int` |
| Float | MUST NOT be quoted. | `2.99` | `float` |
| Boolean | MUST NOT be quoted (`True`/`False`). | `True` | `bool` |

### Example RAS File (`data.ras`)

```ras
products-
item_alpha,"Alpha Product Description",100,"Warehouse A"
item_beta,"Beta Product, with comma",42,"Warehouse B"
+
status-
product1,True,45
item_2,False,100
+
```

## 🚀 Usage

The library provides two primary functions: `parse_ras_data` and the main access function, `rasp_get`.

### 1. Parsing the Data

To parse RAS data, you typically load it from a file. Ensure you have a `data.ras` file (as shown in the example above) in your project or specify its full path.

```python
import raspy_format
import os

# Assuming data.ras is in the same directory as your script
data_file_path = "data.ras" 

# Use the convenience loader (defined in __init__.py)
data_store = raspy_format.load(data_file_path)

# Alternatively, parse content directly:
# with open(data_file_path, 'r') as f:
#     content = f.read()
#     data_store = raspy_format.parse_ras_data(content)

print(data_store)
# Expected Output (dictionary of lists):
# {
#     'products': [
#         ['item_alpha', 'Alpha Product Description', 100, 'Warehouse A'],
#         ['item_beta', 'Beta Product, with comma', 42, 'Warehouse B']
#     ],
#     'status': [
#         ['product1', True, 45],
#         ['item_2', False, 100]
#     ]
# }
```

### 2. Accessing Specific Values with `rasp_get()`

The `rasp_get()` function directly takes a file path and uses a three-part index for precise retrieval:

| Argument | Description | Indexing |
|---|---|---|
| `file_path` | The path to the RAS data file. | |
| `list_name` | The name of the top-level list (e.g., `"products"`). | |
| `item_index` | The zero-based line number within the list. | `0` is the first item. |
| `sub_item_index` | The zero-based field number on that line. | `0` is always the item's key. |

#### Retrieval Examples

```python
# First, ensure you have a data.ras file in the current directory or specify its full path.
# For this example, let's assume 'data.ras' is in the same directory as your script.
data_file_path = "data.ras" # Or provide the full path

# 1. Get the stock level (sub-item 2) for item_alpha (item index 0)
stock_level = raspy_format.rasp_get(data_file_path, "products", 0, 2)
print(f"Stock: {stock_level} (Type: {type(stock_level).__name__})")
# Output: Stock: 100 (Type: int)

# 2. Get the name/description (sub-item 1) for item_beta (item index 1)
description = raspy_format.rasp_get(data_file_path, "products", 1, 1)
print(f"Description: {description}")
# Output: Description: Beta Product, with comma

# 3. Check the availability boolean (sub-item 1) for product1 (item index 0)
is_available = raspy_format.rasp_get(data_file_path, "status", 0, 1)
print(f"Available: {is_available} (Type: {type(is_available).__name__})")
# Output: Available: True (Type: bool)
```

## ⚙️ Development and Contribution
If you find issues or want to expand the features (e.g., adding comment support, nested lists), feel free to open a pull request on the official repository.

### Running Tests

To run the tests, use `pytest`:

```bash
pytest
```

### Building the Package
```bash
python setup.py sdist bdist_wheel
```

## 📜 License
This project is licensed under the MIT License.
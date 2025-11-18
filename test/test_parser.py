import pytest
import os
from raspy_format.parser import parse_ras_data, get

# Define a dummy RAS content for testing
DUMMY_RAS_CONTENT = """
# This is a comment for products list
products-
product1,"The first item",1,"tbh" # Inline comment
item_2,"Another Item, with a comma",42,"done"
+
# This is a comment for status list
status-
product1,True,45
# Another comment line
item_2,False,100
+
prices-
milk,2.99
bread,3.50
+
"""

@pytest.fixture
def ras_file(tmp_path):
    """
    Pytest fixture to create a temporary RAS file for testing.
    """
    file_path = tmp_path / "test.ras"
    file_path.write_text(DUMMY_RAS_CONTENT)
    return str(file_path)

def test_parse_ras_data(ras_file):
    """
    Test the parse_ras_data function.
    """
    with open(ras_file, 'r') as f:
        content = f.read()
    
    data = parse_ras_data(content)
    
    assert isinstance(data, dict)
    assert "products" in data
    assert "status" in data
    assert "prices" in data
    
    assert len(data["products"]) == 2
    assert data["products"][0] == ['product1', 'The first item', 1, 'tbh']
    assert data["products"][1] == ['item_2', 'Another Item, with a comma', 42, 'done']
    
    assert len(data["status"]) == 2
    assert data["status"][0] == ['product1', True, 45]
    assert data["status"][1] == ['item_2', False, 100]
    
    assert len(data["prices"]) == 2
    assert data["prices"][0] == ['milk', 2.99]
    assert data["prices"][1] == ['bread', 3.50]

def test_get_from_file(ras_file):
    """
    Test the get function when reading directly from a file.
    """
    assert get(ras_file, "products", 0, 0) == "product1"
    assert get(ras_file, "products", 0, 1) == "The first item"
    assert get(ras_file, "products", 0, 2) == 1
    assert get(ras_file, "products", 0, 3) == "tbh"
    
    assert get(ras_file, "products", 1, 1) == "Another Item, with a comma"
    assert get(ras_file, "status", 0, 1) == True
    assert get(ras_file, "status", 1, 2) == 100
    assert get(ras_file, "prices", 0, 1) == 2.99

def test_get_from_data_store(ras_file):
    """
    Test the get function when provided with a pre-parsed data_store.
    """
    with open(ras_file, 'r') as f:
        content = f.read()
    data_store = parse_ras_data(content)

    assert get(ras_file, "products", 0, 0, data_store=data_store) == "product1"
    assert get(ras_file, "products", 1, 1, data_store=data_store) == "Another Item, with a comma"
    assert get(ras_file, "status", 0, 1, data_store=data_store) == True
    assert get(ras_file, "prices", 0, 1, data_store=data_store) == 2.99

def test_get_file_not_found():
    """
    Test FileNotFoundError for get function.
    """
    with pytest.raises(FileNotFoundError):
        get("non_existent_file.ras", "products", 0, 0)

def test_get_list_not_found(ras_file):
    """
    Test KeyError for get function when list is not found.
    """
    with pytest.raises(KeyError):
        get(ras_file, "non_existent_list", 0, 0)

def test_get_item_index_out_of_bounds(ras_file):
    """
    Test IndexError for get function when item index is out of bounds.
    """
    with pytest.raises(IndexError):
        get(ras_file, "products", 99, 0) # Too high
    with pytest.raises(IndexError):
        get(ras_file, "products", -1, 0) # Negative

def test_get_sub_item_index_out_of_bounds(ras_file):
    """
    Test IndexError for get function when sub-item index is out of bounds.
    """
    with pytest.raises(IndexError):
        get(ras_file, "products", 0, 99) # Too high
    with pytest.raises(IndexError):
        get(ras_file, "products", 0, -1) # Negative

def test_parse_ras_data_with_comments(ras_file):
    """
    Test the parse_ras_data function with content containing comments.
    Ensure comments are ignored and data is parsed correctly.
    """
    # The ras_file fixture already uses DUMMY_RAS_CONTENT which now includes comments.
    # So, we just need to parse it and assert the content is correct (i.e., comments are absent).
    with open(ras_file, 'r') as f:
        content = f.read()
    
    data = parse_ras_data(content)
    
    assert isinstance(data, dict)
    assert "products" in data
    assert "status" in data
    assert "prices" in data
    
    assert len(data["products"]) == 2
    assert data["products"][0] == ['product1', 'The first item', 1, 'tbh']
    assert data["products"][1] == ['item_2', 'Another Item, with a comma', 42, 'done']
    
    assert len(data["status"]) == 2
    assert data["status"][0] == ['product1', True, 45]
    assert data["status"][1] == ['item_2', False, 100]
    
    assert len(data["prices"]) == 2
    assert data["prices"][0] == ['milk', 2.99]
    assert data["prices"][1] == ['bread', 3.50]
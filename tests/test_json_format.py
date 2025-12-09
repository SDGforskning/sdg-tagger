import json
import pytest
import os
import sys
from jsonschema import validate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.mark.json_format
@pytest.mark.parametrize(
    'input_filename', 
    [
        "sdg1.json",
        "sdg2.json",
        "sdg3.json",
        "sdg4.json",
        "sdg5.json",
        "sdg6.json",
        "sdg7.json",
        "sdg8.json",
        "sdg9.json",
        "sdg10.json",
        "sdg11.json",
        "sdg12.json",
        "sdg13.json",
        "sdg14.json",
        "sdg15.json",
        "sdg16.json",

        "sdg1_template.json",
        "sdg2_template.json",
        "sdg3_template.json",
        "sdg4_template.json",
        "sdg7_template.json",
        "sdg11_template.json",
        "sdg12_template.json",
        "sdg13_template.json",
        "sdg14_template.json",
        "sdg15_template.json",
    ]
)
def test_json_format(input_filename):
    if not os.path.isfile("src/phrases/" + input_filename):
        pytest.skip(f"The file {input_filename} does not exist.")
    # Arrange
    with open("src/phrases/" + input_filename) as file:
        content = json.load(file)
    schema = "tests/json_schema/sdg_schema.json"
    with open(schema) as file:
        json_schema = json.load(file)
    
    # Act
    result = validate(instance=content, schema=json_schema)
    # Assert
    assert result==None

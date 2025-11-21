"""
Test suite for universal_field_editor_V2.py

This test suite demonstrates usage of the Universal Field Editor and verifies
core functionality. Run with: pytest test_universal_field_editor_V2.py -v

Note: Tests that require API calls are marked with @pytest.mark.integration
and will be skipped by default. Run with --integration to include them.
"""

import pytest
import sys
import os
import json

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import universal_field_editor_V2 as editor


class TestPrimitiveFormatter:
    """Test the primitive_formatter function"""

    def test_single_value_non_multiple_field(self):
        """Test formatting a single value for a non-multiple field"""
        change_area = "title:title"
        row = {"title:title": "New Title"}
        field = {
            "typeName": "title",
            "multiple": False,
            "typeClass": "primitive",
            "value": "Old Title"
        }

        result = editor.primitive_formatter(change_area, row, field)

        assert isinstance(result, dict)
        assert result["value"] == "New Title"
        print(f"Single value result: {json.dumps(result, indent=2)}")

    def test_single_value_multiple_field(self):
        """Test formatting a single value for a multiple field"""
        change_area = "alternativeTitle:alternativeTitle"
        row = {"alternativeTitle:alternativeTitle": "Subtitle 1"}
        field = {
            "typeName": "alternativeTitle",
            "multiple": True,
            "typeClass": "primitive",
            "value": ["Old Subtitle"]
        }

        result = editor.primitive_formatter(change_area, row, field)

        assert isinstance(result, dict)
        assert result["value"] == ["Subtitle 1"]
        print(f"Multiple field single value result: {json.dumps(result, indent=2)}")

    def test_multiple_values_split_by_plus(self):
        """Test splitting multiple values separated by '+'"""
        change_area = "alternativeTitle:alternativeTitle"
        row = {"alternativeTitle:alternativeTitle": "Title 1+Title 2+Title 3"}
        field = {
            "typeName": "alternativeTitle",
            "multiple": True,
            "typeClass": "primitive",
            "value": ["Old Title"]
        }

        result = editor.primitive_formatter(change_area, row, field)

        assert isinstance(result, dict)
        assert result["value"] == ["Title 1", "Title 2", "Title 3"]
        print(f"Multiple values result: {json.dumps(result, indent=2)}")

    def test_empty_value_returns_empty_dict_value(self):
        """Test that empty values result in empty value field"""
        change_area = "title:title"
        row = {"title:title": ""}
        field = {
            "typeName": "title",
            "multiple": False,
            "typeClass": "primitive",
            "value": "Old Title"
        }

        result = editor.primitive_formatter(change_area, row, field)

        # Empty string should result in field with empty value
        assert result == ""


class TestCompoundFormatter:
    """Test the compound_formatter function"""

    def test_single_compound_field_with_multiple_primitives(self):
        """Test a compound field with multiple primitive sub-fields"""
        header = "author:authorName;authorAffiliation"
        row = {"author:authorName;authorAffiliation": "Smith, John;University of Toronto"}

        result = editor.compound_formatter(header, row)

        assert isinstance(result, list)
        assert len(result) == 1
        assert "authorName" in result[0]
        assert "authorAffiliation" in result[0]
        assert result[0]["authorName"]["value"] == "Smith, John"
        assert result[0]["authorAffiliation"]["value"] == "University of Toronto"
        print(f"Single compound field result: {json.dumps(result, indent=2)}")

    def test_multiple_compound_entries_with_plus(self):
        """Test multiple compound entries separated by '+'"""
        header = "author:authorName;authorAffiliation"
        row = {"author:authorName;authorAffiliation": "Smith, John;U of T+Jane Doe;York University"}

        result = editor.compound_formatter(header, row)

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["authorName"]["value"] == "Smith, John"
        assert result[0]["authorAffiliation"]["value"] == "U of T"
        assert result[1]["authorName"]["value"] == "Jane Doe"
        assert result[1]["authorAffiliation"]["value"] == "York University"
        print(f"Multiple compound entries result: {json.dumps(result, indent=2)}")

    def test_empty_value_returns_false(self):
        """Test that empty values return False"""
        header = "author:authorName;authorAffiliation"
        row = {"author:authorName;authorAffiliation": ""}

        result = editor.compound_formatter(header, row)

        assert result is False

    def test_whitespace_handling(self):
        """Test that whitespace is properly stripped from values"""
        header = "author:authorName;authorAffiliation"
        row = {"author:authorName;authorAffiliation": "Smith, John ; University of Toronto "}

        result = editor.compound_formatter(header, row)

        assert result[0]["authorName"]["value"] == "Smith, John"
        assert result[0]["authorAffiliation"]["value"] == "University of Toronto"


class TestRecordCheck:
    """Test the record_check function"""

    def test_empty_list_returns_empty_string(self):
        """Test that empty list returns empty string"""
        field = {"typeName": "title", "value": "Old"}
        result = editor.record_check([''], field)
        assert result == ""

    def test_empty_string_returns_empty_string(self):
        """Test that empty string returns empty string"""
        field = {"typeName": "title", "value": "Old"}
        result = editor.record_check('', field)
        assert result == ""

    def test_valid_string_updates_field(self):
        """Test that valid string updates field value"""
        field = {"typeName": "title", "value": "Old Title"}
        result = editor.record_check("New Title", field.copy())
        assert result["value"] == "New Title"

    def test_valid_list_updates_field(self):
        """Test that valid list updates field value"""
        field = {"typeName": "title", "value": ["Old"]}
        result = editor.record_check(["New1", "New2"], field.copy())
        assert result["value"] == ["New1", "New2"]


class TestXmlSelecter:
    """Test the xml_selecter function"""

    def test_select_citation_block(self):
        """Test selecting citation metadata block"""
        headers = ["doi", "MARKER 1", "title:title", "subtitle:subtitle"]

        result = editor.xml_selecter(headers)

        assert isinstance(result, list)
        assert len(result) == 3

        directory, block, master_list = result

        assert block == "citation"
        assert "title" in directory
        assert "author" in directory
        assert isinstance(master_list, list)
        assert len(master_list) == 3  # primitive, compound, controlled_vocab

        print(f"Citation block - Directory keys: {list(directory.keys())[:5]}...")
        print(f"Citation block - Master list: {master_list}")

    def test_select_socialscience_block(self):
        """Test selecting social science metadata block"""
        headers = ["doi", "MARKER 2", "unitOfAnalysis:unitOfAnalysis"]

        result = editor.xml_selecter(headers)

        assert isinstance(result, list)
        assert len(result) == 3

        directory, block, master_list = result

        assert block == "socialscience"
        assert "unitOfAnalysis" in directory
        assert "samplingProcedure" in directory
        assert isinstance(master_list, list)

        print(f"Social Science block - Directory keys: {list(directory.keys())}")
        print(f"Social Science block - Master list: {master_list}")

    def test_primitive_fields_classification(self):
        """Test that primitive fields are correctly classified"""
        headers = ["MARKER 1"]
        result = editor.xml_selecter(headers)

        directory, block, master_list = result
        primitive_fields = master_list[0]

        # These should be classified as primitive
        assert "title" in primitive_fields
        assert "subtitle" in primitive_fields
        assert "alternativeTitle" in primitive_fields

    def test_compound_fields_classification(self):
        """Test that compound fields are correctly classified"""
        headers = ["MARKER 1"]
        result = editor.xml_selecter(headers)

        directory, block, master_list = result
        compound_fields = master_list[1]

        # These should be classified as compound
        assert "author" in compound_fields
        assert "datasetContact" in compound_fields
        assert "dsDescription" in compound_fields


class TestCheckLock:
    """Test the check_lock function"""

    @pytest.mark.integration
    def test_check_lock_with_locked_dataset(self):
        """
        Integration test: Check if a real dataset is locked

        This test requires:
        - Valid API token in the script configuration
        - Valid base URL in the script configuration
        - A dataset ID to test with

        Run with: pytest --integration
        """
        # Set up test configuration - replace with your test values
        test_dataset_id = "your_test_dataset_id"

        # This will take time if dataset is locked (polls every 10 seconds)
        result = editor.check_lock(test_dataset_id)

        assert isinstance(result, bool)

    @pytest.mark.integration
    def test_check_lock_with_invalid_dataset(self):
        """Test check_lock with non-existent dataset"""
        result = editor.check_lock("non_existent_dataset_12345")
        assert result is False or result is True  # Depends on API response


class TestDataParsingIntegration:
    """Integration tests for data parsing workflows"""

    def test_complete_primitive_field_update_workflow(self):
        """
        Test complete workflow for updating a primitive field
        """
        # Simulate a CSV row
        row = {"title:title": "Updated Dataset Title"}
        field = {
            "typeName": "title",
            "multiple": False,
            "typeClass": "primitive",
            "value": "Original Title"
        }

        # Step 1: Format the field
        formatted = editor.primitive_formatter("title:title", row, field.copy())

        # Step 2: Verify the value was updated
        assert formatted["value"] == "Updated Dataset Title"

        print("Primitive field update workflow successful!")
        print(f"Input value: {row['title:title']}")
        print(f"Output field: {json.dumps(formatted, indent=2)}")

    def test_complete_compound_field_update_workflow(self):
        """
        Test complete workflow for updating a compound field
        """
        # Simulate a CSV row with compound data
        row = {"author:authorName;authorAffiliation": "Smith, John;University of Toronto"}

        # Step 1: Format the compound field
        formatted = editor.compound_formatter("author:authorName;authorAffiliation", row)

        # Step 2: Verify structure
        assert isinstance(formatted, list)
        assert len(formatted) == 1
        assert formatted[0]["authorName"]["value"] == "Smith, John"

        print("Compound field update workflow successful!")
        print(f"Input value: {row['author:authorName;authorAffiliation']}")
        print(f"Output field: {json.dumps(formatted, indent=2)}")

    def test_csv_header_parsing_example(self):
        """Demonstrate how CSV headers should be formatted"""
        # Example 1: Primitive field
        primitive_header = "title:title"
        field_name = primitive_header.split(":")[0]
        assert field_name == "title"

        # Example 2: Compound field with multiple primitives
        compound_header = "author:authorName;authorAffiliation"
        parts = compound_header.split(":")
        field_name = parts[0]
        primitives = parts[1].split(";")

        assert field_name == "author"
        assert primitives == ["authorName", "authorAffiliation"]

        print("CSV Header Parsing Examples:")
        print(f"Primitive field format: {primitive_header}")
        print(f"Compound field format: {compound_header}")


@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests that require API access (will be skipped by default)"""

    def test_api_connection(self):
        """Test basic API connectivity"""
        # Replace with your test DOI
        test_doi = "doi:10.5072/FK2/TEST"

        resp = editor.api_origin.get_dataset(test_doi, version="2.0")

        print(f"API Status Code: {resp.status_code}")
        if resp.status_code == 200:
            print("API connection successful!")
        else:
            print(f"API Error: {resp.json()}")


def test_configuration_loaded():
    """Verify that the configuration variables are set"""
    print("\n=== Configuration Check ===")
    print(f"file_directory: {editor.file_directory}")
    print(f"api_token_origin: {'SET' if editor.api_token_origin != 'API KEY HERE' else 'NOT SET - PLEASE CONFIGURE'}")
    print(f"url_base_origin: {'SET' if editor.url_base_origin != 'BASE URL HERE' else 'NOT SET - PLEASE CONFIGURE'}")

    if editor.api_token_origin == "API KEY HERE":
        print("\n⚠️  WARNING: API token not configured!")
        print("Please update the api_token_origin variable in the script.")

    if editor.url_base_origin == "BASE URL HERE":
        print("\n⚠️  WARNING: Base URL not configured!")
        print("Please update the url_base_origin variable in the script.")


if __name__ == "__main__":
    # Run tests directly
    print("Running Universal Field Editor Tests...\n")

    # Run a simple test
    test_configuration_loaded()

    print("\n=== Testing Primitive Formatter ===")
    test = TestPrimitiveFormatter()
    test.test_single_value_non_multiple_field()

    print("\n=== Testing Compound Formatter ===")
    test = TestCompoundFormatter()
    test.test_single_compound_field_with_multiple_primitives()

    print("\n=== All basic tests completed! ===")
    print("\nFor full test suite, run: pytest test_universal_field_editor_V2.py -v")

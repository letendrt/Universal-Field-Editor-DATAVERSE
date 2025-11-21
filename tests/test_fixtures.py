"""
Test fixtures and sample data for universal_field_editor_V2.py

This file contains example CSV files, mock API responses, and test data
to help understand and test the Universal Field Editor.
"""

import json

# ============================================================================
# SAMPLE CSV FILES FOR TESTING
# ============================================================================

# Example 1: Citation Metadata CSV
SAMPLE_CITATION_CSV = """doi,title:title,subtitle:subtitle,alternativeTitle:alternativeTitle,author:authorName;authorAffiliation
https://doi.org/10.5072/FK2/TEST1,Test Dataset 1,Primary Data,Alternative Title 1+Alternative Title 2,"Smith, John;University of Toronto+Doe, Jane;York University"
https://doi.org/10.5072/FK2/TEST2,Test Dataset 2,,,"Johnson, Bob;McGill University"
"""

# Example 2: Social Science Metadata CSV
SAMPLE_SOCIALSCIENCE_CSV = """doi,unitOfAnalysis:unitOfAnalysis,samplingProcedure:samplingProcedure,dataCollector:dataCollector
https://doi.org/10.5072/FK2/TEST1,Individuals+Households,Random sampling,Research Team A
https://doi.org/10.5072/FK2/TEST2,Organizations,Systematic sampling,Research Team B
"""

# Example 3: CSV with empty values (edge cases)
SAMPLE_EDGE_CASES_CSV = """doi,title:title,subtitle:subtitle,author:authorName;authorAffiliation
https://doi.org/10.5072/FK2/TEST1,,,"Smith, John;University of Toronto"
https://doi.org/10.5072/FK2/TEST2,Updated Title,,,
"""


# ============================================================================
# MOCK API RESPONSES
# ============================================================================

MOCK_DATASET_RESPONSE = {
    "status": "OK",
    "data": {
        "id": 12345,
        "persistentId": "doi:10.5072/FK2/TEST1",
        "latestVersion": {
            "metadataBlocks": {
                "citation": {
                    "fields": [
                        {
                            "typeName": "title",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": "Original Title"
                        },
                        {
                            "typeName": "subtitle",
                            "multiple": False,
                            "typeClass": "primitive",
                            "value": ""
                        },
                        {
                            "typeName": "author",
                            "multiple": True,
                            "typeClass": "compound",
                            "value": [
                                {
                                    "authorName": {
                                        "typeName": "authorName",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "Original Author"
                                    },
                                    "authorAffiliation": {
                                        "typeName": "authorAffiliation",
                                        "multiple": False,
                                        "typeClass": "primitive",
                                        "value": "Original University"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        }
    }
}

MOCK_LOCK_RESPONSE_UNLOCKED = {
    "status": "OK",
    "data": []
}

MOCK_LOCK_RESPONSE_LOCKED = {
    "status": "OK",
    "data": [
        {
            "lockType": "finalizePublication"
        }
    ]
}


# ============================================================================
# FIELD DEFINITION EXAMPLES
# ============================================================================

EXAMPLE_PRIMITIVE_FIELD = {
    "typeName": "title",
    "multiple": False,
    "typeClass": "primitive",
    "value": "Original Title"
}

EXAMPLE_MULTIPLE_PRIMITIVE_FIELD = {
    "typeName": "alternativeTitle",
    "multiple": True,
    "typeClass": "primitive",
    "value": ["Original Subtitle"]
}

EXAMPLE_COMPOUND_FIELD = {
    "typeName": "author",
    "multiple": True,
    "typeClass": "compound",
    "value": [
        {
            "authorName": {
                "typeName": "authorName",
                "multiple": False,
                "typeClass": "primitive",
                "value": "Original Author"
            }
        }
    ]
}


# ============================================================================
# TEST DATA ORGANIZED BY SCENARIO
# ============================================================================

SCENARIOS = {
    "update_primitive_single_value": {
        "description": "Update a single primitive field value",
        "csv_row": {"title:title": "New Title"},
        "field_before": EXAMPLE_PRIMITIVE_FIELD.copy(),
        "expected_after": {
            "typeName": "title",
            "multiple": False,
            "typeClass": "primitive",
            "value": "New Title"
        }
    },
    "update_primitive_multiple_values": {
        "description": "Update a primitive field with multiple values (using +)",
        "csv_row": {"alternativeTitle:alternativeTitle": "Subtitle 1+Subtitle 2"},
        "field_before": EXAMPLE_MULTIPLE_PRIMITIVE_FIELD.copy(),
        "expected_after": {
            "typeName": "alternativeTitle",
            "multiple": True,
            "typeClass": "primitive",
            "value": ["Subtitle 1", "Subtitle 2"]
        }
    },
    "add_new_author": {
        "description": "Add a new author to dataset",
        "csv_row": {"author:authorName;authorAffiliation": "Smith, John;University of Toronto+Doe, Jane;York University"},
        "expected_output": [
            {
                "authorName": {
                    "typeName": "authorName",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": "Smith, John"
                },
                "authorAffiliation": {
                    "typeName": "authorAffiliation",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": "University of Toronto"
                }
            },
            {
                "authorName": {
                    "typeName": "authorName",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": "Doe, Jane"
                },
                "authorAffiliation": {
                    "typeName": "authorAffiliation",
                    "multiple": False,
                    "typeClass": "primitive",
                    "value": "York University"
                }
            }
        ]
    },
    "empty_value_no_update": {
        "description": "Empty value should not trigger update",
        "csv_row": {"title:title": ""},
        "field_before": EXAMPLE_PRIMITIVE_FIELD.copy(),
        "expected_after": ""  # Empty string indicates no update
    }
}


# ============================================================================
# HELPER FUNCTIONS FOR TESTS
# ============================================================================

def create_sample_csv(filename, content):
    """Create a sample CSV file for testing"""
    with open(filename, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    print(f"Created sample CSV: {filename}")


def print_scenario(scenario_name):
    """Print a test scenario for demonstration"""
    scenario = SCENARIOS.get(scenario_name)
    if not scenario:
        print(f"Scenario '{scenario_name}' not found")
        return

    print(f"\n{'='*70}")
    print(f"SCENARIO: {scenario['description']}")
    print(f"{'='*70}")
    print(f"CSV Row: {scenario['csv_row']}")
    if 'field_before' in scenario:
        print(f"Field Before: {json.dumps(scenario['field_before'], indent=2)}")
    if 'expected_after' in scenario:
        print(f"Expected After: {json.dumps(scenario['expected_after'], indent=2)}")


def demonstrate_csv_parsing():
    """Demonstrate how CSV files are parsed"""
    print(f"\n{'='*70}")
    print("CSV FILE FORMAT DEMONSTRATION")
    print(f"{'='*70}")

    print("\n1. CITATION METADATA CSV FORMAT:")
    print("- First column: DOI (unique identifier)")
    print("- Other columns: field:subfield format")
    print("- Use '+' to separate multiple values")
    print("- Use ';' to separate subfields in compound fields")
    print("\nExample:")
    print(SAMPLE_CITATION_CSV)

    print("\n2. SOCIAL SCIENCE METADATA CSV FORMAT:")
    print("- Same format but different metadata block")
    print("- May contain different field names")
    print("\nExample:")
    print(SAMPLE_SOCIALSCIENCE_CSV)


if __name__ == "__main__":
    print("="*70)
    print("TEST FIXTURES AND SAMPLE DATA")
    print("="*70)

    demonstrate_csv_parsing()

    print(f"\n{'='*70}")
    print("TEST SCENARIOS")
    print(f"{'='*70}")

    for scenario_name in SCENARIOS:
        print_scenario(scenario_name)

    print(f"\n{'='*70}")
    print("To use these fixtures, import this module in your tests:")
    print("from test_fixtures import SCENARIOS, SAMPLE_CITATION_CSV")
    print("="*70)

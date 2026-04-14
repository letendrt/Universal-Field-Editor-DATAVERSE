# Testing Guide for Universal Field Editor

This guide explains how to test the Universal Field Editor script and understand what works and what doesn't.

## Table of Contents
1. [Setup](#setup)
2. [Running Tests](#running-tests)
3. [Understanding Test Coverage](#understanding-test-coverage)
4. [What Works vs What Doesn't](#what-works-vs-what-doesnt)
5. [Example Usage](#example-usage)
6. [Writing Your Own Tests](#writing-your-own-tests)

---

## Setup

### 1. Install Test Dependencies

```bash
# Install pytest
pip install pytest

# Optional: Install additional testing tools
pip install pytest-cov pytest-mock

# Install main dependencies (if not already installed)
pip install pandas requests pyDataverse
```

### 2. Configure the Script

Before running tests, you **must** update the configuration in `universal_field_editor_V2.py`:

```python
# Update these variables:
file_directory = ['path/to/your/test_file.csv']  # Path to your test CSV
api_token_origin = "YOUR_API_TOKEN_HERE"          # Your Dataverse API token
url_base_origin = 'https://your.dataverse.org'    # Your Dataverse URL
```

### 3. Create Test CSV Files

Use the sample formats provided in `test_fixtures.py`:

**Citation Metadata Example** (`test_citation.csv`):
```csv
doi,title:title,subtitle:subtitle,author:authorName;authorAffiliation
https://doi.org/10.5072/FK2/TEST1,Test Dataset,My Subtitle,"Smith, John;University of Toronto+Doe, Jane;York University"
```

**Social Science Example** (`test_socialscience.csv`):
```csv
doi,unitOfAnalysis:unitOfAnalysis,samplingProcedure:samplingProcedure
https://doi.org/10.5072/FK2/TEST1,Individuals+Households,Random sampling
```

---

## Running Tests

### Run All Tests

```bash
# Basic test run
pytest test_universal_field_editor_V2.py -v

# With coverage report
pytest test_universal_field_editor_V2.py --cov=universal_field_editor_V2 --cov-report=html

# Stop on first failure
pytest test_universal_field_editor_V2.py -x
```

### Run Specific Test Categories

```bash
# Unit tests only (no API calls)
pytest test_universal_field_editor_V2.py -v -k "not integration"

# Integration tests only (requires API)
pytest test_universal_field_editor_V2.py -v -k "integration"

# Specific test class
pytest test_universal_field_editor_V2.py::TestPrimitiveFormatter -v

# Specific test method
pytest test_universal_field_editor_V2.py::TestPrimitiveFormatter::test_multiple_values_split_by_plus -v
```

### Run Tests Directly (Without pytest)

```bash
# Run the test file directly
python test_universal_field_editor_V2.py

# View test fixtures
python test_fixtures.py
```

---

## Understanding Test Coverage

### What's Tested

#### ✓ Core Formatting Functions
- **primitive_formatter**: Handles single and multiple primitive field values
- **compound_formatter**: Handles compound fields with sub-fields
- **record_check**: Validates and assigns new values to fields

#### ✓ Configuration Functions
- **xml_selecter**: Selects correct metadata block (citation, socialscience)

#### ✓ Data Parsing Logic
- CSV header parsing (`field:subfield` format)
- Multiple value handling (`+` separator)
- Sub-field handling (`;` separator)
- Empty value detection

#### ✗ Not Tested (Require Real API)
- **check_lock**: Requires live Dataverse instance
- **API_push**: Makes actual API calls
- **update_metadata**: Full integration with API
- **file_loader**: End-to-end CSV processing
- **publish_dataset**: Publishes datasets

---

## What Works vs What Doesn't

### ✅ Works (Tested & Reliable)

1. **CSV Header Parsing**
   - Parses `field:subfield` format correctly
   - Handles `field:subfield1;subfield2;subfield3` for compound fields

2. **Value Splitting**
   - Splits on `+` for multiple values
   - Splits on `;` for sub-fields
   - Example: `"Value1+Value2;Sub2"` → `["Value1 Value2", "Sub2"]`

3. **Primitive Field Updates**
   - Single values work: `"title:title", "New Title"` ✓
   - Multiple values work: `"alternativeTitle:alternativeTitle", "Title1+Title2"` ✓
   - Empty values skip updates correctly ✓

4. **Compound Field Updates**
   - Single compound entries: `"author:authorName;authorAffiliation", "Smith;UofT"` ✓
   - Multiple entries: `"author:name;affil", "Smith;UofT+Doe;York"` ✓

5. **Field Type Classification**
   - Correctly identifies primitive vs compound fields ✓
   - Selects appropriate metadata block ✓

6. **Value Validation**
   - Detects empty strings and empty lists ✓
   - Prevents updates with no data ✓

### ⚠️ Partially Works (Edge Cases May Fail)

1. **Date Format Handling**
   - Should work with standard ISO dates
   - Untested with various date formats
   - May need format validation

2. **Controlled Vocabulary Fields**
   - Currently treats as primitive (per code comment)
   - May not validate against allowed values

3. **Very Large CSV Files**
   - No explicit tests for performance
   - May hit API rate limits
   - No batching/pausing implemented

4. **Unicode Characters**
   - Should work (UTF-8 BOM handled)
   - Not extensively tested with all character sets

### ❌ Known Limitations

1. **No Error Recovery**
   - If one dataset update fails, script continues
   - No retry logic for transient failures

2. **No Transaction Safety**
   - Updates one field at a time
   - Partial updates possible if script interrupted

3. **API Rate Limiting**
   - No rate limit handling
   - May hit limits with large batches

4. **No Input Validation**
   - CSV format errors cause failures
   - No schema validation

### 🔴 Requires Real Dataverse Instance

The following functions **cannot be tested without a live Dataverse API**:
- `check_lock()` - Checks dataset lock status
- `API_push()` - Pushes metadata updates
- `update_metadata()` - Full update workflow
- `file_loader()` - End-to-end processing
- `publish_dataset()` - Publishes datasets

---

## Example Usage

### Example 1: Update a Title

**CSV:**
```csv
doi,title:title
https://doi.org/10.5072/FK2/TEST1,Updated Title for Dataset
```

**What happens:**
1. Script reads the CSV row
2. Parses `title:title` header → field name = "title"
3. Formats primitive field with value "Updated Title for Dataset"
4. Calls API to update the dataset

**Expected Result:** ✓ Works

### Example 2: Add Multiple Authors

**CSV:**
```csv
doi,author:authorName;authorAffiliation
https://doi.org/10.5072/FK2/TEST1,"Smith, John;University of Toronto+Doe, Jane;York University"
```

**What happens:**
1. Parses compound field header: `author:authorName;authorAffiliation`
2. Splits values by `+`: ["Smith, John;University of Toronto", "Doe, Jane;York University"]
3. Splits each by `;`: First author: ("Smith, John", "University of Toronto")
4. Formats compound field structure with both authors
5. Calls API to update

**Expected Result:** ✓ Works

### Example 3: Update with Empty Value

**CSV:**
```csv
doi,title:title,subtitle:subtitle
https://doi.org/10.5072/FK2/TEST1,Updated Title,
```

**What happens:**
1. `title:title` has value "Updated Title" → update happens ✓
2. `subtitle:subtitle` is empty → update skipped ✓

**Expected Result:** ✓ Works (no errors)

### Example 4: Incorrect Format (Will Fail)

**CSV:**
```csv
doi,title,subtitle
https://doi.org/10.5072/FK2/TEST1,Updated Title,My Subtitle
```

**What happens:**
- Missing `:` in header format
- Script cannot parse field names

**Expected Result:** ❌ Will fail or skip fields

---

## Writing Your Own Tests

### Template for Testing a Function

```python
import pytest
from universal_field_editor_V2 import primitive_formatter

def test_my_custom_scenario():
    # Arrange
    change_area = "title:title"
    row = {"title:title": "New Title"}
    field = {"typeName": "title", "multiple": False, "value": "Old"}

    # Act
    result = primitive_formatter(change_area, row, field)

    # Assert
    assert result["value"] == "New Title"
```

### Testing with Mock API

```python
from unittest.mock import Mock, patch
import universal_field_editor_V2 as editor

def test_with_mock_api():
    # Mock the API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"id": 12345}}

    with patch('requests.get', return_value=mock_response):
        # Your test code here
        result = editor.check_lock("test_id")
        assert result is True
```

### Adding a New Test Scenario

1. Add scenario to `test_fixtures.py`:
```python
SCENARIOS["my_new_test"] = {
    "description": "Describe what you're testing",
    "csv_row": {...},
    "field_before": {...},
    "expected_after": {...}
}
```

2. Write test:
```python
def test_my_new_scenario():
    scenario = SCENARIOS["my_new_test"]
    result = some_function(scenario["csv_row"])
    assert result == scenario["expected_after"]
```

---

## Running Integration Tests

### Setup Integration Testing

1. Create a test dataset in your Dataverse instance
2. Configure test values:
```python
# In test_universal_field_editor_V2.py
TEST_DATASET_ID = "your_test_dataset_id"
TEST_DOI = "doi:10.5072/FK2/TEST"
```

3. Run integration tests:
```bash
pytest --integration
```

### What Integration Tests Check

1. API connectivity
2. Actual metadata updates
3. Dataset locking behavior
4. Real CSV file processing
5. End-to-end workflow

---

## Troubleshooting

### Test Failures

**Problem:** `ImportError: No module named 'pytest'`
**Solution:** Run `pip install pytest`

**Problem:** `ModuleNotFoundError: No module named 'universal_field_editor_V2'`
**Solution:** Run tests from the repository root directory

**Problem:** Integration tests fail with 401 Unauthorized
**Solution:** Update API token in the script

**Problem:** Tests pass but real usage fails
**Solution:** Check CSV format - use UTF-8 BOM encoding

### Common CSV Format Errors

❌ Wrong: `title,subtitle`
✅ Right: `title:title,subtitle:subtitle`

❌ Wrong: `"Value","Value2"` (with extra quotes)
✅ Right: `Value,Value2`

❌ Wrong: `Smith, John;University` (no backslash for comma)
✅ Right: `"Smith, John;University"` (quotes around value with comma)

---

## Test Coverage Report

Generate a test coverage report:

```bash
# Install coverage tool
pip install pytest-cov

# Run with coverage
pytest --cov=universal_field_editor_V2 --cov-report=html

# View report
open htmlcov/index.html
```

Expected coverage:
- `primitive_formatter`: ~95%
- `compound_formatter`: ~90%
- `record_check`: 100%
- `xml_selecter`: ~85%
- `check_lock`: Cannot test without API
- `API_push`: Cannot test without API
- `update_metadata`: Cannot test without API
- `file_loader`: Cannot test without API

---

## Summary

### Quick Test Commands

```bash
# Install dependencies
pip install pytest pandas requests pyDataverse

# Run unit tests only (recommended first step)
pytest test_universal_field_editor_V2.py -v -k "not integration"

# Run specific test
pytest test_universal_field_editor_V2.py::TestPrimitiveFormatter::test_multiple_values_split_by_plus -v

# View fixtures and examples
python test_fixtures.py

# Check configuration
python test_universal_field_editor_V2.py
```

### Next Steps

1. ✓ Run unit tests to verify core logic
2. ✓ Create test CSV files with your data
3. ✓ Test with a single dataset first
4. ✓ Review logs to confirm updates
5. ✓ Run full batch only after testing

---

## Need Help?

- Check `test_fixtures.py` for examples
- Review test output for detailed logging
- Use `-v` flag for verbose test output
- Use `--integration` for API testing (requires real Dataverse)

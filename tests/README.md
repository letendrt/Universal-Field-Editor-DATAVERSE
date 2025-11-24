# Tests for Universal Field Editor

This directory contains the test suite for the Universal Field Editor script.

## Directory Structure

```
tests/
├── __init__.py                    # Package initializer
├── conftest.py                    # Pytest configuration
├── pytest.ini                     # Pytest settings
├── README.md                      # This file
├── test_universal_field_editor_V2.py  # Main test suite
├── test_fixtures.py               # Test data and fixtures
└── sample_data/                   # Sample CSV files
    ├── citation_test.csv
    └── socialscience_test.csv
```

## Running Tests

### From Repository Root

```bash
# Run all tests
pytest -v

# Run unit tests only (no API required)
pytest -v -k "not integration"

# Run integration tests (requires API)
pytest -v -m integration

# Run specific test file
pytest tests/test_universal_field_editor_V2.py -v

# Run with coverage
pytest --cov=.. --cov-report=html
```

### From Tests Directory

```bash
c tests/

# Run all tests
pytest -v

# Run without coverage
pytest -v --no-cov
```

## Test Categories

### Unit Tests (Fast, No API)
- `TestPrimitiveFormatter` - Tests primitive field formatting
- `TestCompoundFormatter` - Tests compound field formatting
- `TestRecordCheck` - Tests value validation
- `TestXmlSelecter` - Tests metadata block selection

### Integration Tests (Requires Live API)
- `TestCheckLock` - Tests dataset lock checking
- `TestAPIIntegration` - Tests actual API calls

## Test Data

### Sample CSV Files

Located in `tests/sample_data/`:

- **citation_test.csv** - Example citation metadata updates
- **socialscience_test.csv** - Example social science metadata updates

### Fixtures

Import test fixtures in your tests:

```python
from test_fixtures import (
    SAMPLE_CITATION_CSV,
    MOCK_DATASET_RESPONSE,
    SCENARIOS
)
```

## Configuration

Tests use the `conftest.py` file to set up the environment:

- Adds parent directory to Python path
- Enables imports of the main module

## Writing New Tests

### Template

```python
def test_your_feature():
    """Test description"""
    # Arrange
    input_data = {...}

    # Act
    result = your_function(input_data)

    # Assert
    assert result == expected_output
```

### Best Practices

1. Use descriptive test names
2. Include docstrings explaining what's tested
3. Test both success and failure cases
4. Use fixtures from `test_fixtures.py`
5. Mark integration tests with `@pytest.mark.integration`

## Troubleshooting

### Import Errors

If you get `ModuleNotFoundError` for `universal_field_editor_V2`:

- Make sure you're running pytest from the repository root or tests directory
- Check that `conftest.py` exists in the tests directory
- Verify the main script is in the parent directory

### Integration Test Failures

Integration tests require:
- Valid API token in the main script
- Valid base URL
- Access to a test dataset

Mark integration tests to skip them:

```bash
pytest -m "not integration"
```

## Continuous Integration

To run tests in CI/CD pipelines:

```bash
# Install dependencies
pip install pytest pandas requests pyDataverse

# Run unit tests only
pytest -v -k "not integration" --tb=short

# Generate coverage report
pytest --cov=.. --cov-report=xml --cov-report=html
```

## License

Same as the main project.

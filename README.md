# Universal Field Editor for Dataverse

Bulk edit dataset metadata in Dataverse installations using CSV files.

## Overview

The Universal Field Editor is a Python script that enables batch updates to dataset metadata in Dataverse repositories (including Borealis). Instead of manually editing metadata fields through the web interface, you can use CSV files to update multiple datasets at once. <br> <br>

### What it does

- Updates dataset metadata fields via the Dataverse API (through pyDataverse)
- Supports ALL metadata blocks
- Handles primitive fields and compound fields (controlled vocabulary functionalities via primitive fields)
- Processes multiple datasets from a single CSV file
- Checks dataset locks and waits for operations to complete before continuing with locked datasets

## Installation

### Requirements

- Python 3.8+
- Dataverse account with API access

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Universal-Field-Editor-DATAVERSE
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install using Poetry:
```bash
poetry install
```

3. Configure your environment:
```bash
cp .env.example .env
```

4. Edit `.env` with your Dataverse credentials and CSV file path.

## Configuration

Create a `.env` file with the following variables:

```env
# Required
DATAVERSE_API_TOKEN=your_api_token_here
DATAVERSE_BASE_URL=https://demo.borealisdata.ca
CSV_FILE_PATHS=/path/to/metadata.csv

# Optional
AUTO_PUBLISH=false
LOG_LEVEL=INFO
TEST_MODE=false
```

### Getting an API Token

1. Log into your Dataverse instance
2. Go to your user profile
3. Click "API Token"
4. Generate or copy your existing token

## Usage

### Basic Usage

1. Create a CSV file with your metadata updates (see README.md in CSV_Excel_Sheets folder above)
2. Update the `CSV_FILE_PATHS` in your `.env` file (the script can also be run from any IDE or virtual environment like Google Collaboratory or Jupyter Notebook)
3. Run the script:

```bash
python universal_field_editor_V2.py
```

### Using the Makefile

Common operations are available through the Makefile:

```bash
# Run the field editor
make run

# Run tests
make test

# Check code style
make lint
```

## Functions

The script includes these core functions:

### `file_loader()`
Loads and validates the CSV file(s) specified in configuration.

### `xml_selecter(header)`
Identifies the metadata block based on the MARKER column and loads the appropriate XML schema.

### `update_metadata(...)`
Core function that:
- Parses CSV rows
- Formats metadata fields (primitive or compound)
- Pushes updates to Dataverse API

### `primitive_formatter(change_area, row, field)`
Formats primitive metadata fields (single-level fields).

### `compound_formatter(header, row)`
Formats compound metadata fields (nested parent-child structures).

### `API_push(field, doi)`
Sends the formatted metadata to the Dataverse API.

### `check_lock(dataset_id)`
Checks if a dataset is locked and waits for the lock to clear.

## Testing

Run the test suite:

```bash
pytest
```

Or using the Makefile:

```bash
make test
```

Tests cover:
- CSV parsing and validation
- Field formatting (primitive and compound)
- API communication (with mocks)
- Error handling

## Environment Variables

### Required
- `DATAVERSE_API_TOKEN` - Your Dataverse API token
- `DATAVERSE_BASE_URL` - Base URL of your Dataverse instance
- `CSV_FILE_PATHS` - Comma-separated paths to CSV files

### Optional
- `AUTO_PUBLISH` - Automatically publish datasets after update (default: false)
- `PUBLISH_TYPE` - Type of publish (major/minor, default: minor)
- `LOCK_CHECK_INTERVAL` - Seconds between lock checks (default: 10)
- `MAX_RETRIES` - Maximum API retry attempts (default: 3)
- `TEST_MODE` - Run without making API calls (default: false)
- `DRY_RUN` - Log updates without applying them (default: false)

## Troubleshooting

### Common Issues

**"API token invalid"**
- Verify your API token in `.env`
- Ensure token has permission to edit datasets

**"Dataset not found"**
- Check that DOIs in CSV are correct
- Verify datasets exist in your Dataverse instance

**"CSV file not found"**
- Check file paths in `CSV_FILE_PATHS`
- Use absolute paths

**"Field validation error"**
- Check that values match field types
- For controlled vocabulary, use allowed terms only
- Verify compound field formatting

**"Dataset locked"**
- The script will wait for locks to clear
- Check Dataverse for ongoing operations
- Increase `LOCK_CHECK_TIMEOUT` if needed

### Log Files

Logs are written to stdout by default. To save to a file:

```bash
python universal_field_editor_V2.py > update_log.txt 2>&1
```

## Best Practices

1. **Test with a single dataset first** - Verify CSV format and API access
2. **Use dry run mode** - Test without making changes: `DRY_RUN=true`
3. **Backup data** - Export current metadata before bulk updates
4. **Small batches** - Process datasets in small groups initially
5. **Check logs** - Review output for errors and warnings
6. **Use Excel template** - Refer to `All_Sheets.xlsx` for column structure

## Limitations

- Only processes CSV files (not XLSX directly)
- Currently supports citation and social sciences metadata blocks
- Updates existing datasets only (does not create new datasets)
- API rate limits apply

## Development

### Project Structure

```
Universal-Field-Editor-DATAVERSE/
├── universal_field_editor_V2.py    # Main script
├── All_Sheets.xlsx                 # Excel template
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Poetry configuration
├── .env.example                    # Environment template
├── tests/                          # Test suite
├── Makefile                        # Common commands
└── README.md                       # This file
```

### Adding New Features

See [TODO.md](./TODO.md) for planned improvements and development roadmap.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Run the test suite: `make test`
5. Submit a pull request

## License

[License information to be added]

## Support

For issues and questions:
- Check the troubleshooting section
- Review example CSV files
- Open an issue on GitHub

## Dataverse API Documentation

- [Dataverse API Guide](https://guides.dataverse.org/en/latest/api/)
- [pyDataverse Documentation](https://pydataverse.readthedocs.io/)
- [Dataset Locks API](https://guides.dataverse.org/en/latest/api/native-api.html#dataset-locks)

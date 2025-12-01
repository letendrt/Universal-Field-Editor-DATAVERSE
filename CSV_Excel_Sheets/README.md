## Google Sheets to Create CSV Files

Creating a private copy of the Google Sheet below (instead of editing raw CSV files) has the distinct advanatage of holding scroll down menus containing the permissible terms for each controlled vocabulary fields (except language and country). Once filled out, the sheets can then be exported in CSV format and used by the python script. This approach also has the advantage of avoiding potential diacritics issues when exporting CSV files. Copies of the Google Sheet are unique to each user (unless they, themselves, are shared). Copies of the original spreadsheets can be created and edited by following this link: https://docs.google.com/spreadsheets/d/1NaGVIVGPJxam1c8Hp5KBd1IT-JyQ4IcUlTiCJ5-BbhE/copy <br><br>

This above link was created to facilitate the CSV sheet creation process, though it is not mandatory to use the present tool. The CSV copies and Excel format can be found in a folder above. <br><br>

### :warning: Many of the scroll down menu options for controlled vocabulary fields in the Excel format are broken and do not work. :warning:


## CSV Format

The CSV file uses specific column formats to identify field types. Each column header follows a pattern that indicates how the data should be processed.

### Column Header Formats

#### Primitive Fields (Single Value)
**Format**: `fieldName`

Simple fields that accept a single value or array of values.

Examples:
- `title` - Dataset title
- `alternativeTitle` - Alternative titles
- `subtitle` - Dataset subtitle

**Multiple values**: Use `+` to separate values in a single cell:
```
alternativeTitle
Title 1 + Title 2 + Title 3
```

#### Compound Fields (Parent-Child Structure)
**Format**: `parent:child1;child2;child3`

Fields that contain nested primitive fields. Use semicolons to separate child fields.

Examples:
- `keyword:keywordValue;keywordVocabulary` - Keywords with vocabulary terms
- `contributor:contributorName;contributorType` - Contributors with type

**Multiple entries**: Use `+` to separate groups:
```
keyword:keywordValue;keywordVocabulary
Economics; controlled + Census; StatCan
```

**Empty child values**: Use `;` with blank space:
```
keyword:keywordValue;keywordVocabulary
Economics; + Census; StatCan
```

#### Controlled Vocabulary Fields
**Format**: `fieldName`

Fields that only accept specific values from a controlled list.

Examples:
- `subject` - Subject terms (must match Dataverse's controlled list)

#### Dataset Identifier
**Format**: `doi`

The first column must be the dataset identifier. Can be in either format:
- DOI format: `doi:10.5072/FK2/12345`
- URL format: `https://doi.org/10.5072/FK2/12345`

### Marker Column

Each CSV file must have a special marker column to identify the metadata block:

- `MARKER 1` = Citation metadata block
- `MARKER 2` = Social Sciences and Humanities metadata block

This column should be placed after all data columns.

### Example CSV Structure

```csv
doi,title,alternativeTitle,keyword:keywordValue;keywordVocabulary,subject,MARKER 1
https://doi.org/10.5072/FK2/ABC123,My Dataset Title,Alt Title 1 + Alt Title 2,Economics;controlled + Census;StatCan,Economics,1
```

### Creating CSV Files in Excel

1. Use the provided `All_Sheets.xlsx` as a template
2. **Important**: Always export to CSV before running the script
3. The Excel template uses color coding for visual organization:
   - **Green**: Primitive fields
   - **Red**: Compound fields
   - **Blue**: Controlled vocabulary
   - **Black**: Marker column (do not remove)

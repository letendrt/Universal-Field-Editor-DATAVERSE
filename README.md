# :tada: Universal-Field-Editor-DATAVERSE :tada:
This repository holds the relevant code for the universal field editor in Dataverse (more specifically Borealis)


# :snake: 1. Universal_Field_Editor python file :snake:
There are 5 major functions in this script - they are listed below in the sequential order of use (primitive_formatter and compound_formatter depend on the type of metadata being processed):


## <b> :file_folder: 1 - file_loader() </b>
File load and selection. This is the first function to run. 
<br>
It takes no argument 
<br>
<br>

## <b> :bookmark_tabs: 2 - xml_selecter(header) </b>
Uses the CSV file MARKER to select the correct XML dictionary - from which it will create a master_list used in a later function (master_list is a list of list. master_list[0] holds the primitive metadata fields, and master_list[1] holds the compound metadata fields). 
<br>
<br>
Takes one argument:
<ul>
    1 - header: list of column headers in the CSV file 
</ul>
<br>

## <b> :newspaper: 3 - update_metadata(latest_version, row, doi, header, directory, master_list, block) </b> 
  This function parses through the metadata blocks and the CSV file row to retrieve to-be updated metadata. It formats the new metadata field value by calling other functions (see below). It then pushes the updated fields to the API (via pyDataverse).
    <br>
    <br>
    Takes six argument:
    <ul>
       1 - latest_version: most recent version of the metadatablock (pulled form borealis); <br>
       2 - row: the row of the CSV file; <br>
       3 - doi: the doi of the dataset being modified; <br>
       4 - header: list of all to-be parsed field column names; <br>
       5 - directory: dictionary of all the main-level citation metadata fields (defined in file_loader()); <br>
       6 - master_list: list of lists defined in xml_selecter()
    </ul>
    <br>
    
## <b> :floppy_disk: 4 - primitive_formatter(change_area, row, field) </b>
This function formats the values of primitive metadata fields if an only if they are not imbedded in a compound field (meaning that it is a first-level field). It is called in update_metadata()
<br>
<br>
Takes three arguments:
<ul>
  1 - change_area: the name of the field whose value is being updated; <br>
  2 - row: CSV row in which the new values are held; <br>
  3 - field: JSON/dictionary format that will be modified and returned.
</ul>
<br>

## <b> :eyes: 5 - record_check(new_unit, field) </b>
This function is used to avoid code redundancy in primitive_formatter(). It checks if the new field value is not an empty string or empty listed string. It is called in primitive_formatter().
<br>
<br>
Takes two arguments:
<ul>
    1 - new_unit: the new value used to modify the existing record; <br>
    2 - field: the existing record in which the value is added.
</ul>
<br>

## <b> :dvd: 6 - compound_formatter(header, row) </b>
This function is used to format metadata fields that are compound in nature (meaning that they hold primitive fields as values). It is called in update_metadata()
<br>
<br>
Takes two arguments:
<ul>
    1 - header: name of the CSV column currently being parsed through by update_metadata(); <br>
    2 - row: the CSV file row for the dataset.
</ul>
<br>

## <b> :satellite: 7 - API_push(field, doi) </b>
This function pushes the updated metadata field to the API.
<br>
<br>
Takes two arguments:
<ul>
    1 - field: the metadata field ready to be updated; <br>
    2 - doi: the dataset doi.
</ul>
<br>

## <b> :lock: 8 - check_lock(dataset_id) </b>
This function checks if a dataset is locked (for one reason or another; it could be due to .tab file ingestion, for instance). More documentation on what this entails available here: https://guides.dataverse.org/en/6.2/api/native-api.html#dataset-locks. It is not currently in use in the the present version of the code, but this will be updated in due time.
<br>
<br>
Takes one argument:
<ul>
    1 - dataset_id: the dataset doi
</ul>




# 2. Citation_Fields CSV/XLSX File
Each column in the file denotes a different citation metadata field from Dataverse. The CSV file has no colour coding. The XLSX file has colour coding. The spreadsheet (as of now) only holds citation metadata block editing functionalities. There are 4 types of columns: Yellow, Green, Red, and Blue. All of which represent a different type of metadata field. There is a Black 'Marker' column on each sheet (see documentation below). 
<br>

### :warning: Note :warning:
The python file can only process the CSV format as of now. That being said, it is easier for users to edit their fields in excel as all sheets are made available there (requires one excel sheet to be open as opposed to several CSV sheets to be opened). Nevertheless, those XLSX sheets will have to be exported to CSV.
<br>
<br>
<br>

## :ledger: YELLOW :ledger:
Exclusively used for the dataset <b>DOI</b>. Can be in link format (https://doi.org/) or in standard "doi:" format. The code will convert link format to standard format during CSV parsing. <br>
<img width="267" height="105" alt="image" src="https://github.com/user-attachments/assets/1d3d6000-084c-40da-8d34-444c70e55fbd" /> <br>
<img width="453" height="142" alt="image" src="https://github.com/user-attachments/assets/662b7389-1727-47c8-8bae-f3dc3f181d3e" />
<br>
<br>
<br>

## :green_book: GREEN :green_book:
Used for metadata fields that are entirely <b>PRIMITIVE</b> (meaning that there is neither parent nor children). E.g., title, subtitle, alternativeTitle, etc. <br>
<img width="807" height="105" alt="Screenshot 2025-11-17 130742" src="https://github.com/user-attachments/assets/7017867a-c1b9-43e4-89e3-74657a28ee41" />
<br>
<br>
In a <b>PRIMITIVE</b> field, there is only one value. Depending on the field, it can either be a <b>STRING</b> or an <b>ARRAY</b> (that itself holds one or more <b>STRING</b>). In the example below, title and subtitle take a <b>STRING</b>, but alternativeTitle takes an <b>ARRAY</b>. <br>
<img width="313" height="378" alt="image" src="https://github.com/user-attachments/assets/648cc146-cb53-4ced-8644-c35bcb8f17f5" /> <br>
If a <b>PRIMITIVE</b> field takes an <b>ARRAY</b>, it can hold more than one value in the CSV field. This can be done by adding a ‘+’ sign between the cell values (more on this in the RED section). 
<br>
<br>
<br>

## :closed_book: RED :closed_book:
Used to denote COMPOUND fields. A COMPOUND field is a field that holds as its value one or more <b>PRIMITIVE</b> fields (simplification) in an ARRAY. Below is an example of a <b>COMPOUND</b> field in the CSV sheet. Here, the <b>COMPOUND</b> field is keyword, and its children/<b>PRIMITIVE</b> fields are keywordValue and keywordVocabulary. Pragmatically speaking, the values we attribute to the <b>COMPOUND</b> fields are actually that of its children/<b>PRIMITIVE</b> fields. As such, the values we input in the column cells must match the layout of the column header. <br>
<img width="471" height="114" alt="image" src="https://github.com/user-attachments/assets/60019e8f-1211-41fb-9d61-e7535c6d511a" /> <br>
<img width="400" height="423" alt="image" src="https://github.com/user-attachments/assets/89d02a4a-ada2-4296-b507-e006ae9d3d84" />


In the above example, we have the <b>COMPOUND</b> field “keyword” - the <b>COMPOUND</b> field name is always separated from its <b>PRIMITIVE</b> fields by a colon [ : ]. This is just so that the python code can differentiate the COMPOUND name from the <b>PRIMITIVE</b> names. The <b>PRIMITIVE</b> names of each column header are split by a semi-colon [ ; ]. This is done so that the code can do a second pass and differentiate <b>PRIMITIVE</b> fields. 
<br>
<br>
In the example “Hello; StatCan”, we can see that it follows a similar pattern to the <b>PRIMITIVE</b> fields in the column header - that is, they are also split by a semi-colon [ ; ]. In this case, “Hello” is the keywordValue, and “StatCan” is the keywordVocabulary. As it may have been noticed by the reader of this document, “Hello; StatCan” is followed by a “+” sign, and then the entry “World; Federal Agency”. Here, the “+” sign is used to denote that there are more than one entry to the field. The code is set up to be recursive and to loop through the metadata updater for as long as there are “+” signs in the cell. 
<br>
<br>
Log example from the code (formatted to facilitate legibility - appears on one line in practice): <br>
<img width="996" height="673" alt="image" src="https://github.com/user-attachments/assets/8b6e1df2-1020-473c-a346-f42a109ed977" />
<br>
<br>
In the event that we have a keywordValue, but no keywordVocabulary (at which time we would technically have a discrepancy between the column header and its cells), we would simply put a semi-colon followed by a blank space. The code was set up in such a way that allows for some keywords to have a keywordVocabulary even if others do not. Empty strings at the start and end of words are cleaned up with .strip(). An Example is provided below. This approach is used for all <b>COMPOUND</b> fields, not just keywords. Note that this applies to all <b>COMPOUND</b> fields, and not just the keyword field

Example: “Hello; + World; Federal Agency” 
<br>
<br>
<br>

## :blue_book: BLUE :blue_book:
Used to denote control vocabulary, it is neither PRIMITIVE nor COMPOUND, it is controlledVocabulary. Although it is its own typeClass, it works similarly to the input of values in PRIMITIVE fields. The main difference is that only allowed terms (usually a scroll down menu on the borealis user interface) are allowed - elsewise it will return an error 403 (or other) when pushing through the API.<br>
<img width="423" height="102" alt="image" src="https://github.com/user-attachments/assets/f2fd4c0a-d60e-4eeb-901e-e4013edd3acd" /> <br>
<img width="493" height="186" alt="image" src="https://github.com/user-attachments/assets/0d7a5a20-365f-46f2-95c5-f2022457549b" />
<br>
<br>
<br>

## :notebook: BLACK MARKER :notebook:
### :warning::warning: MUST BE KEPT IN THE SHEET. DO NOT REMOVE. 
Used for the code to recognise which sheet is currently being processed (citation metadata or social sciences metadata). <br>
MARKER 1 indicates to the code that it is processing citation metadata <br>
MARKER 2 indicates to the code that it is processing social sciences metadata <br>

<img width="200" height="105" alt="Screenshot 2025-11-21 113154" src="https://github.com/user-attachments/assets/1b116c43-dba6-4806-b05e-759aaba47e39" />
<img width="200" height="105" alt="Screenshot 2025-11-21 113531" src="https://github.com/user-attachments/assets/2405d004-6556-4aa7-8bd4-216e4766fa12" />
<br>
<br>
<br>







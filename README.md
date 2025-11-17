# :tada: Universal-Field-Editor-DATAVERSE :tada:
This repository holds the relevant code for the universal field editor in Dataverse (more specifically Borealis)

# What this repository holds:
## 1) Universal_Field_Editing python file



## 2) Citation_Fields CSV/XLSX File
Each column in the file denotes a different citation metadata field from Dataverse. The CSV file has no colour coding. The XLSX file has colour coding. The spreadsheet (as of now) only holds citation metadata block editing functionalities. There are 4 types of columns: Yellow, Green, Red, and Blue. All of which represent a different type of metadata field.
<br>

### :warning: Note :warning:
The python file can only process the CSV format as of now. As such, users who compile their mass changes in Excel should export the file as a csv when running the script. 
<br>
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
<br>

## :blue_book: BLUE :blue_book:
Used to denote control vocabulary, it is neither PRIMITIVE nor COMPOUND, it is controlledVocabulary. Although it is its own typeClass, it works similarly to the input of values in PRIMITIVE fields. The main difference is that only allowed terms (usually a scroll down menu on the borealis user interface) are allowed - elsewise it will return an error 403 (or other) when pushing through the API.<br>
<img width="423" height="102" alt="image" src="https://github.com/user-attachments/assets/f2fd4c0a-d60e-4eeb-901e-e4013edd3acd" /> <br>
<img width="493" height="186" alt="image" src="https://github.com/user-attachments/assets/0d7a5a20-365f-46f2-95c5-f2022457549b" />
<br>
<br>
<br>
<br>












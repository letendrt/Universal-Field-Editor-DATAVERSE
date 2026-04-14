# Universal Field Editor for Dataverse :milky_way::snake:
The Universal Field Editor is a Python script that enables batch updates to dataset metadata in Dataverse repositories (including Borealis). Instead of manually editing metadata fields through the web interface, you can use CSV files to update multiple datasets at once.

## Code Purpose 🤔❓
1) Streamline the metadata updating process for researchers and data curators that may have minimal python knowledge;
2) Assist seasoned professionals in curating their entire collections in a time efficient manner;
3) Updates dataset metadata fields via the Dataverse API (through [pyDataverse](https://pydataverse.readthedocs.io/en/latest/index.html));
4) Supports ALL metadata blocks and ALL metadata fields (last update - April 2026).

## Minimum Python Requirements 🐍🔧
1) Local IDE (Jupyter, Wing, PyCharm, etc.)
2) Minimum python version: 3.6+

⚠️Note that Borealis does not support web-based IDEs⚠️

## File Requirements 📂🔧
1) Create a copy of the [Universal Field Editor Google Sheet](https://docs.google.com/spreadsheets/d/1NaGVIVGPJxam1c8Hp5KBd1IT-JyQ4IcUlTiCJ5-BbhE/copy).<br><br>
⚠️⚠️ Note that while it is possible to simply download the individual CSV sheets to do use the Universal Field Editor script, the Google Sheet is equipped to handle fields that are restricted to controlled vocabulary terms via predefined drop down menus. As such, creating a personal copy of the CSV sheet will provide a better overall user experience. Once filled out, the sheets can then be exported in CSV format and used by the python script. This approach also has the advantage of avoiding potential character diacritics issues when exporting CSV files. Copies of the Google Sheet are unique to each user (unless they, themselves, are shared).<br>

2) Download the [universal_field_editor.py](https://github.com/letendrt/Universal-Field-Editor-DATAVERSE/blob/main/universal_field_editor_v6.1.py) file.

## Understanding the Google Sheet Format
1) Once a copy is created, users will be greeted by the "Citation" tab of the document. Note, howevevr, that there are 9 sheets - one for each Borealis metadata block:
<kbd><img width="1435" height="78" alt="image" src="https://github.com/user-attachments/assets/378fe4bf-8e14-4309-a30b-6a2914b686d6" /></kbd>

<ul>
  <li>Citation</li>
  <li>Terms of Use</li>
  <li>Social Science and Humanities</li>
  <li>Geospatial</li>
  <li>Astronomy and Astrophysics</li>
  <li>Life Sciences</li>
  <li>Journal</li>
  <li>Computational Workflow</li>
  <li>3D Objects</li>
</ul>

This was done to prevent clutter in a singular, massive sheet. You only need to edit the sheets for the metadata blocks you want to edit. In otherwords, if you are not bringing any modifications to the 'Journal' block, you can just ignore it!

### DO NOT CHANGE THE NAMES OF THE COLUMNS AND DO NOT CHANGE THE NAMES OF THE SHEETS⚠️🚧

2) Next, bring your attention to the column headers. You'll quickly notice that they are colour coded. There are 5 possible types of headers on the sheets. Each colour denotes a different role or information architecture in Dataverse. It is of paramount importance that users understand what each header type indicates. We will then discuss how to fill out fields of each type.
<ul>
  <li><b>Yellow</b>: Always indicates the dataset DOI</li>
  <kbd><img width="226" height="40" alt="image" src="https://github.com/user-attachments/assets/66ad2469-ff7a-462e-b652-5379b937dc51" /></kbd>
  <li><b>Green</b>: Indicates PRIMITIVE metadata fields (no children fields)</li>
  <kbd><img width="407" height="39" alt="image" src="https://github.com/user-attachments/assets/300eac4d-8d02-4420-871a-277485f8b408" /></kbd>
  <li><b>Red</b>: Indicates COMPOUND metadata fields (fields that have children fields)</li>
  <kbd><img width="470" height="38" alt="image" src="https://github.com/user-attachments/assets/5bc30a0c-2c78-44ec-9b01-4aff4a6c1975" /></kbd>
  <li><b>Blue</b>: Indicates CONTROLLED VOCABULARY metadata fields (fields that can only be filled with exact pre-vetted values)</li>
  <kbd><img width="321" height="32" alt="image" src="https://github.com/user-attachments/assets/320ce39e-85a6-4329-b738-4c5dac9fb8ab" /></kbd>
  <li><b>Black</b>: Indicates the kind of sheet being processed by the python script - do not remove this column from your CSV sheet</li>
  <kbd><img width="227" height="40" alt="image" src="https://github.com/user-attachments/assets/814f1a7c-1e2a-4361-8646-8c0ca7971e9c" /></kbd>
</ul>

⚠️The script processes inputs differently depending on whether a primitive or compound field is being added, edited, or removed. <br>
⚠️It is important that you pay attention to the following instructions on how to fill in each kind of field type.

### DO NOT CHANGE THE NAMES OF THE COLUMNS AND DO NOT CHANGE THE NAMES OF THE SHEETS⚠️🚧


### 🟡Yellow Fields: Direct Object Identifier (doi)🟡
This field simply requires that users copy and paste the dataset doi in the column cell. Note that each row in the Google Sheet represents a different dataset. In this case, the DOI can be inserted in "https" format (e.g., https://doi.org/10.80240/FK2/LDRCTM) or in "doi:" format (e.g., doi:10.80240/FK2/LDRCTM). The script will automatically convert the doi format to make the API calls possible. 

Example:<br>
<kbd><img width="313" height="179" alt="image" src="https://github.com/user-attachments/assets/f48389f3-a9d4-41bd-b760-c9a1dc8e7ab8" /></kbd>
<br><br>

### 🟢Green Fields: Primitive Fields🟢
These fields require that users enter the the value they wish to integrate in their dataset metadata record. It's that simple. Note that some entries require integers instead of text strings (mostly in geospatial data) - You'll have to familiarise yourself with your own datasets before bringing forth substantial modifications. You can leave a field empty if you do not wish to add or edit a field. 

Some fields can be repeated (for instance, you can have more than one alternative title, but you cannot have more than one dataset title). If you want the script to create more than one metadata field in Borealis, use a '+' sign between your entries! This will instruct the script to input both entries in two different metadata fields of the same type (see second screenshot below).

Examples:<br>
<kbd><img width="658" height="153" alt="image" src="https://github.com/user-attachments/assets/0283fd40-3315-4fba-bb53-4eb4ee1710f9" /></kbd><br>
<kbd><img width="332" height="142" alt="image" src="https://github.com/user-attachments/assets/b5621ad6-01d0-4b14-83bc-22fab950bc76" /></kbd><br>
<br>

### 🔴Red Fields: Compound Fields🔴
These fields are the most challenging to grasp (but it's all very relative, since they're not too difficult at all). Here, the column names are of great importance. There are 3 important parts to the column name: the column marker, the parent field, and the children field. 

















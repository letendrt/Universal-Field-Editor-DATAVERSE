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

## Understanding the Google Sheet Format 💡🌵🦖
1) Once a copy is created, users will be greeted by the "Citation" tab of the document. Note, howevevr, that there are 9 sheets - one for each Borealis metadata block:
<kbd><img width="1435" height="78" alt="image" src="https://github.com/user-attachments/assets/378fe4bf-8e14-4309-a30b-6a2914b686d6" /></kbd>

<ul>
  <li>Citation</li>
  <li>Terms of Use (only for custom terms)</li>
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
These fields are the most challenging to grasp (but it's all very relative, since they're not too difficult at all). Here, the column names are of great importance. There are 2 important parts to the column names: the parent field (before the colon), and the children fields (after the colon). In the example below, 'Keyword' is the parent field, 'keywordValue' is the first child field, and 'keywordVocabulary' is the second child field.

<kbd><img width="521" height="86" alt="image" src="https://github.com/user-attachments/assets/1ec3fe00-4119-4e43-ae52-2439e9627d95" /></kbd>

The structure of your row entry must match the column name pattern after the colon. In the below example, for instance, we are adding a singular keyword and its thesaurus of origin. The keyword in this case is 'Corn' (same position as child field 'keywordValue'), and its thesaurus is 'Crop Thesaurus' (same position as child field 'keywordVocabulary'). 

<kbd><img width="440" height="88" alt="image" src="https://github.com/user-attachments/assets/f3f5053f-0a2e-4a4b-b0b3-0c647371c9bf" /></kbd>

The example below is how you would input more than one keyword, both of which have their own thesaurus of origin (simply add a '+' sign, and continue the process - you can repeat this as many times as desired for eligible fields):

<kbd><img width="442" height="90" alt="image" src="https://github.com/user-attachments/assets/8ed61df4-c800-441f-b771-f33a28cb6e33" /></kbd>

But what if your keyword does not have a thesuaurs of reference or isn't extracted from a controlled vocabulary? In this case, you would simply enter your keyword value, a semi-colon, and then continue on to your next keyword. You MUST do so for each child node that is not filled. The first screenshot below is how this is done when there is only two children. The second screenshot is for when there is four children. The third is when there are four children, but only the first and third fields are populated (note that we still need to include the unused fields by inserting their semi-colon):

<kbd><img width="439" height="99" alt="image" src="https://github.com/user-attachments/assets/2d31c77b-3b66-4459-b13e-b28480da36f9" /></kbd><br>
<kbd><img width="670" height="114" alt="image" src="https://github.com/user-attachments/assets/984837bb-7f83-4c8b-910a-bfe930514d02" /></kbd><br>
<kbd><img width="672" height="91" alt="image" src="https://github.com/user-attachments/assets/c2b8e083-6748-4db7-88a0-b2b0bf8f42c0" /></kbd>

You now know how to populate the cells of compound columns! Here are some important details and cases to keep in mind:

<li>Some Compound fields only have one child - these do not require the use of semi-colons. They behave like primitive fields (see example below) </li>
<kbd><img width="406" height="94" alt="image" src="https://github.com/user-attachments/assets/71eb82bb-da5f-475d-9e22-9a269f7599bd" /></kbd><br><br>

### 🔵Blue Fields: Controlled Vocabulary🔵
Controlled vocabulary fields are the easiest to handle since most controlled vocabulary fields in the Google Sheet already include vetted entries in column drop down menus. For the exception of a few fields (notably the 'language' field on the citation sheet), users can simply select the pre-vetted option of their choice. Not using the included fields will likely result in errors once submitted to Borealis/Dataverse through the python script.

Example:<br>
<kbd><img width="901" height="783" alt="image" src="https://github.com/user-attachments/assets/234700de-4bf0-4d61-9b80-678aeee0159c" /></kbd>

## Removing (without replacing) values from the existing dataset records ↪️🗑️💯
It is possible the you are using the script to remove existing fields from your datasets. Perhaps there was an error on 200 datasets that you want removed without iterating through every single one of them. The present tool is well-suited to do exactly that. For fields you want removed form your existing datasets, simply enter REMOVE (all caps) in the respective cell on the Google Sheet. The term REMOVE only needs to be entered once per cell, regardless of wether it is a primitive or compound field (see first screenshot below). Note however that controlled vocabulary fields won't accept the REMOVE term. For those, you'll simply have to leave field empty on your Google sheet (see second screenshot below).

Example 1:<br>
<kbd><img width="653" height="131" alt="image" src="https://github.com/user-attachments/assets/586deead-a3f2-4d98-abd7-83d1e3dcd6ac" /></kbd><br>

Example 2 (if a controlled vocabulary field already exists, set the cell to its default blank option to remove it from your dataset):<br>
<kbd><img width="974" height="128" alt="image" src="https://github.com/user-attachments/assets/6e4115d3-c5c6-4733-9d31-bbb06f68f0c6" /></kbd>



## Organising files 💫📂 (optional step)
1) Once you have finished formatting your Google Sheets, download each one in CSV format and place them in a dedicated folder on your device. The naming convention of the files does not matter - though they will become important in the next section (Running the python script 🐍📜).
2) Download the most recent version of the python script (universal_field_editor_v6.2.py - version number is privy to changes), and place it in the same folder as the CSV sheets above.

 ⚠️File location does not actually matter - file paths will be used to retrieve the CSV files⚠️

## Running the python script 🐍📜
Before running the script, you'll have to edit a few parameters in the python file. This is easy and doesn't require any know-how. Just know that you need to have a local python IDE. You may also need to install python libraries (if you don't know how to do so, follow this useful [python module installation](https://www.geeksforgeeks.org/installation-guide/how-to-install-a-python-module/) guide by Geeks for Geeks).<br><br>

1) Open the python file in your IDE and navigate to the 'CONFIGURATION SETTINGS' section.

    <kbd><img width="770" height="103" alt="image" src="https://github.com/user-attachments/assets/8563d358-51a6-4948-ba9d-c2362e358e39" /></kbd>

2) Fetch your copy the path of your CSV files in the placeholder pythong list (python lists are denoted by square brackets). The path directory should be between quotes. If you're loading more than one sheet, add a comma after the entry (after the quote), and then paste the directory of the second CSV sheet. See the example below.

   <kbd><img width="952" height="379" alt="image" src="https://github.com/user-attachments/assets/a0e19765-8a84-472a-8c4e-7bda2b18e806" /></kbd>

 3) Fetch your Borealis/Dataverse API key and paste it in the script placeholder. 

    <kbd><img width="975" height="106" alt="image" src="https://github.com/user-attachments/assets/10c9a703-7470-4d04-99a6-961ab628b65b" /></kbd>

4) Run the script, and ensure that everything went well! 🎊🥳










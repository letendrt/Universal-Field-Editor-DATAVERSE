# Universal Field Editor for Dataverse :milky_way::snake:
The Universal Field Editor is a Python script that enables batch updates to dataset metadata in Dataverse repositories (including Borealis). Instead of manually editing metadata fields through the web interface, you can use CSV files to update multiple datasets at once.

## Code Purpose 🤔❓
1) Streamline the metadata updating process for researchers and data curators that may have minimal python knowledge;
2) Updates dataset metadata fields via the Dataverse API (through [pyDataverse](https://pydataverse.readthedocs.io/en/latest/index.html));
3) Supports ALL metadata blocks and ALL metadata fields (last update - April 2026).

## Minimum Python Requirements 🐍🔧
1) Local IDE (Jupyter, Wing, PyCharm, etc.)
2) Minimum python version: 3.6+

## File Requirements 📂🔧
1) Create a copy of the [Universal Field Editor Google Sheet](https://docs.google.com/spreadsheets/d/1NaGVIVGPJxam1c8Hp5KBd1IT-JyQ4IcUlTiCJ5-BbhE/copy).<br><br>
⚠️⚠️ Note that while it is possible to simply download the individual CSV sheets to do use the Universal Field Editor script, the Google Sheet is equipped to handle fields that are restricted to controlled vocabulary terms via predefined drop down menus. As such, creating a personal copy of the CSV sheet will provide a better overall user experience. Once filled out, the sheets can then be exported in CSV format and used by the python script. This approach also has the advantage of avoiding potential character diacritics issues when exporting CSV files. Copies of the Google Sheet are unique to each user (unless they, themselves, are shared).

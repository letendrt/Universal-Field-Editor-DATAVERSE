# Universal Field Editor for Dataverse :milky_way::snake:

The Universal Field Editor is a Python script that enables batch updates to dataset metadata in Dataverse repositories (including Borealis). Instead of manually editing metadata fields through the web interface, you can use CSV files to update multiple datasets at once.

## Code Purpose 🤔❓
1) Updates dataset metadata fields via the Dataverse API (through pyDataverse)
2) Supports ALL metadata blocks
3) Handles primitive fields and compound fields (controlled vocabulary functionalities via primitive fields)
4) Processes multiple datasets from a single CSV file
5) Checks dataset locks and waits for operations to complete before continuing with locked datasets

## Minimum Python Requirements 🐍🔧
1) Local IDE (Jupyter, Wing, PyCharm, etc.)
2) Minimum python version: 3.6+

## File Requirements 📂🔧

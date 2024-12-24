Heart Failure Analysis with Python
Overview
This project analyzes a dataset of heart failure clinical records, applying data preprocessing and feature engineering techniques. A simple GUI is built using tkinter to provide user interaction with the processed data.

Features
Preprocesses the dataset by:
Applying thresholds to numerical columns (e.g., creatinine_phosphokinase, ejection_fraction, platelets, etc.).
Converting numerical data into binary categories.
Provides a user-friendly graphical interface using tkinter.
Reads and processes data from a CSV file.
Prerequisites
Python 3.x
Required Python libraries:
pandas
itertools
tkinter
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/USERNAME/REPOSITORY_NAME.git
cd REPOSITORY_NAME
Install required libraries:

bash
Copy code
pip install pandas
Place the dataset (heart_failure_clinical_records_dataset.csv) in the project directory.

Usage
Run the script:
bash
Copy code
python code.py
Interact with the GUI to view processed data.
File Details
code.py: Main Python script for data processing and GUI.
heart_failure_clinical_records_dataset.csv: Input dataset (not included, ensure to place your own)
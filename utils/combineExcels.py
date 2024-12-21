#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 17:22:28 2024

@author: gamzeadibelli
"""

import os
import pandas as pd

# Specify the directory containing the Excel files
directory = "/Users/gamzeadibelli/OZU DS/CS552/Project/data"

# Create an empty list to store DataFrames
dataframes = []

# Loop through files in the directory
for file in os.listdir(directory):
    if "kadro" in file.lower() and file.endswith(".xlsx"):  # Check if 'kadro' is in the filename and it is an Excel file
        filepath = os.path.join(directory, file)
        # Read the Excel file into a DataFrame
        df = pd.read_excel(filepath)
        dataframes.append(df)

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a new Excel file
output_file = os.path.join(directory, "combined.xlsx")
combined_df.to_excel(output_file, index=False)

print(f"Combined file saved as {output_file}")

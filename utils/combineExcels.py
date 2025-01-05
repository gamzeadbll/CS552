import os
import pandas as pd

directory = "/Users/gamzeadibelli/OZU DS/CS552/CS552/google_data"
university_data = "/Users/gamzeadibelli/OZU DS/CS552/CS552/data/universities.xlsx"

universities_data = pd.read_excel(university_data)
dataframes = []

for file in os.listdir(directory):
    if  file.endswith(".xlsx"):
        filepath = os.path.join(directory, file)
        
        df = pd.read_excel(filepath)
        university_name = file.replace('_authors.xlsx', '')
        df['University'] = university_name
        dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)
final_df = combined_df.merge(universities_data, on='University', how='left')

output_file = "/Users/gamzeadibelli/OZU DS/CS552/CS552/All_Data.xlsx"
final_df.to_excel(output_file, index=False)

print(f"Combined file saved as {output_file}")

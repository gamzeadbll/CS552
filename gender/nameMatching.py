import os
import pandas as pd
import unicodedata


def normalize_name(name):
    if pd.isnull(name) or not name.strip():
        return None
    name = name.split('.')[-1].strip()
    name_parts = name.split()
    if not name_parts:
        return None
    name = name_parts[0].strip().lower()
    translation_table = str.maketrans({
        "ç": "c", "Ç": "c",
        "ğ": "g", "Ğ": "g",
        "ı": "i", "İ": "i",
        "I": "i",
        "ö": "o", "Ö": "o",
        "ş": "s", "Ş": "s",
        "ü": "u", "Ü": "u",

    })
    normalized = name.translate(translation_table)
    return ''.join(
        char for char in unicodedata.normalize('NFD', normalized)
        if unicodedata.category(char) != 'Mn'
    )


def infer_gender(name):
    if name.endswith(("han", "alp", "kan", "met", "et", "ar","ali")):
        return "Male"
    if name.endswith(("ye", "nur", "gul", "su", "can", "ra", "sa", "an")):
        return "Female"


def check_second_name(row, gender_data):
    if pd.notna(row['Gender']) and row['Gender'] not in ["Unknown", "Unisex"]:
        return row['Gender']

    name = row['Name']
    name = name.split('.')[-1].strip()
    name_parts = name.split()

    if len(name_parts) >= 3:
        second_name = normalize_name(name_parts[1])
        matched_gender = gender_data.loc[gender_data['Normalized Name'] == second_name, 'Gender']
        if not matched_gender.empty:
            return matched_gender.iloc[0]
        return "Female"
    return row['Gender']


def merge_with_gender(file_path, gender_file_path, output_file):
    if not os.path.exists(file_path):
        return

    if not os.path.exists(gender_file_path):
        return

    all_data = pd.read_excel(file_path)
    gender_data = pd.read_excel(gender_file_path)

    all_data['Normalized Name'] = all_data['Name'].apply(normalize_name)
    gender_data['Normalized Name'] = gender_data['Name'].apply(normalize_name)
    gender_data = gender_data.drop_duplicates(subset=['Normalized Name'])

    merged_data = all_data.merge(gender_data[['Normalized Name', 'Gender']], on='Normalized Name', how='left')
    matched = merged_data['Gender'].notna().sum()
    unmatched = merged_data['Gender'].isna().sum()
    print(f"Matched rows before inference: {matched}")
    print(f"Unmatched rows before inference: {unmatched}")

    merged_data['Gender'] = merged_data.apply(
        lambda row: infer_gender(row['Normalized Name']) if pd.isna(row['Gender']) and row['Normalized Name'] else row[
            'Gender'],
        axis=1
    )

    unmatched_before_second_name_check = merged_data[merged_data['Gender'].isna() | (merged_data['Gender'] == "Unisex")]
    unmatched_before_second_name_check[['Name']].to_excel('Unmatched_Before_Second_Name_Check.xlsx', index=False)

    merged_data['Gender'] = merged_data.apply(
        lambda row: check_second_name(row, gender_data) if pd.isna(row['Gender']) or row['Gender'] == "Unisex" else row[
            'Gender'],
        axis=1
    )

    unmatched_after_second_name_check = merged_data[merged_data['Gender'].isna() | (merged_data['Gender'] == "Unknown")]
    unmatched_after_second_name_check[['Name']].to_excel('Unmatched_After_Second_Name_Check.xlsx', index=False)

    unmatched_final = unmatched_after_second_name_check.shape[0]
    print(f"Unmatched rows after second name check: {unmatched_final}")

    merged_data = merged_data.drop(columns=['Normalized Name'])
    merged_data.to_excel(output_file, index=False)
    print(f"Merged data saved as {output_file}")


def main():
    project_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_folder, "../All_Data.xlsx")
    gender_file_path = os.path.join(project_folder, "merged-names.xlsx")
    output_file = os.path.join(project_folder, "../All_Data_With_Gender.xlsx")

    merge_with_gender(file_path, gender_file_path, output_file)


if __name__ == "__main__":
    main()
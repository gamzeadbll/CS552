import pandas as pd

def load_excel_to_dataframe(file_path):
    return pd.read_excel(file_path)

def merge_and_deduplicate_with_precedence(file1, file2, output_file):
    df1 = load_excel_to_dataframe(file1)
    df2 = load_excel_to_dataframe(file2)

    combined_df = pd.concat([df1, df2], ignore_index=True)

    combined_df = combined_df.drop_duplicates(subset=["Name"], keep="last")

    combined_df.to_excel(output_file, index=False)
    print(f"Merged file saved to {output_file}")

if __name__ == "__main__":
    file1 = "turkish_names.xlsx"
    file2 = "turkish_names_with_gender.xlsx"
    output_file = "merged_names.xlsx"

    merge_and_deduplicate_with_precedence(file1, file2, output_file)
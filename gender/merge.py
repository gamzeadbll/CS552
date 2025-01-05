import pandas as pd
import chardet


def detect_encoding(file_path):
    """Detect file encoding."""
    with open(file_path, "rb") as file:
        result = chardet.detect(file.read())
        return result['encoding']


def load_excel_to_dataframe(file_path):
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"Error: Excel file not found at {file_path}")
        exit()


def load_txt_to_dataframe(file_path):
    try:
        # Detect encoding
        encoding = detect_encoding(file_path)
        print(f"Detected encoding for {file_path}: {encoding}")

        data = []
        with open(file_path, "r", encoding=encoding) as file:
            for line in file:
                if line.strip():
                    try:
                        name, gender = line.strip().split(",")
                        # Map gender values
                        gender = gender.strip().upper()
                        if gender == "E":
                            gender = "Male"
                        elif gender == "K":
                            gender = "Female"
                        else:
                            gender = "Unisex"
                        data.append({"Name": name.strip(), "Gender": gender})
                    except ValueError:
                        print(f"Skipping invalid line: {line.strip()}")
        return pd.DataFrame(data)
    except FileNotFoundError:
        print(f"Error: TXT file not found at {file_path}")
        exit()


def merge_and_deduplicate(file_txt, file_excel, output_file):
    df_txt = load_txt_to_dataframe(file_txt)
    df_excel = load_excel_to_dataframe(file_excel)
    combined_df = pd.concat([df_txt, df_excel], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=["Name"], keep="last")
    combined_df.to_excel(output_file, index=False)
    print(f"Merged file saved to {output_file}")


if __name__ == "__main__":
    file_txt = "Turkce_isimler_listesi.txt"
    file_excel = "names-scraped-from-sites.xlsx"

    output_file = "merged-names.xlsx"
    merge_and_deduplicate(file_txt, file_excel, output_file)
from openpyxl import Workbook
import os

def save_instructors_to_excel(university_name, instructors):
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    file_name = f"data/{university_name}-kadro.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Kadro"
    ws.append(["University Name", "Instructor Name", "Title", "Faculty", "Department"])

    for instructor in instructors:
        ws.append([
            university_name,
            instructor["full_name"],
            instructor["title"],
            instructor["faculty"],
            instructor["department"]
        ])

    wb.save(file_name)
    print(f"Saved instructor data to {file_name}.")
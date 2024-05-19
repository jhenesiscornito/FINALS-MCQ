
from openpyxl import load_workbook

class FileHandler:
    def read_excel(self, file_path):
        try:
            workbook = load_workbook(filename=file_path)
            sheet = workbook.active
            return sheet
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None

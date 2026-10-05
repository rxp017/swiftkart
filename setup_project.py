"""Point the editable PBIP at this checkout's five local CSV files."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
TABLES = ROOT / "swiftkart_report.SemanticModel" / "definition" / "tables"
NAMES = ("FactSales", "DimCustomer", "DimProduct", "DimStore", "DimDate")

for name in NAMES:
    csv_file = ROOT / "data" / f"{name}.csv"
    table_file = TABLES / f"{name}.tmdl"
    if not csv_file.is_file():
        raise FileNotFoundError(csv_file)
    text = table_file.read_text(encoding="utf-8-sig")
    path = csv_file.as_posix().replace('"', '""')
    updated, count = re.subn(r'File\.Contents\("[^"\r\n]+"\)',
                             lambda _: f'File.Contents("{path}")', text)
    if count != 1:
        raise ValueError(f"Expected one CSV source in {name}, found {count}.")
    table_file.write_text(updated, encoding="utf-8")
    print(f"Configured {name}: {csv_file}")

print("Open swiftkart_report.pbip in Power BI Desktop and refresh. No account required.")
print("This script does not modify swiftkart_report.pbix; it already contains saved data.")

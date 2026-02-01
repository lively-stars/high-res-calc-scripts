# usage python check_negative_pressure.py /path/to/fort.11
# this routine runs through all points in MPS-ATLAS format atmosphere file fort.11 and checks if there are any negative pressure values
# if negative pressures occurs, it prints T and P values 
import sys
from pathlib import Path

def check_file(file_path):
    neg_found = False
    file_path = Path(file_path)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return

    with file_path.open("r") as f:
        # Skip first two header lines
        next(f, None)
        next(f, None)

        for lineno, line in enumerate(f, start=3):
            if not line.strip():
                continue

            cols = line.split()
            if len(cols) < 3:
                continue

            col2 = float(cols[1])
            col3 = float(cols[2])

            if col2 < 0 or col3 < 0:
                print(f"{file_path} -> Negative value at line {lineno}: {col2}, {col3}")
                neg_found = True

    if not neg_found:
        print(f"{file_path} -> No negative values found.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_negative_pressure.py /path/to/fort.11")
    else:
        check_file(sys.argv[1])

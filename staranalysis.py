import argparse
import csv
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Keep only rows whose 'proper' column has a value.",
    )
    parser.add_argument("filename", help="Input CSV file to clean.")
    return parser.parse_args()


def validate_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {path}")


def read_and_filter(path: Path):
    with path.open("r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError("CSV missing header row.")
        if "proper" not in fieldnames:
            raise ValueError("CSV missing required 'proper' column.")

        filtered_rows = [
            row for row in reader if row.get("proper", "").strip()
        ]
    return fieldnames, filtered_rows


def write_clean_file(path: Path, fieldnames, rows):
    output_path = path.with_name(f"clean{path.name}")
    with output_path.open("w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def main() -> None:
    args = parse_args()
    input_path = Path(args.filename).expanduser().resolve()
    try:
        validate_file(input_path)
        fieldnames, rows = read_and_filter(input_path)
        output_path = write_clean_file(input_path, fieldnames, rows)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Wrote {len(rows)} rows with non-empty 'proper' values to {output_path}")


if __name__ == "__main__":
    main()

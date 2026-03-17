"""Command-line interface for deink."""

import argparse
import sys
from pathlib import Path

from deink.converter import convert


def main():
    parser = argparse.ArgumentParser(
        prog="deink",
        description="Strips colored backgrounds from PDFs for clean printing.",
    )
    parser.add_argument(
        "input",
        nargs="+",
        help="PDF file(s) to process",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (only valid with a single input file)",
    )

    args = parser.parse_args()

    if args.output and len(args.input) > 1:
        print("error: -o/--output cannot be used with multiple input files", file=sys.stderr)
        sys.exit(1)

    errors = 0
    for input_path in args.input:
        path = Path(input_path)
        if not path.exists():
            print(f"error: {input_path}: file not found", file=sys.stderr)
            errors += 1
            continue
        if not path.suffix.lower() == ".pdf":
            print(f"error: {input_path}: not a PDF file", file=sys.stderr)
            errors += 1
            continue

        if args.output:
            output_path = args.output
        else:
            output_path = str(path.with_stem(f"{path.stem}_deink"))

        try:
            convert(input_path, output_path)
            print(f"{output_path}")
        except Exception as e:
            print(f"error: {input_path}: {e}", file=sys.stderr)
            errors += 1

    sys.exit(1 if errors else 0)

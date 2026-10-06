"""Frequency analysis and Polibius cipher tool."""

from __future__ import annotations

import argparse
import sys

import pandas as pd


def read_text(filename: str) -> str:
    """Read text from a file."""
    try:
        with open(filename, encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("File not found")
        sys.exit(2)
    except PermissionError:
        print("Permission denied")
        sys.exit(2)
    except OSError as exc:
        print(exc)
        sys.exit(2)


def encode_polibius(text: str, key: pd.DataFrame) -> str:
    """Encode text using the Polibius square."""
    text = text.upper()
    rows, cols = key.shape
    mapping: dict[str, str] = {}

    for i in range(rows):
        for j in range(cols):
            cell = key.iloc[i, j]  # type: ignore[reportUnknownMemberType]
            if not pd.isna(cell) and str(cell).strip():
                mapping[str(cell)] = f"{i + 1}{j + 1}"

    result: str = ""
    for char in text:
        if char in mapping:
            result += mapping[char]
        elif char == " ":
            result += " "
        else:
            result += char
    return result


def decode_polibius(text: str, key: pd.DataFrame) -> str:
    """Decode text using the Polibius square."""
    rows, cols = key.shape
    mapping: dict[str, str] = {}

    for i in range(rows):
        for j in range(cols):
            cell = key.iloc[i, j]  # type: ignore[reportUnknownMemberType]
            if not pd.isna(cell) and str(cell).strip():
                mapping[f"{i + 1}{j + 1}"] = str(cell)

    result: str = ""
    i = 0
    while i < len(text):
        if text[i] == " ":
            result += " "
            i += 1
        elif i + 1 < len(text) and text[i : i + 2] in mapping:
            result += mapping[text[i : i + 2]]
            i += 2
        else:
            result += text[i]
            i += 1
    return result


def write_text(filename: str, text: str) -> None:
    """Write text to a file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
    except PermissionError:
        print("Permission denied")
        sys.exit(2)
    except OSError as exc:
        print(exc)
        sys.exit(2)


def terminal_parsing() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Polibius encode")
    parser.add_argument("--input_file", required=True, help="file with text")
    parser.add_argument("--key", required=True, help="key for encode")
    parser.add_argument("--output_file", required=True, help="file for encode text")
    return parser.parse_args()


def main() -> None:
    """Run the Polibius encode/decode pipeline."""
    args = terminal_parsing()
    text = read_text(args.input_file)
    key = pd.read_excel(args.key)  # type: ignore[reportUnknownMemberType]
    encode_text = encode_polibius(text, key)
    write_text(args.output_file, encode_text)
    decode_text = decode_polibius(encode_text, key)
    print(decode_text)


if __name__ == "__main__":
    main()

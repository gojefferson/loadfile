from typing import List

import click
from colorama import Fore, init as init_colorama
import chardet
import re
import csv
import pathlib
import json
import sys

init_colorama()


ASCII_MATCH = re.compile("[a-zA-Z0-9]")

def get_encoding(filepath) -> str:
    with open(filepath, "rb") as readfile:
        raw = readfile.read()
    det = chardet.detect(raw)
    return det["encoding"]


def get_lines(filepath, encoding) -> List[str]:
    try:
        with open(filepath, encoding=encoding, errors="backslashreplace") as txt_file:
            lines: List[str] = list(txt_file.readlines())
        return lines
    except UnicodeDecodeError as e:
        click.echo(f"Error decoding {filepath}: {e}")
    raise Exception("Could not parse file")


def remove_empty_lines(lines):
    new_lines = []
    for line in lines:
        if len(line) > 1:
            new_lines.append(line)
    return new_lines


def get_rows(lines):
    new_lines = []
    for line in lines:
        new_line = line.split("\x14")
        new_line = [i.strip("þ") for i in new_line]
        new_line = [i.strip("þ\n") for i in new_line]
        new_lines.append(new_line)
    cell_per_line = len(new_lines[0])
    assert cell_per_line > 1
    new_lines = remove_empty_lines(new_lines)
    assert all([len(l) == cell_per_line for l in new_lines])

    fields = new_lines[0]
    rows = []
    for line in new_lines[1:]:
        row = {}
        for i, field_name in enumerate(fields):
            row[field_name] = line[i]
        rows.append(row)

    assert len(rows) == len(new_lines) - 1
    return rows


def make_csv(rows, filepath: pathlib.Path):
    with open(str(filepath), "wt") as writefile:
        writer = csv.DictWriter(writefile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def make_json(cells, filepath: pathlib.Path):
    with open(str(filepath), "wt") as writefile:
        write_text = json.dumps(cells, sort_keys=True, indent=4)
        writefile.write(write_text)


@click.command()
@click.argument("source")
@click.argument("dest")
@click.option(
    "-j",
    "--json",
    is_flag=True,
    help="Whether to convert to JSON, rather than CSV (the default)",
)
def loadfile(source, dest, json):
    """
    Converts a .DAT formatted loadfile to CSV or JSON.

    SOURCE: the the file you wish to convert

    DEST: the directory where the converted file will be created.

    The converted file will have the same name as the original file, with either .csv or
    .json added at the end.
    """

    src_path: pathlib.Path = pathlib.Path(source)
    if json:
        dest_path = pathlib.Path(dest) / f"{src_path.name}.json"
    else:
        dest_path = pathlib.Path(dest) / f"{src_path.name}.csv"
    if src_path.is_file():
        enc = get_encoding(src_path)
        lines = get_lines(src_path, enc)
        rows = get_rows(lines)
        if json:
            make_json(rows, dest_path)
        else:
            make_csv(rows, dest_path)
        click.echo(Fore.GREEN + f"Success: output saved to {dest_path}")
    else:
        click.echo(Fore.RED + f"Oops, {source} is a directory")


if __name__ == "__main__":
    loadfile()

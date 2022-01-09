#!/usr/bin/env python
import argparse
from msgraphy import GraphApi
import msgraphy_util


def main(filenames, batch=False):
    api = GraphApi(scopes=["Files.Read.All"], batch=batch)

    responses = []
    for filename in filenames:
        response = api.files.parse_drive_item(filename)
        responses.append((filename, response))

    for filename, response in responses:
        print(f"Results for {filename}:")
        print(response.value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Print information for a sharepoint path'
    )
    parser.add_argument("filenames", type=str, nargs="+",  help="The sharepoint path(s) to the file to print")
    parser.add_argument("--batch", "-b", action="store_true", help="Batch mode")

    args = parser.parse_args()
    main(**vars(args))

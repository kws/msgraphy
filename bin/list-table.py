import urllib

import msgraphy_util
import argparse
from msgraphy import GraphApi


def main(file, table):
    api = GraphApi()

    drive_item = api.files.parse_drive_item(file).value

    table_api = api.workbook.get_table_api(table, drive_item)
    root_resource = table_api._root_resource

    # range = urllib.parse.quote_plus("address='$A$1:$B$2'")
    resource = f"{root_resource}/columns?$top=1"

    print(api.client.make_request(resource).text)
    # header = table_api.get_header_row_range().value
    # print(header)
    # first_row = table_api.get_row(2)
    # print(first_row.value)
    # rows = table_api.get_rows(top=10).value
    # for ix, row in enumerate(rows):
    #     print(ix, row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='List or search for MS team'
    )
    parser.add_argument("file", type=str, help="The file URL to open")
    parser.add_argument("table", type=str, help="The table to open")

    args = parser.parse_args()
    main(**vars(args))

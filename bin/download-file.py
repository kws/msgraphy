import argparse
from pathlib import Path

from msgraphy import GraphApi


def main(remote_file):
    api = GraphApi(scopes=["Files.Read.All"], batch=True)

    _, filename = api.files.parse_file_path(remote_file)
    response = api.files.parse_drive_item(remote_file)
    drive_item = response.value

    path = Path(filename)

    response = api.files.download_file(drive_item)
    with open(path.name, 'wb') as f:
        for chunk in response.response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Download a file'
    )
    parser.add_argument("remote_file", type=str, help="The sharepoint source: <site>:<folder>")
    args = parser.parse_args()
    main(args.remote_file)

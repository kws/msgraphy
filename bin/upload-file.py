import argparse
from pathlib import Path

from msgraphy import GraphApi
from msgraphy.auth.graph_auth import BasicAuth
from msgraphy.client.graph_client import RequestsGraphClient
from msgraphy.data.sharepoint import SiteResource
import msgraphy_util


def main(local_file, remote_file):
    api = GraphApi(scopes=["Files.ReadWrite.All"])

    local_file = Path(local_file)

    response, filename = api.files.parse_file_path(remote_file)
    drive_root = response.value
    sharepoint_path = filename + "/" + local_file.name

    response = api.files.upload_file(drive_root, sharepoint_path, local_file)
    if not response.ok:
        print(response.text)
    else:
        print("Uploaded file:", response.value.web_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Upload a file'
    )
    parser.add_argument("local_file", type=str, help="The filename of the local file")
    parser.add_argument("remote_file", type=str, help="The sharepoint destination: <site>:<folder>")
    args = parser.parse_args()
    main(args.local_file, args.remote_file)

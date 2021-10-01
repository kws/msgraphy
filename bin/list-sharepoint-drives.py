import argparse
from msgraphy import GraphApi
from msgraphy.auth.graph_auth import BasicAuth
from msgraphy.client.graph_client import RequestsGraphClient
from msgraphy.data.sharepoint import SiteResource


def main(site):
    if site:
        site = SiteResource(name=site)
    else:
        site = SiteResource()

    api = GraphApi(RequestsGraphClient(BasicAuth()))
    response = api.sharepoint.list_drives(site)
    print(response.value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='List drives associated with a sharepoint site'
    )
    parser.add_argument("site", type=str, nargs="?", help="Site name")
    args = parser.parse_args()
    main(args.site)

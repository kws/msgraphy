import argparse
from msgraphy import GraphApi
from msgraphy.auth.graph_auth import BasicAuth
from msgraphy.client.graph_client import RequestsGraphClient
from msgraphy.data.sharepoint import SiteResource


def main(name):
    api = GraphApi(RequestsGraphClient(BasicAuth(scopes=["Sites.Read.All"])))

    response = api.sharepoint.list_sites(search=name)
    for site in response.value:
        print(site, end="\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='List or search for sharepoint sites'
    )
    parser.add_argument("name", type=str, nargs="?", help="show only sites which contains this name")
    args = parser.parse_args()
    main(args.name, )

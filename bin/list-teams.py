import argparse
from msgraphy import GraphApi
from msgraphy.auth.graph_auth import BasicAuth
from msgraphy.client.graph_client import RequestsGraphClient
from msgraphy.data.sharepoint import SiteResource


def main(name):
    api = GraphApi(RequestsGraphClient(BasicAuth(scopes=["Group.Read.All"])))

    response = api.team.list_teams(search=name)
    for team in response.value:
        print(team, end="\n\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='List or search for MS team'
    )
    parser.add_argument("name", type=str, nargs="?", help="show only teams which contains this name")
    args = parser.parse_args()
    main(args.name, )

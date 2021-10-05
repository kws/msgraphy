import argparse
from time import sleep

from msgraphy import GraphApi
from msgraphy.auth.graph_auth import BasicAuth
from msgraphy.client.graph_client import RequestsGraphClient
from msgraphy.data.team import Team
import msgraphy_util


def main(name):
    api = GraphApi(scopes=['Group.ReadWrite.All'])
    response = api.team.list_teams()
    for team in response.value:
        if team.display_name == name or team.id == name:
            print("Deleting team", team.id)
            response = api.group.delete(team.id)
            if not response.ok:
                print(response.text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Delete one or more Teams'
    )
    parser.add_argument("name", type=str, help="The name or id of the team")
    args = parser.parse_args()
    main(args.name)

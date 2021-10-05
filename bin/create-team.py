import argparse
from time import sleep

from msgraphy import GraphApi
from msgraphy.data.team import Team
import msgraphy_util


def main(name, description=None):
    api = GraphApi(scopes=['Team.Create', 'TeamSettings.ReadWrite.All'])
    team = Team(display_name=name, description=description)

    response = api.team.create_team(team)
    location = response.headers.get('Location')

    sleep(1)
    response = api.client.make_request(location).value
    while response.get("status") != 'succeeded':
        print("Creating team:", response.get("status"), end="\r")
        sleep(1)
        response = api.client.make_request(location).value

    print(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create an MS team'
    )
    parser.add_argument("name", type=str, help="The name of the team")
    parser.add_argument("--description", "-d", type=str, nargs="?", help="Team description")
    args = parser.parse_args()
    main(**vars(args))

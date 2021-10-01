import argparse
from time import sleep

from msgraphy import GraphApi
from msgraphy.auth.graph_auth import BasicAuth
from msgraphy.client.graph_client import RequestsGraphClient
from msgraphy.data.team import Team


def main(name):
    client = RequestsGraphClient(BasicAuth(scopes=['Team.Create', 'TeamSettings.ReadWrite.All']))
    api = GraphApi(client)

    team = Team(display_name=name)

    response = api.team.create_team(team)
    team_id = response.headers.get('Content-Location')
    location = response.headers.get('Location')

    sleep(1)
    response = client.make_request(location).value
    while response.get("status") != 'succeeded':
        sleep(.5)
        response = client.make_request(location).value

    print(response)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create an MS team'
    )
    parser.add_argument("name", type=str, help="The name of the team")
    args = parser.parse_args()
    main(args.name)

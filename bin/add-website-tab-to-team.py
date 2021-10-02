import argparse
from msgraphy import GraphApi

def main(team_id, channel, tab_name, tab_url):
    api = GraphApi(scopes=['Team.Create', 'TeamSettings.ReadWrite.All'])

    response = api.team.get_team(team_id)
    team = response.value
    print(team)

    channel_id = None
    if channel:
        response = api.team.list_channels(team_id)
        for ch in response.value:
            if ch.display_name.lower() == channel.lower():
                channel_id = ch.id
                break
    else:
        response = api.team.get_primary_channel(team_id)
        channel_id = response.value.id

    if not channel_id:
        raise Exception("Channel not found")

    response = api.team.add_tab_to_channel(team_id, channel_id, tab_name, tab_url)
    if response.ok:
        print("Created tab", response.value)
    else:
        print("Failed to create tab", response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Add a website tab to a team'
    )
    parser.add_argument("team_id", type=str, help="The team id")
    parser.add_argument("tab_name", type=str, help="The tab name")
    parser.add_argument("tab_url", type=str, help="The tab url")
    parser.add_argument("--channel", "-c", type=str, nargs="?", help="The channel name, otherwise default channel")

    args = parser.parse_args()
    main(args.team_id, args.channel, args.tab_name, args.tab_url)
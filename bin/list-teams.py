import msgraphy_util
import argparse
from msgraphy import GraphApi


def main(name, starts_with, channels, folder):
    api = GraphApi(scopes=["Group.Read.All"])

    response = api.team.list_teams(search=name, starts_with=starts_with)
    for team in response.value:
        print(f"{team.display_name} [{team.id}]")
        print(team.description)
        if channels or folder:
            response = api.team.list_channels(team.id)
            for ch in response.value:
                print(f"* {ch.display_name} [{ch.id}]")
                if folder:
                    response = api.team.get_channel_files_folder(team.id, ch.id)
                    if response.ok:
                        folder = response.value
                        print(f"  {folder.web_url}")
                    else:
                        print("  [Folder not found]")
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='List or search for MS team'
    )
    parser.add_argument("name", type=str, nargs="?",  help="show only teams which contains [name]")
    parser.add_argument("--starts_with", "-s", type=str, nargs="?", metavar="value", help="only teams starting with [value]")
    parser.add_argument("--channels", "-c", action='store_true', help="include channels")
    parser.add_argument("--folder", "-f", action='store_true', help="include channel folder (implies -c)")

    args = parser.parse_args()
    main(**vars(args))

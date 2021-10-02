import argparse
from msgraphy import GraphApi
from msgraphy.data.sharepoint import SiteResource


def main(site):
    api = GraphApi(scopes="Files.Read.All")

    if site:
        site = SiteResource(name=site)
    else:
        site = SiteResource()

    response = api.sharepoint.list_drives(site)
    print(response.value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='List drives associated with a sharepoint site'
    )
    parser.add_argument("site", type=str, nargs="?", help="Site name")
    args = parser.parse_args()
    main(args.site)

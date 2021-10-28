import argparse
from msgraphy import GraphApi
from msgraphy.data.sharepoint import SiteResource
import msgraphy_util


def main(folder, role, grantee, set=None):
    api = GraphApi(scopes="Files.Read.All")
    item = api.files.parse_drive_item(folder).value
    print(f"Request permissions for: {item.get_api_reference()}")

    if set:
       grantee, role = set
       response = api.files.list_permissions(item, granted_to=grantee)
       perms = response.value['value']
       for p in perms:
           granted_roles = p['roles']
           if role not in granted_roles:
               print(f"Updating {p['id']} ", end="")
               response = api.files.update_permission(item, p['id'], role)
               print("OK" if response.ok else "FAILED")
               if not response.ok:
                   print(response.text)
    else:
        response = api.files.list_permissions(
            item,
            role=role[0] if role else None,
            granted_to=grantee[0] if grantee else None,
        )
        perms = response.value['value']
        for p in perms:
            print(p, end="\n\n")

        #
        # if p.get('grantedToV2', {}).get('siteGroup', {}).get("loginName", "").endswith('Members'):
        #     print(p)
        #     print("")
        #     response = api.client.make_request(
        #         f"{item.get_api_reference()}/permissions/{p['id']}",
        #         method="patch",
        #         json=dict(roles=['read']),
        #     )
        #     print(response.value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Get permissions for a drive item'
    )
    parser.add_argument("folder", type=str, help="Item path")
    parser.add_argument("--role", "-r", nargs=1, default=None)
    parser.add_argument("--grantee", "-g", nargs=1, default=None)
    parser.add_argument("--set", "-s", nargs=2, metavar=('GRANTEE', 'ROLE'))

    args = parser.parse_args()
    main(**vars(args))

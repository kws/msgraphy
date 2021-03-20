import urllib
from typing import Tuple

from msgraphy.data.file import Drive, DriveItem, BaseItem
from msgraphy.data.monitor import Monitor
from msgraphy.client.graph_client import GraphResponse


class FilesGraphApi:

    def __init__(self, api):
        self._api = api

    def parse_file_path(self, filename: str) -> Tuple[Drive, str]:
        """
        This is a utility method that looks up drive and file data based on a set of fixed formats:

        * <EmailAddress>:path/to/file
        * <SiteName>:path/to/file
        * <SiteName>/<LibraryName>:path/to/file

        For the root site, leave <SiteName> blank, and for the root folder, leave path blank

        :param filename:
        :return:
        """
        if filename.startswith("sharepoint:"):
            filename = filename[11:]

        drivename, filename = filename.split(":", 1)
        if '@' in drivename:
            user = self._api.user.get_user_by_email(email=drivename).value
            drive = self._api.user.get_user_drive(user).value
        elif '/' in drivename:
            sitename, drivename = drivename.split("/", 1)
            site = self._api.sharepoint.get_site_resource(name=sitename)
            drive = self._api.sharepoint.get_drive_by_name(site, drivename).value
        else:
            site = self._api.sharepoint.get_site_resource(drivename)
            drive = self._api.sharepoint.get_drive_by_name(site).value

        return drive, filename

    def parse_drive_item(self, filename: str) -> GraphResponse[DriveItem]:
        """
        This is a utility method that looks up a driveitem by "special path" as accepted by parse_file_path.

        :param filename:
        :return: A drive item
        """
        drive, filename = self.parse_file_path(filename)
        return self.get_file_by_name(drive, filename)

    def get_file_by_name(self, drive: Drive, filename: str) -> GraphResponse[DriveItem]:
        assert drive.id
        assert filename is not None

        if not filename.startswith("/"):
            filename = "/" + filename

        resource = f"/drives/{urllib.parse.quote(drive.id)}/root"
        if filename and filename != "/":
            resource += f":{filename}"

        return self._api.client.make_request(url=resource, method="get", response_type=DriveItem)

    def copy(self, item: BaseItem, new_parent_ref: BaseItem = None,
             new_name: str = None, conflict_behaviour=None) -> GraphResponse[Monitor]:
        """

        :param item:
        :param new_parent_ref:
        :param new_name:
        :param conflict_behaviour: The conflict resolution behavior for actions that create a new item.
                                    You can use the values fail, replace, or rename.
        :return:
        """
        assert new_parent_ref or new_name, "Must either set 'new_parent_ref' or 'new_name'"

        body = {}
        if new_name:
            body['name'] = new_name
        if new_parent_ref:
            body['parentReference'] = dict(
                driveId=new_parent_ref.parent_reference.drive_id,
                id=new_parent_ref.id,
            )

        params = {}
        if conflict_behaviour:
            params['@microsoft.graph.conflictBehavior'] = conflict_behaviour

        resource = f"{item.get_api_reference()}/copy"
        return self._api.client.make_request(url=resource, method="post", params=params,
                                             json=body, response_type=Monitor)

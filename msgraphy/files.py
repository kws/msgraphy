import urllib
from typing import Tuple

from msgraphy.data.file import Drive, DriveItem


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
            user = self._api.user.get_user_by_email(email=drivename)
            drive = self._api.user.get_user_drive(user)
        elif '/' in drivename:
            sitename, drivename = drivename.split("/", 1)
            site = self._api.sharepoint.get_site_resource(name=sitename)
            drive = self._api.sharepoint.get_drive_by_name(site, drivename)
        else:
            site = self._api.sharepoint.get_site_resource(drivename)
            drive = self._api.sharepoint.get_drive_by_name(site)

        return drive, filename

    def parse_drive_item(self, filename: str) -> DriveItem:
        """
        This is a utility method that looks up a driveitem by "special path" as accepted by parse_file_path.

        :param filename:
        :return: A drive item
        """
        drive, filename = self.parse_file_path(filename)
        return self.get_file_by_name(drive, filename)

    def get_file_by_name(self, drive: Drive, filename: str) -> DriveItem:
        assert drive.id
        assert filename is not None

        if not filename.startswith("/"):
            filename = "/" + filename

        resource = f"/drives/{urllib.parse.quote(drive.id)}/root"
        if filename and filename != "/":
            resource += f":{filename}"

        response = self._api.client.make_request(url=resource, method="get")
        return DriveItem(response.json())

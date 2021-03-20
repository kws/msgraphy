from typing import Union

from extras.graph_api.data.file import DriveList, Drive
from extras.graph_api.data.sharepoint import SiteResource, Site


class SharepointGraphApi:
    def __init__(self, api):
        self._api = api

    def get_site_resource(self, name=None, site_collection: dict = None) -> SiteResource:
        if site_collection is None:
            site_collection = dict(hostname=self._api.client._config["root_site"])

        return SiteResource(name=name, site_collection=site_collection)

    def get_site(self, site: SiteResource) -> Site:
        response = self._api.client.make_request(url=site.resource)
        return Site(response.json())

    def list_drives(self, site: SiteResource) -> DriveList:
        resource = site.resource + "/drives"
        response = self._api.client.make_request(url=resource)
        return DriveList(response.json())

    def get_drive_by_name(self, site: SiteResource, name: str = "Documents") -> Union[Drive, None]:
        drives = self.list_drives(site)
        for d in drives:
            if d.name == name:
                return d

        return None

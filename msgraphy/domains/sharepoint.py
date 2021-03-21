from typing import Union

from msgraphy.data.file import DriveList, Drive
from msgraphy.data.sharepoint import SiteResource, Site
from msgraphy.client.graph_client import GraphResponse


class SharepointGraphApi:
    def __init__(self, api):
        self._api = api

    def get_site_resource(self, name=None, site_collection: dict = None) -> SiteResource:
        if site_collection is None:
            site_collection = dict(hostname=self._api.client._config["root_site"])

        return SiteResource(name=name, site_collection=site_collection)

    def get_site(self, site: SiteResource) -> GraphResponse[Site]:
        return self._api.client.make_request(url=site.resource, response_type=Site)

    def list_drives(self, site: SiteResource) -> GraphResponse[DriveList]:
        resource = site.resource + "/drives"
        return self._api.client.make_request(url=resource, response_type=DriveList)

    def get_drive_by_name(self, site: SiteResource, name: str = "Documents") -> GraphResponse[Union[Drive, None]]:
        def name_filter(data):
            drives = DriveList(data)
            for d in drives:
                if d.name == name:
                    return d

        resource = site.resource + "/drives"
        return self._api.client.make_request(url=resource, response_type=name_filter)
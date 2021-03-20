from datetime import datetime

from extras.graph_api.data import graphdataclass


@graphdataclass
class SharePointIds:
    list_id: str = None
    list_item_id: str = None
    list_item_unique_id: str = None
    site_id: str = None
    site_url: str = None
    tenant_id: str = None
    web_id: str = None


@graphdataclass
class SiteResource:
    name: str
    site_collection: dict

    @property
    def resource(self):
        resource = f"sites/{self.site_collection['hostname']}"
        if self.name is not None and self.name != "":
            resource += f":/sites/{self.name}:"
        return resource


@graphdataclass
class Site(SiteResource):
    display_name: str
    id: str
    description: str
    created_date_time: datetime
    last_modified_date_time:  datetime
    web_url: str
    root: str

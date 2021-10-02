from contextlib import contextmanager

from msgraphy.auth.graph_auth import BasicAuth
from msgraphy.client.graph_client import RequestsGraphClient
from msgraphy.domains.files import FilesGraphApi
from msgraphy.domains.group import GroupGraphApi
from msgraphy.domains.list import ListGraphApi
from msgraphy.domains.monitor import MonitorGraphApi
from msgraphy.domains.sharepoint import SharepointGraphApi
from msgraphy.domains.team import TeamGraphApi
from msgraphy.domains.user import UserGraphApi
from msgraphy.domains.workbook import WorkbookGraphApi


class GraphApi:

    def __init__(self, client=None, scopes=None, is_batch=False):
        if not client:
            client = RequestsGraphClient(BasicAuth(scopes=scopes))
        elif scopes:
            raise Exception("Cannot both set client and scopes")

        self.client = client
        self._is_batch = is_batch

        self.files = FilesGraphApi(self)
        self.group = GroupGraphApi(self)
        self.list = ListGraphApi(self)
        self.monitor = MonitorGraphApi(self)
        self.sharepoint = SharepointGraphApi(self)
        self.team = TeamGraphApi(self)
        self.user = UserGraphApi(self)
        self.workbook = WorkbookGraphApi(self)

    @contextmanager
    def batch(self):
        if self._is_batch:
            return self
        from msgraphy.client.graph_batch import BatchGraphClient
        client = BatchGraphClient(self.client)
        batch_api = GraphApi(client=client, is_batch=True)
        try:
            yield batch_api
        finally:
            client.flush()

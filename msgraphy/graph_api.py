from contextlib import contextmanager


class GraphApi:

    def __init__(self, client, is_batch=False):
        from msgraphy.files import FilesGraphApi
        from msgraphy.sharepoint import SharepointGraphApi
        from msgraphy.user import UserGraphApi
        from msgraphy.workbook import WorkbookGraphApi

        self.client = client
        self.files = FilesGraphApi(self)
        self.user = UserGraphApi(self)
        self.sharepoint = SharepointGraphApi(self)
        self.workbook = WorkbookGraphApi(self)
        self._is_batch = is_batch

    @contextmanager
    def batch(self):
        if self._is_batch:
            return self
        from msgraphy.graph_batch import BatchGraphClient
        client = BatchGraphClient(self.client)
        batch_api = GraphApi(client=client, is_batch=True)
        try:
            yield batch_api
        finally:
            client.flush()

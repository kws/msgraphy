import importlib
from contextlib import contextmanager


class GraphApi:
    __parts = {
        'files': 'msgraphy.domains.files.FilesGraphApi',
        'monitor': 'msgraphy.domains.monitor.MonitorGraphApi',
        'sharepoint': 'msgraphy.domains.sharepoint.SharepointGraphApi',
        'user': 'msgraphy.domains.user.UserGraphApi',
        'workbook': 'msgraphy.domains.workbook.WorkbookGraphApi',
    }

    def __init__(self, client, is_batch=False):
        self.client = client
        self._is_batch = is_batch
        self.__api_parts = {}

    def __getattr__(self, item):
        prop = self.__api_parts.get(item)
        if prop:
            return prop
        elif item in self.__parts:
            module = self.__parts[item]
            p, cls = module.rsplit('.', 1)
            p = importlib.import_module(p)
            cls = getattr(p, cls)
            instance = cls(self)
            self.__api_parts[item] = instance
            return instance
        else:
            raise AttributeError(item)

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

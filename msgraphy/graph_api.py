
class GraphApi:

    def __init__(self, token_store, **kwargs):
        from extras.graph_api.files import FilesGraphApi
        from extras.graph_api.graph_client import GraphClient
        from extras.graph_api.sharepoint import SharepointGraphApi
        from extras.graph_api.user import UserGraphApi
        from extras.graph_api.workbook import WorkbookGraphApi

        self.client = GraphClient(token_store, **kwargs)
        self.files = FilesGraphApi(self)
        self.user = UserGraphApi(self)
        self.sharepoint = SharepointGraphApi(self)
        self.workbook = WorkbookGraphApi(self)



class GraphApi:

    def __init__(self, token_store, **kwargs):
        from msgraphy.files import FilesGraphApi
        from msgraphy.graph_client import GraphClient
        from msgraphy.sharepoint import SharepointGraphApi
        from msgraphy.user import UserGraphApi
        from msgraphy.workbook import WorkbookGraphApi

        self.client = GraphClient(token_store, **kwargs)
        self.files = FilesGraphApi(self)
        self.user = UserGraphApi(self)
        self.sharepoint = SharepointGraphApi(self)
        self.workbook = WorkbookGraphApi(self)


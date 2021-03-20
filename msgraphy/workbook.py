from contextlib import contextmanager
from typing import Union, List

from msgraphy.data.file import DriveItem
from msgraphy.data.workbook import TableList, WorkbookSessionInfo, WorkbookTableRow, WorkbookTableRowList, \
    WorkbookTableColumnList, WorkbookRange


class WorkbookGraphApi:

    def __init__(self, api: "....GraphApi"):
        self._api = api

    def list_tables(self, drive_item: DriveItem) -> TableList:
        resource = f"{drive_item.get_api_reference()}/workbook/tables"
        response = self._api.client.make_request(url=resource)
        return TableList(response.json())

    def create_session(self, drive_item: DriveItem) -> WorkbookSessionInfo:
        resource = f"{drive_item.get_api_reference()}/workbook/createSession"
        response = self._api.client.make_request(url=resource, method="post")
        return WorkbookSessionInfo(response.json(), workbook_reference=drive_item)

    def close_session(self, session: WorkbookSessionInfo):
        resource = f"{session.workbook_reference.get_api_reference()}/workbook/closeSession"
        self._api.client.make_request(url=resource, method="post", headers=session.headers())

    @contextmanager
    def session_context(self, drive_item: DriveItem):
        session = self.create_session(drive_item)
        try:
            yield session
        finally:
            self.close_session(session)

    def get_table_api(self, table_name: str, workbook: Union[DriveItem, WorkbookSessionInfo]):
        if isinstance(workbook, WorkbookSessionInfo):
            return TableGraphApi(self._api, workbook.workbook_reference, table_name, workbook)
        else:
            return TableGraphApi(self._api, workbook, table_name)


class TableGraphApi:

    def __init__(self, api: "....GraphApi", workbook: DriveItem, table_name: str, session: WorkbookSessionInfo = None):
        self._api = api
        self._workbook = workbook
        self._table_name = table_name
        self._session = session
        self._root_resource = f"{workbook.get_api_reference()}/workbook/tables/{table_name}"

    def __make_request(self, *args, headers=None, **kwargs):
        """ We use an internal method to make requests and ensure we always have session info if set"""
        if self._session:
            headers = {**headers, **self._session.headers()} if headers else {**self._session.headers()}
        return self._api.client.make_request(*args,  headers=headers, **kwargs)

    def get_table(self, select: str = None):
        resource = f"{self._root_resource}"
        params = {}
        if select:
            params['$select'] = select
        response = self.__make_request(url=resource, params=params)
        return response.json()

    def get_rows(self, index: int = None, top: int = None, skip: int = None) -> WorkbookTableRowList:
        resource = f"{self._root_resource}/rows"
        params = None
        if index is not None:
            resource += f"/itemAt(index={index})"
        else:
            params = {}
            if top is not None:
                params['$top'] = top
            if skip is not None:
                params['$skip'] = skip

        response = self.__make_request(url=resource, params=params)
        return WorkbookTableRowList(response.json())

    def get_columns(self, index: int = None, top: int = None, skip: int = None) -> WorkbookTableColumnList:
        resource = f"{self._root_resource}/columns"
        params = None
        if index is not None:
            resource += f"/itemAt(index={index})"
        else:
            params = {}
            if top is not None:
                params['$top'] = top
            if skip is not None:
                params['$skip'] = skip

        response = self.__make_request(url=resource, params=params)
        return WorkbookTableColumnList(response.json())

    def get_range(self, select=None) -> WorkbookRange:
        resource = f"{self._root_resource}/range"
        params = {}
        if select:
            params['$select'] = select
        response = self.__make_request(url=resource, params=params)
        return WorkbookRange(response.json())

    def get_data_body_range(self, select=None) -> WorkbookRange:
        resource = f"{self._root_resource}/dataBodyRange"
        params = {}
        if select:
            params['$select'] = select
        response = self.__make_request(url=resource, params=params)
        return WorkbookRange(response.json())

    def add_rows(self, values: List):
        resource = f"{self._root_resource}/rows/add"
        response = self.__make_request(url=resource, json=dict(values=values), method="post")
        return response.json()

    def update_row(self, index: int, values: List):
        resource = f"{self._root_resource}/rows/itemAt(index={index})"
        response = self.__make_request(url=resource, json=dict(index=index, values=values), method="patch")
        return response.json()

    def delete_row(self, index: int):
        resource = f"{self._root_resource}/rows/itemAt(index={index})"
        self.__make_request(url=resource, method="delete")

    def delete_range(self):
        resource = f"{self._root_resource}/range/delete"
        self.__make_request(url=resource, method="post")

    def delete_data_body_range(self):
        resource = f"{self._root_resource}/dataBodyRange/delete"
        self.__make_request(url=resource, method="post")

    def get_filter_criteria(self, index: int):
        resource = f"{self._root_resource}/columns/itemAt(index={index})/filter"
        response = self.__make_request(url=resource, method="get")
        return response.json()

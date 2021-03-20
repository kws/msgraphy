import abc
from typing import TypeVar, Generic
import requests

from msgraphy.auth.graph_auth import TokenStore, login

T = TypeVar('T')


class GraphResponse(Generic[T]):

    @property
    @abc.abstractmethod
    def ready(self) -> bool:
        return NotImplemented

    @property
    @abc.abstractmethod
    def ok(self) -> bool:
        return NotImplemented

    @property
    @abc.abstractmethod
    def value(self) -> T:
        return NotImplemented


class RequestsGraphResponse(GraphResponse[T]):
    def __init__(self, response: requests.Response, response_type: T):
        self.__response = response
        self.__response_type = response_type

    @property
    def ready(self) -> bool:
        return True

    @property
    def ok(self) -> bool:
        return self.__response.ok

    @property
    def text(self) -> str:
        return self.__response.text

    @property
    def response(self) -> requests.Response:
        return self.__response

    @property
    def value(self) -> T:
        self.__response.raise_for_status()
        if hasattr(self.__response_type, 'from_response'):
            return self.__response_type.from_response(self.__response)
        else:
            data = self.__response.json()
            return self.__response_type(data)


class GraphClient(abc.ABC):
    @abc.abstractmethod
    def make_request(self, url, method="get", headers=None, response_type: T = dict, **kwargs) -> GraphResponse[T]:
        return NotImplemented


class RequestsGraphClient(GraphClient):
    DEFAULTS = dict(
        root_url="https://graph.microsoft.com/v1.0/",
        scope='https://graph.microsoft.com/.default',
        grant_type='client_credentials',
    )

    def __init__(self, token_store: TokenStore, **kwargs):
        self._config = dict(**RequestsGraphClient.DEFAULTS, **kwargs)
        self._token_store = token_store
        self._token: TokenStore.Token = self._token_store.load_token()

    @property
    def __access_token(self) -> str:
        if self._token is None or self._token.almost_expired():
            self._token = login(**self._config)
            self._token_store.save_token(self._token)

        return self._token.access_token

    def make_request(self, url, method="get", headers=None, response_type: T = dict, use_auth=True, **kwargs) -> GraphResponse[T]:
        if use_auth:
            headers = headers if headers else {}
            headers = {**headers, "Authorization": f'Bearer {self.__access_token}'}

        if not url.startswith("http"):
            url = f"{self._config['root_url']}{url}"
        response = requests.request(method, url, headers=headers, **kwargs)
        return RequestsGraphResponse(response, response_type)



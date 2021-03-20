import sys
from typing import Iterable
import requests
from requests import HTTPError

from msgraphy.graph_auth import TokenStore


class GraphClient:

    DEFAULTS = dict(
        root_url="https://graph.microsoft.com/v1.0/",
        scope='https://graph.microsoft.com/.default',
        grant_type='client_credentials',
    )

    def __init__(self, token_store: TokenStore, **kwargs):
        self._config = dict(**GraphClient.DEFAULTS, **kwargs)
        self._token_store = token_store
        self._token: TokenStore.Token = self._token_store.load_token()

    @property
    def __access_token(self) -> str:
        if self._token is None or self._token.almost_expired():
            self.__login()

        return self._token.access_token

    def __login(self):
        data = {
            'client_id': self._config['client_id'],
            'client_secret': self._config['client_secret'],
            'scope': self._config['scope'],
            'grant_type': self._config['grant_type'],
        }

        assert self._config["tenant"], "No tenant in config"

        response = requests.post(
            url=f'https://login.microsoftonline.com/{self._config["tenant"]}/oauth2/v2.0/token',
            data=data
        )
        response.raise_for_status()
        self._token = TokenStore.Token.from_dict(response.json())
        self._token_store.save_token(self._token)

    def make_request(self, url, **kwargs):
        method = kwargs.get("method", "get")
        headers = kwargs.get("headers", {})
        if "method" in kwargs:
            del kwargs['method']
        if "headers" in kwargs:
            del kwargs['headers']

        headers = {**headers, "Authorization": f'Bearer {self.__access_token}'}

        response = requests.request(method, f"{self._config['root_url']}{url}", headers=headers, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError as e:
            sys.stderr.write(response.text)
            raise e

        return response

    def batch(self, request_map: [dict, Iterable]):
        if not isinstance(request_map, dict):
            request_map = {p['id']: p for p in request_map}

        all_requests = []
        for key, req in request_map.items():
            method = req.get("method", "get").upper()
            values = dict(id=str(key), method=method, url=req['url'])
            if "headers" in req:
                values["headers"] = req["headers"]
            all_requests.append(values)

        response = self.make_request(
            "$batch",
            method="post",
            json=dict(requests=all_requests)
        )

        all_responses = response.json().get("responses", [])

        return {r['id']: r for r in all_responses}

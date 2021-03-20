import uuid
from typing import TypeVar

from msgraphy.graph_client import GraphClient, GraphResponse

T = TypeVar('T')


class StateError(Exception):
    def __init__(self, *args):
        super(StateError, self).__init__(*args)


class RequestsGraphResponse(GraphResponse[T]):
    def __init__(self, id, response_type):
        self.id = id
        self.response_type = response_type
        self.response = None

    @property
    def ready(self) -> bool:
        return self.response is not None

    @property
    def ok(self) -> bool:
        try:
            return self.response.ok
        except AttributeError:
            raise StateError("Response is not ready.")

    @property
    def value(self) -> T:
        try:
            data = self.response['body']
            return self.response_type(data)
        except AttributeError:
            raise StateError("Response is not ready.")


class BatchGraphClient(GraphClient):

    def __init__(self, client: GraphClient):
        self.__client = client
        self.__requests = []
        self.__responses = {}

    def make_request(self, url, method="get", headers=None, response_type: T = dict, **kwargs) -> GraphResponse[T]:
        id = str(uuid.uuid4())

        method = method.upper()
        values = dict(id=id, method=method, url=url)
        if headers:
            values['headers'] = headers

        response = RequestsGraphResponse(id, response_type=response_type)

        self.__requests.append(values)
        self.__responses[id] = response
        self.flush(threshold=20)

        return response

    def flush(self, threshold=0, batch_size=20):
        """
        Flush all requests until there remain less than threshold.
        With a threshold of 0 all requests are flushed
        """
        while len(self.__requests) >= threshold:
            batch = self.__requests[0:batch_size]
            if not batch:
                return

            self.__requests = self.__requests[batch_size:]
            response = self.__client.make_request("$batch", method="post", json=dict(requests=batch))
            for r in response.value["responses"]:
                self.__responses.pop(r['id']).response = r

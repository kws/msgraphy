from msgraphy.data.file import Drive
from msgraphy.data.user import User, UserList
from msgraphy.client.graph_client import GraphResponse


class UserGraphApi:

    def __init__(self, api):
        self._api = api

    def get_user_by_principal(self, id: str) -> GraphResponse[User]:
        return self._api.client.make_request(url=f"/users/{id}", response_type=User)

    def get_user_by_email(self, email: str) -> GraphResponse[User]:
        def find_first(data):
            return UserList(data).value[0]

        return self._api.client.make_request(
            url=f"/users?$filter=startswith(mail,'{email}')",
            method="get",
            response_type=find_first
        )

    def get_user_drive(self, user: User) -> GraphResponse[Drive]:
        assert user.id
        return self._api.client.make_request(url=f"/users/{user.id}/drive", method="get", response_type=Drive)

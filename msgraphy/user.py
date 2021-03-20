from msgraphy.data.file import Drive
from msgraphy.data.user import User


class UserGraphApi:

    def __init__(self, api):
        self._api = api

    def get_user_by_email(self, email: str) -> User:
        response = self._api.client.make_request(url=f"/users?$filter=startswith(mail,'{email}')", method="get")
        response = response.json()
        value = response.get("value", [])
        if len(value) == 0:
            raise Exception("No user found")
        elif len(value) > 1:
            raise Exception("Multiple matching users found")
        return User(value[0])

    def get_user_drive(self, user: User) -> Drive:
        assert user.id
        response = self._api.client.make_request(url=f"/users/{user.id}/drive", method="get")
        return Drive(response.json())

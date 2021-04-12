import atexit
from pathlib import Path
from typing import List, Union
import msal


class FileSystemTokenCache(msal.SerializableTokenCache):
    """
    A very basic implementation of the MSAL SerializableTokenCache that stores the cached credentials
    in a file.

    Think carefully before using whether this is safe enough for your purposes. Ideally use as a wrapper around
    your protected credential store.
    """

    def __init__(self, filename: Union[str, Path], save_on_exit=False):
        self.__filename = filename
        super(FileSystemTokenCache, self).__init__()
        self.load()
        if save_on_exit:
            atexit.register(self.save)

    def load(self):
        try:
            with open(self.__filename, 'r') as file:
                self.deserialize(file.read())
        except:
            pass

    def save(self):
        with open(self.__filename, 'w') as file:
            file.write(self.serialize())


class InteractiveTokenWrapper:
    """
    Provides your API with a way of getting up-to-date credentials.

    Fetches a new token if your token has expired or is about to expire, but does not validate the
    token this in any way, nor is it aware of any exception in the client layer.


    To use this, simply pass to the Graph Client:
    RequestsGraphClient(InteractiveTokenWrapper(PublicClientApplication(....), ['Scope1', 'Scope2']))

    """

    def __init__(self, app: msal.PublicClientApplication, scopes: List[str]):
        self.__app = app
        self.__scopes = scopes

    def __call__(self):
        for account in self.__app.get_accounts():
            result = self.__app.acquire_token_silent(self.__scopes, account=account)
            if result and 'access_token' in result and result.get('expires_in', 0) > 30:
                return result['access_token']

        result = self.__app.acquire_token_interactive(self.__scopes)
        return result['access_token']

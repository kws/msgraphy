import abc
from dataclasses import dataclass
from time import time


class TokenStore(abc.ABC):

    @dataclass
    class Token:
        """An OAUTH token."""
        access_token: str
        expires_at: float

        def expired(self):
            if self.expires_at is None:
                return True
            else:
                return self.expires_at <= time()

        def almost_expired(self, delta=30):
            if self.expires_at is None:
                return True
            else:
                return self.expires_at <= time() + delta

        def as_dict(self) -> dict:
            return dict(access_token=self.access_token, expires_at=self.expires_at)

        @classmethod
        def from_dict(cls, token: dict):
            expires_at = token.get("expires_at")
            if expires_at is None:
                expires_at = time() + token.get('expires_in', 0)
            return TokenStore.Token(
                access_token=token.get("access_token"),
                expires_at=expires_at,
            )

    @abc.abstractmethod
    def load_token(self) -> Token:
        """
        Loads a token
        :return: token
        """
        return NotImplemented

    @abc.abstractmethod
    def save_token(self, token: Token):
        """
        Saves the token
        """
        return NotImplemented


class FileTokenStore(TokenStore):
    import json

    def __init__(self, filename):
        self.filename = filename

    def load_token(self) -> TokenStore.Token:
        try:
            with open(self.filename, 'rt') as fp:
                data = self.json.load(fp)
                return TokenStore.Token.from_dict(data)
        except FileNotFoundError:
            return None

    def save_token(self, token: TokenStore.Token):
        with open(self.filename, 'wt') as fp:
            data = token.as_dict()
            self.json.dump(data, fp)

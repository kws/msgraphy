import os


class MSGraphyConfig:

    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 tenant_id=None,
                 authority=None,
                 device_flow=None,
                 token_cache_file=None,
                 env_prefix="MSGRAPHY"
                 ):

        if not client_id:
            client_id = os.environ[f'{env_prefix}_CLIENT_ID']
        self.client_id = client_id

        if not client_secret:
            client_secret = os.getenv(f'{env_prefix}_CLIENT_SECRET')
        self.client_secret = client_secret

        if not tenant_id:
            tenant_id = os.getenv(f'{env_prefix}_TENANT_ID')
        self.tenant_id = tenant_id

        if not authority:
            authority = os.getenv(f'{env_prefix}_AUTHORITY')

        if device_flow is None:
            device_flow = os.getenv(f'{env_prefix}_DEVICE_FLOW')

        if isinstance(device_flow, str):
            if device_flow.lower() in ['true', '1', 'yes', 'y', 't']:
                from .graph_auth import default_device_flow_handler
                device_flow = default_device_flow_handler
            else:
                try:
                    from pkgutil import resolve_name
                except ImportError:
                    raise Exception("Using resolver plugins requires Python >= 3.9")
                device_flow = resolve_name(device_flow)
        self.device_flow = device_flow

        if not authority:
            if tenant_id:
                authority = f"https://login.microsoftonline.com/{tenant_id}"
            else:
                raise Exception("Either 'authority' or 'tenant_id' must be set")

        self.authority = authority

        if not token_cache_file:
            token_cache_file = os.getenv(f'{env_prefix}_TOKEN_CACHE_FILE')
        self.token_cache_file = token_cache_file


class UserSettingsConfig:

    def __init__(self, app_id):
        import usersettings
        self.__settings = s = usersettings.Settings(app_id)
        s.add_setting("client_id", str, default="")
        s.add_setting("client_secret", str, default="")
        s.add_setting("authority", str, default="")
        s.add_setting("device_flow", bool, default=False)

        s.load_settings()

    @property
    def token_cache_file(self):
        return f"{self.__settings.settings_directory}/token_cache.bin"

    @property
    def client_id(self):
        return self.__settings.client_id

    @client_id.setter
    def client_id(self, value):
        self.__settings.client_id = value
        self.save()

    @property
    def client_secret(self):
        return self.__settings.client_secret

    @client_secret.setter
    def client_secret(self, value):
        self.__settings.client_secret = value
        self.save()

    @property
    def device_flow(self):
        return self.__settings.device_flow

    @device_flow.setter
    def device_flow(self, value: bool):
        self.__settings.device_flow = value
        self.save()

    @property
    def authority(self):
        return self.__settings.authority

    @authority.setter
    def authority(self, value):
        if "http" in value:
            self.__settings.authority = value
        else:
            self.__settings.authority = f"https://login.microsoftonline.com/{value}"
        self.save()

    def save(self):
        self.__settings.save_settings()


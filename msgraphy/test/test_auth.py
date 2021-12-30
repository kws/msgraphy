import os
from unittest import mock

import pytest

from msgraphy.auth.config import MSGraphyConfig


@mock.patch.dict(os.environ, {
    "MSGRAPHY_CLIENT_ID": "--client-id--",
    "MSGRAPHY_CLIENT_SECRET": "--client-secret--",
    "MSGRAPHY_TENANT_ID": "--tenant-id--",
})
def test_config_environ():
    config = MSGraphyConfig()
    assert config.client_id == "--client-id--"
    assert config.client_secret == "--client-secret--"
    assert config.tenant_id == "--tenant-id--"


def test_config_no_environ():
    with pytest.raises(KeyError):
        config = MSGraphyConfig()


def test_config_init_args():
    config = MSGraphyConfig(client_id="--client-id--", client_secret="--client-secret--", tenant_id="--tenant-id--")
    assert config.client_id == "--client-id--"
    assert config.client_secret == "--client-secret--"
    assert config.tenant_id == "--tenant-id--"

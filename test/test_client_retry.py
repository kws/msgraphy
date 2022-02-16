from unittest.mock import MagicMock, Mock

import pytest
from requests import exceptions

from msgraphy.client.graph_client import timeout_retry


def test_client_retry_decorator():

    mock_func = Mock(side_effect=exceptions.ReadTimeout())

    @timeout_retry(0)
    def test_function():
        mock_func()

    with pytest.raises(exceptions.ReadTimeout):
        test_function()

    assert mock_func.call_count == 1

    mock_func.reset_mock()

    @timeout_retry(1)
    def test_function():
        mock_func()

    with pytest.raises(exceptions.ReadTimeout):
        test_function()

    assert mock_func.call_count == 2

    mock_func.reset_mock()

    @timeout_retry(5)
    def test_function():
        mock_func()

    with pytest.raises(exceptions.ReadTimeout):
        test_function()

    assert mock_func.call_count == 6

    mock_func.reset_mock()
    mock_func.side_effect = None

    test_function()

    assert mock_func.call_count == 1


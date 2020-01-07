import socket
import unittest
from unittest import mock

from proxy_passer import ProxyPasser


@unittest.mock.patch("proxy_passer.select")
def test_proxy_passer(mock_select):
    """
    Test if proxy passer actually passes target messages to source
    and source message to target
    :param mock_select: mocked select function
    """
    mock_select.side_effect = (
        lambda x, y, z, _: (x, y, z)
    )
    with mock.patch('socket.socket') as source:
        source_instance = source(socket.AF_INET, socket.SOCK_STREAM)
        source.return_value.recv.side_effect = [b'source', b'request']
        source.return_value.connect.return_value = None
        source.return_value.setblocking.return_value = None
        source.return_value.send.side_effect = (
            lambda x: len(x)
        )
        source.return_value.fileno.return_value = 0
        with mock.patch('socket.socket') as target:
            target_instance = target(socket.AF_INET, socket.SOCK_STREAM)
            target.return_value.recv.side_effect = [b'target', b'response']
            target.return_value.connect.return_value = None
            target.return_value.setblocking.return_value = None
            target.return_value.send.side_effect = (
                lambda x: len(x)
            )
            target.return_value.fileno.return_value = 0

            passer = ProxyPasser(source_instance, target_instance)
            passer.run()

            source_instance.send.assert_called_with(b'targetresponse')
            target_instance.send.assert_called_with(b'sourcerequest')

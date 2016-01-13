import unittest
from pyvista.rpc import VistaToken, TokenParams


class TestToken(unittest.TestCase):

    def test_encrypt_decrypt(self):
        raw = '900:123456789:DEPARTMENT OF DEFENSE,USER:33'
        token = VistaToken.encrypt(raw)
        self.assertEqual(88, len(token))

        expected = TokenParams(
            site_id='900',
            fed_id='123456789',
            username='DEPARTMENT OF DEFENSE,USER',
            duz='33'
        )
        params = VistaToken.decrypt(token)
        self.assertEqual(expected, params)

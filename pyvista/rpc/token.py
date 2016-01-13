import base64
from collections import namedtuple
from Crypto.Cipher import AES
from Crypto import Random

BS = 16
secret_key = 'MortimerSnerdKey'.encode()

TokenParams = namedtuple('TokenParams', ['site_id', 'fed_id', 'username', 'duz'])


class VistaToken(object):

    @staticmethod
    def _pad(s):
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    @staticmethod
    def encrypt(raw):
        raw = VistaToken._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    @staticmethod
    def decrypt(enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        raw = VistaToken._unpad(cipher.decrypt(enc[16:])).decode('utf8')
        parts = raw.split(':')
        return TokenParams(
            site_id=parts[0],
            fed_id=parts[1],
            username=parts[2],
            duz=parts[3]
        )

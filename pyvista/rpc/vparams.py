from collections import namedtuple
from simplecrypt import encrypt, decrypt

VParams = namedtuple('VParams', ['site_id', 'fed_id', 'username', 'duz'])

secret_key = ''


def encrypt_token(vparams):
    param_str = ':'.join(vparams)
    return encrypt(secret_key, param_str)


def decrypt_token(token):
    param_str = decrypt(secret_key, token).decode('utf8')
    parts = param_str.split(':')
    return VParams(
        site_id=parts[0],
        fed_id=parts[1],
        username=parts[2],
        duz=parts[3]
    )

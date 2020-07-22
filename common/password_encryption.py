""" this file is used to perform data encryption and decryption operations."""

import yaml
from simplecrypt import encrypt, decrypt
from base64 import b64encode, b64decode


salt = ""
with open("mgnrega/config.yaml", 'r') as ymlfile:
    """
    getting salt from yaml config file.
    """
    cfg = yaml.load(ymlfile)
    salt = cfg['enc']['salt']


def encrypt_pass(password):
    """
    this method is used to encrypt data.
    :param password: string, password.
    :return: string, encrypted password.
    """
    cipher = encrypt(salt, password)
    return b64encode(cipher)


def decrypt_pass(encoded_cipher):
    """
    this method is used to decrypt data.
    :param encoded_cipher: encoded data.
    :return: decrypted password.
    """
    cipher = b64decode(encoded_cipher)
    return decrypt(salt, cipher)




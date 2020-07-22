import unittest
import mock
from common.password_encryption import encrypt_pass, decrypt_pass


class PasswordEncrpytion(unittest.TestCase):

    @mock.patch('common.password_encryption.encrypt')
    @mock.patch('common.password_encryption.b64encode')
    def test_encrypt_pass(self, mock_encode, mock_encrypt):
        password = 'sample_password'
        encrypt_pass(password)
        mock_encrypt.assert_called_once_with(mock.ANY, password)
        mock_encode.assert_called_once()

    @mock.patch('common.password_encryption.decrypt')
    @mock.patch('common.password_encryption.b64decode')
    def test_decrypt_pass(self, mock_decode, mock_decrypt):
        encoded_cipher = 'sample_password'
        mock_decrypt.return_value = 'encrypted value'
        decrypt_pass(encoded_cipher)
        mock_decode.assert_called_once_with(encoded_cipher)
        mock_decrypt.assert_called_once()


if __name__ == '__main__':
    unittest.main()

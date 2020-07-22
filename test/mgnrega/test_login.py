import unittest
import mock
from mgnrega.login import main

class LoginTest(unittest.TestCase):

    @mock.patch('mgnrega.login.BDO')
    @mock.patch('mgnrega.login.decrypt_pass', return_value=b'pass')
    @mock.patch('mgnrega.login.ConnectDb')
    @mock.patch('mgnrega.login.input', return_value='sample')
    @mock.patch('mgnrega.login.getpass', return_value='pass')
    @mock.patch('mgnrega.login.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.login.os')
    def test_main_bdo(self, mock_os, mock_print, mock_menu, mock_pass, mock_input, mock_db, mock_decrypt, mock_bdo):
        # we will use mock.Mock() when we want to mock a object and its functions and pass it as argument to
        # actual function which we want to test
        # mock_db = mock.Mock()
        # mock_db.validate_number.side_effect = (False, True, True)
        # main (mock_db)

        mock_db().get_user_with_role.return_value = ['1', 'pass']
        mock_menu().draw_menu.return_value = 'BDO'
        main()
        mock_decrypt.assert_called_once()
        mock_print.assert_called_once()
        mock_bdo.assert_called_once()
        mock_db().close_conn.assert_called_once()
        mock_bdo().bdo_features.assert_called_once()
        mock_pass.assert_called_once()
        self.assertEqual(mock_bdo().bdo_id, '1')
        self.assertEqual(mock_os.system.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.login.GPM')
    @mock.patch('mgnrega.login.decrypt_pass', return_value=b'pass')
    @mock.patch('mgnrega.login.ConnectDb')
    @mock.patch('mgnrega.login.input', return_value='sample')
    @mock.patch('mgnrega.login.getpass', return_value='pass')
    @mock.patch('mgnrega.login.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.login.os')
    def test_main_gpm(self, mock_os, mock_print, mock_menu, mock_pass, mock_input, mock_db,
                      mock_decrypt, mock_gpm):
        mock_db().get_user_with_role.return_value = ['2', 'pass']
        mock_menu().draw_menu.return_value = 'GPM'
        main()
        mock_print.assert_called_once()
        mock_gpm.assert_called_once()
        mock_decrypt.assert_called_once()
        mock_pass.assert_called_once()
        mock_db().close_conn.assert_called_once()
        mock_gpm().gpm_features.assert_called_once()
        self.assertEqual(mock_gpm().gpm_id, '2')
        self.assertEqual(mock_os.system.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.login.Member')
    @mock.patch('mgnrega.login.decrypt_pass', return_value=b'pass')
    @mock.patch('mgnrega.login.ConnectDb')
    @mock.patch('mgnrega.login.input', return_value='sample')
    @mock.patch('mgnrega.login.getpass', return_value='pass')
    @mock.patch('mgnrega.login.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.login.os')
    def test_main_member(self, mock_os, mock_print, mock_menu, mock_pass, mock_input, mock_db, mock_decrypt,
                         mock_member):
        mock_db().get_user_with_role.return_value = ['3', 'pass']
        mock_menu().draw_menu.return_value = 'Member'
        main()
        mock_print.assert_called_once()
        mock_member.assert_called_once()
        mock_db().close_conn.assert_called_once()
        mock_pass.assert_called_once()
        mock_decrypt.assert_called_once()
        mock_member().member_features.assert_called_once()
        self.assertEqual(mock_member().member_id, '3')
        self.assertEqual(mock_os.system.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.login.getpass', return_value='different_pass')
    @mock.patch('mgnrega.login.decrypt_pass', return_value=b'pass')
    @mock.patch('mgnrega.login.ConnectDb')
    @mock.patch('mgnrega.login.input', return_value='sample')
    @mock.patch('mgnrega.login.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.login.os')
    def test_main_invalid_credentials(self, mock_os, mock_print, mock_menu, mock_input, mock_db, mock_decrypt,
                                      mock_pass):

        mock_os.system.side_effect = ['', '', SystemExit]
        mock_db().get_user_with_role.return_value = ['3', 'pass']
        mock_menu().draw_menu.return_value = 'Member'
        self.assertRaises(SystemExit, main)
        self.assertEqual(mock_os.system.call_count, 3)
        mock_decrypt.assert_called_once()
        mock_pass.assert_called_once()
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(mock_db().close_conn.call_count, 2)

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.login.sys')
    @mock.patch('mgnrega.login.ConnectDb')
    @mock.patch('mgnrega.login.os')
    def test_main_exception(self, mock_os, mock_db, mock_sys, mock_print):
        mock_os.system.side_effect = Exception
        main()

        mock_sys.exit.assert_called_once()
        mock_print.assert_called_once()
        mock_db().close_conn.assert_called_once()


if __name__ == '__main__':
    unittest.main()

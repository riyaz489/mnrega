import unittest
import mock
from mgnrega.member import Member
import sqlite3
from common.connect_db import ConnectDb


class MemberTest(unittest.TestCase):

    @mock.patch('mgnrega.member.Member.view_details', return_value='')
    @mock.patch('mgnrega.member.getattr')
    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('mgnrega.member.os')
    @mock.patch('mgnrega.member.Menu')
    @mock.patch('builtins.print')
    def test_member_features(self, mock_print, mock_menu, mock_os, mock_input, mock_getattr, mock_view_details):
        member = Member()
        mock_getattr.side_effect = [member.view_details, SystemExit]
        self.assertRaises(SystemExit, member.member_features)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_getattr.call_count, 2)
        self.assertEqual(mock_input.call_count, 3)
        mock_os.system.assert_any_call('clear')
        mock_print.assert_any_call("choose feature :\n")

    @mock.patch('mgnrega.member.sys')
    @mock.patch('mgnrega.member.getattr', return_value='exception_function')
    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('mgnrega.member.Menu')
    @mock.patch('builtins.print')
    def test_member_features_exception(self, mock_print, mock_menu, mock_input, mock_getattr, mock_sys):
        member = Member()
        member.member_features()
        mock_sys.exit.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.member.ConnectDb')
    @mock.patch('mgnrega.member.decrypt_pass')
    def test_view_details(self, mock_decrypt, mock_db, mock_print, mock_input):
        mock_db().get_member_details.return_value = ['dummy', 'dummy2', 'dummy2', 'dummy2', 'dummy2', 'dummy2',
                                                     'dummy2', 'dummy2', 'dummy2', 'dummy2', 'dummy2']
        mock_db().get_member_project.return_value = ['2020-01-01', 'dummy2', 'dummy2']
        mock_decrypt.return_value = 'dummy'
        member = Member()
        member.view_details()
        self.assertEqual(mock_print.call_count, 17)
        mock_db().get_member_details.assert_called_once()
        mock_db().get_member_project.assert_called_once()
        mock_decrypt.assert_called_once()

    @mock.patch('mgnrega.member.decrypt_pass')
    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.member.ConnectDb')
    def test_view_details_project_not_exits(self, mock_db, mock_print, mock_input, mock_decrypt):

        mock_db().get_member_project.return_value = None
        mock_db().get_member_details.return_value = ['dummy', 'dummy2', 'dummy2', 'dummy2', 'dummy2', 'dummy2',
                                                     'dummy2', 'dummy2', 'dummy2', 'dummy2', 'dummy2']
        mock_decrypt.return_value = 'dummy'

        member = Member()
        member.view_details()
        self.assertEqual(mock_print.call_count, 13)
        mock_db().get_member_details.assert_called_once()
        mock_db().get_member_project.assert_called_once()
        mock_decrypt.assert_called_once()

    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.member.ConnectDb')
    def test_view_details_member_not_exits(self, mock_db, mock_print, mock_input):
        mock_db().get_member_details.return_value = None
        member = Member()
        self.assertRaises(SystemExit, member.view_details)
        mock_print.assert_called_once()
        mock_db().get_member_details.assert_called_once()

    @mock.patch('mgnrega.member.Menu')
    @mock.patch('mgnrega.member.ConnectDb')
    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('builtins.print')
    def test_file_complain(self, mock_print, mock_input, mock_db, mock_menu):
        # arrange
        mock_db().get_bdo_gpm_for_member.return_value = ['dummy', 'dummy', 'dummy']
        mock_menu().draw_menu.return_value = 'BDO'
        # act
        member = Member()
        member.file_complain()
        # assert
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)
        mock_db().get_bdo_gpm_for_member.assert_called_once()
        mock_db().register_complain.assert_called_once()
        mock_db().commit_data.assert_called_once()

    @mock.patch('mgnrega.member.Menu')
    @mock.patch('mgnrega.member.ConnectDb')
    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('builtins.print')
    def test_file_complain_empty_member_details(self, mock_print, mock_input, mock_db, mock_menu):
        # arrange
        mock_db().get_bdo_gpm_for_member.return_value = None
        mock_menu().draw_menu.return_value = 'BDO'
        # act
        member = Member()
        member.file_complain()
        # assert
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(mock_input.call_count, 1)
        mock_db().get_bdo_gpm_for_member.assert_called_once()


    @mock.patch('mgnrega.member.Menu')
    @mock.patch('mgnrega.member.ConnectDb')
    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('builtins.print')
    def test_file_complain_exception(self, mock_print, mock_input, mock_db, mock_menu):
        # arrange
        mock_db().get_bdo_gpm_for_member.return_value = ['dummy', 'dummy', 'dummy']
        mock_menu().draw_menu.return_value = 'GPM'
        mock_db().commit_data.side_effect = sqlite3.Error
        # act
        member = Member()
        member.file_complain()
        # assert
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)
        mock_db().get_bdo_gpm_for_member.assert_called_once()
        mock_db().register_complain.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.member.Menu')
    @mock.patch('mgnrega.member.ConnectDb')
    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('builtins.print')
    def test_file_complain_invalid_option(self, mock_print, mock_input, mock_db, mock_menu):
        # arrange
        mock_db().get_bdo_gpm_for_member.return_value = ['dummy', 'dummy', 'dummy']
        mock_menu().draw_menu.return_value = 'dummy'
        # act
        member = Member()
        member.file_complain()
        # assert
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(mock_input.call_count, 1)
        mock_db().get_bdo_gpm_for_member.assert_called_once()

    @mock.patch('mgnrega.member.Menu')
    @mock.patch('mgnrega.member.ConnectDb')
    @mock.patch('mgnrega.member.input', return_value='')
    @mock.patch('builtins.print')
    def test_file_complain_back_button(self, mock_print, mock_input, mock_db, mock_menu):
        # arrange
        mock_menu().draw_menu.return_value = 'BACK'
        # act
        member = Member()
        member.file_complain()
        # assert
        self.assertEqual(mock_print.call_count, 1)
        self.assertEqual(mock_input.call_count, 1)


if __name__ == '__main__':
    unittest.main()

import unittest
import mock
from mgnrega.bdo import BDO


class BdoTest(unittest.TestCase):
    @mock.patch('mgnrega.bdo.BDO.show_gpm', return_value='')
    @mock.patch('mgnrega.bdo.getattr')
    @mock.patch('mgnrega.bdo.input', return_value='')
    @mock.patch('mgnrega.bdo.os')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_bdo_features(self, mock_print, mock_menu, mock_os, mock_input, mock_getattr, show_gpm):
        bdo = BDO()
        mock_getattr.side_effect = [show_gpm, SystemExit]
        self.assertRaises(SystemExit, bdo.bdo_features)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_getattr.call_count, 2)
        self.assertEqual(mock_input.call_count, 3)
        mock_os.system.assert_any_call('clear')
        mock_print.assert_any_call("choose feature :\n")

    @mock.patch('mgnrega.bdo.sys')
    @mock.patch('mgnrega.bdo.getattr', return_value='exception_function')
    @mock.patch('mgnrega.bdo.input', return_value='')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_bdo_features_exception(self, mock_print, mock_menu, mock_input, mock_getattr, mock_sys):
        bdo = BDO()
        bdo.bdo_features()
        mock_sys.exit.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.raw_data_to_table')
    @mock.patch('mgnrega.bdo.decrypt_pass')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_show_gpm(self, mock_db, mock_decrypt, mock_raw_to_table, mock_print):
        mock_db().get_subordinate_details.return_value.fetchall.return_value = [['dummy1', 'dummy2', 'dummy3']]
        bdo = BDO()
        bdo.show_gpm()
        mock_print.assert_called_once_with("GPM's list:\n")
        mock_db().get_subordinate_details.assert_called_once()
        mock_db().get_subordinate_details().fetchall.assert_called_once()
        mock_decrypt.assert_called_once()
        mock_raw_to_table.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.raw_data_to_table')
    @mock.patch('mgnrega.bdo.decrypt_pass')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_show_gpm_no_gpm(self, mock_db, mock_decrypt, mock_raw_to_table, mock_print):
        mock_db().get_subordinate_details.return_value.fetchall.return_value = []
        bdo = BDO()
        bdo.show_gpm()
        self.assertEqual(mock_print.call_count, 2)
        mock_db().get_subordinate_details.assert_called_once()
        mock_db().get_subordinate_details().fetchall.assert_called_once()

    @mock.patch('mgnrega.bdo.GPM')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_show_members(self, mock_db, mock_print, mock_gpm):
        mock_db().get_user_names.return_value = [['dummy', 'dummy']]
        bdo = BDO()
        bdo.show_members()
        mock_db().get_user_names.assert_called_once()
        mock_gpm().show_members.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('mgnrega.bdo.GPM')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_show_members_no_gpm(self, mock_db, mock_print, mock_gpm):
        mock_db().get_user_names.return_value = []
        bdo = BDO()
        bdo.show_members()
        mock_db().get_user_names.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('mgnrega.bdo.encrypt_pass')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_create_gpm(self, mock_db, mock_print, mock_input, mock_encrypt):
        mock_input.side_effect = ['name', 'pass@Pas123', 'username', 'state', 'district', '232323', '21', 'M']
        bdo = BDO()
        bdo.create_gpm()
        mock_db().add_user.assert_called_once()
        mock_db().add_personal_details.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_encrypt.assert_called_once()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 8)

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    def test_create_gpm_invalid_password(self, mock_print, mock_input):
        mock_input.side_effect = ['name', 'pass@', '']
        bdo = BDO()
        bdo.create_gpm()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 3)

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    def test_create_gpm_invalid_pincode(self, mock_print, mock_input):
        mock_input.side_effect = ['name', 'pass@Pas123', 'username', 'state', 'district', '23s2323', '']
        bdo = BDO()
        bdo.create_gpm()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 7)

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    def test_create_gpm_invalid_age(self, mock_print, mock_input):
        mock_input.side_effect = ['name', 'pass@Pas123', 'username', 'state', 'district', '232323', 'invalid-age', '']
        bdo = BDO()
        bdo.create_gpm()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 8)

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    def test_create_gpm_invalid_gender(self, mock_print, mock_input):
        mock_input.side_effect = ['name', 'pass@Pas123', 'username', 'state', 'district', '232323', '21', 'male', '']
        bdo = BDO()
        bdo.create_gpm()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 9)

    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.input', side_effect=Exception)
    @mock.patch('builtins.print')
    def test_create_gpm_exception(self, mock_print, mock_input, mock_db):
        bdo = BDO()
        bdo.create_gpm()
        mock_input.assert_called_once()
        mock_print.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.BDO.delete_project_members')
    @mock.patch('mgnrega.bdo.os')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    def test_delete_gpm(self, mock_gpm_list, mock_menu, mock_print, mock_db, mock_os, mock_delete_member, mock_input):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'name2']
        mock_db().get_gpm_projects.return_value = ['dummy']
        mock_db().get_project_members.return_value = [['dummy']]
        bdo = BDO()
        bdo.delete_gpm()
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_os.system.assert_called_once()
        mock_delete_member.assert_called_once()
        mock_db().get_project_members.assert_called_once()
        mock_db().get_gpm_projects.assert_called_once()
        mock_gpm_list.assert_called_once()
        mock_db().update_member_gpm.assert_called_once()
        mock_db().update_user.assert_called_once()
        mock_db().commit_data.assert_called_once()

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.os')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    def test_delete_gpm_no_alternative(self, mock_gpm_list, mock_menu, mock_print, mock_os, mock_input):
        mock_gpm_list.return_value = {'name1': 'id1'}
        mock_menu().draw_menu.side_effect = ['name1']
        bdo = BDO()
        bdo.delete_gpm()
        self.assertEqual(mock_print.call_count, 3)
        mock_os.system.assert_called_once()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_gpm_list.assert_called_once()

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    def test_delete_gpm_menu1_back(self, mock_gpm_list, mock_menu, mock_print, mock_input):
        mock_gpm_list.return_value = {'name1': 'id1'}
        mock_menu().draw_menu.side_effect = ['BACK']
        bdo = BDO()
        bdo.delete_gpm()
        mock_input.assert_called_once()
        mock_print.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_gpm_list.assert_called_once()

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.os')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    def test_delete_gpm_menu2_back(self, mock_gpm_list, mock_menu, mock_print, mock_os, mock_input):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'BACK']
        bdo = BDO()
        bdo.delete_gpm()
        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        mock_os.system.assert_called_once_with('clear')
        mock_gpm_list.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    def test_delete_gpm_exception(self, mock_gpm_list, mock_db, mock_print):
        mock_gpm_list.side_effect = Exception
        bdo = BDO()
        bdo.delete_gpm()
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.bdo.encrypt_pass')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_update_gpm_user_details(self, mock_db, mock_input, mock_gpm_list, mock_print, mock_menu, mock_encrypt):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'PASSWORD']
        mock_encrypt.return_value = 'Pass@123'
        mock_input.side_effect = ['', '', 'Pass@123']
        bdo = BDO()
        bdo.update_gpm()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 3)
        mock_db().update_user.assert_called_once_with('PASSWORD', mock.ANY, 'Pass@123')
        mock_db().commit_data.assert_called_once()

    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_update_gpm_personal_detail(self, mock_db, mock_input, mock_gpm_list, mock_validation, mock_print,
                                        mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'AGE']
        mock_validation.age.return_value = True
        mock_input.side_effect = ['', '', 'dummy_data']
        bdo = BDO()
        bdo.update_gpm()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        mock_validation.age.assert_called_once()
        self.assertEqual(mock_input.call_count, 3)
        mock_db().update_personal_details.assert_called_once_with('AGE', mock.ANY, 'dummy_data')
        mock_db().commit_data.assert_called_once()

    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.input')
    def test_update_gpm_invalid_age(self, mock_input, mock_gpm_list, mock_validation, mock_print, mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'AGE']
        mock_validation.age.return_value = False
        mock_input.side_effect = ['', '', 'dummy_data', '']
        bdo = BDO()
        bdo.update_gpm()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 4)
        mock_validation.age.assert_called_once_with('dummy_data')

    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.input')
    def test_update_gpm_invalid_pincode(self, mock_input, mock_gpm_list, mock_validation, mock_print, mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'PINCODE']
        mock_validation.pincode.return_value = False
        mock_input.side_effect = ['', '', 'dummy_data', '']
        bdo = BDO()
        bdo.update_gpm()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 4)
        mock_validation.pincode.assert_called_once_with('dummy_data')

    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.input')
    def test_update_gpm_invalid_password(self, mock_input, mock_gpm_list, mock_validation, mock_print, mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'PASSWORD']
        mock_validation.password.return_value = False
        mock_input.side_effect = ['', '', 'dummy_data', '']
        bdo = BDO()
        bdo.update_gpm()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 4)
        mock_validation.password.assert_called_once_with('dummy_data')

    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.input')
    def test_update_gpm_invalid_gender(self, mock_input, mock_gpm_list, mock_validation, mock_print, mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'GENDER']
        mock_validation.gender.return_value = False
        mock_input.side_effect = ['', '', 'dummy_data', '']
        bdo = BDO()
        bdo.update_gpm()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 4)
        mock_validation.gender.assert_called_once_with('dummy_data')

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    def test_update_gpm_exception(self, mock_gpm_list, mock_db, mock_print):
        mock_gpm_list.side_effect = Exception
        bdo = BDO()
        bdo.update_gpm()
        mock_print.assert_called_once()
        mock_gpm_list.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    def test_update_gpm_back(self, mock_gpm_list, mock_menu, mock_input):
        mock_gpm_list.return_value = {'name1': 'id1'}
        mock_menu().draw_menu.side_effect = ['BACK']
        bdo = BDO()
        bdo.update_gpm()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_gpm_list.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_get_gpm_list(self, mock_db, mock_print):
        mock_db().get_user_names.return_value = [['name', 'id']]
        sample_dict = {'name': 'id'}
        bdo = BDO()
        result = bdo.get_gpm_list()
        mock_db().get_user_names.assert_called_once()
        self.assertEqual(result, sample_dict)

    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_create_project(self, mock_db, mock_print, mock_menu, mock_input, mock_validation, mock_gpm_list):
        mock_input.return_value = ''
        mock_menu().draw_menu.return_value = ''
        mock_validation.is_int.return_value = True
        mock_validation.start_date.return_value = True
        mock_validation.end_date.return_value = True
        mock_menu().draw_menu.side_effect = ['name', 'project_type']
        mock_gpm_list.return_value = {'name': 'id'}

        bdo = BDO()
        bdo.create_project()
        mock_db().create_project.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_validation.start_date.assert_called_once()
        mock_validation.end_date.assert_called_once()
        self.assertEqual(mock_validation.is_int.call_count, 3)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_input.call_count, 8)

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    def test_create_project_exception(self, mock_gpm_list, mock_db, mock_print):
        mock_gpm_list.side_effect = Exception
        bdo = BDO()
        bdo.create_project()
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_create_project_invalid_labour_number(self, mock_print, mock_menu, mock_input, mock_validation, mock_gpm_list):
        mock_input.return_value = ''
        mock_menu().draw_menu.return_value = ''
        mock_validation.is_int.return_value = False
        mock_menu().draw_menu.side_effect = ['name', 'project_type']
        mock_gpm_list.return_value = {'name': 'id'}

        bdo = BDO()
        bdo.create_project()
        self.assertEqual(mock_validation.is_int.call_count, 1)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_input.call_count, 5)

    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_create_project_invalid_cost_number(self, mock_print, mock_menu, mock_input, mock_validation, mock_gpm_list):
        mock_input.return_value = ''
        mock_menu().draw_menu.return_value = ''
        mock_validation.is_int.side_effect = [True, False]
        mock_menu().draw_menu.side_effect = ['name', 'project_type']
        mock_gpm_list.return_value = {'name': 'id'}

        bdo = BDO()
        bdo.create_project()
        self.assertEqual(mock_validation.is_int.call_count, 2)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_input.call_count, 6)

    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_create_project_invalid_area_number(self, mock_print, mock_menu, mock_input, mock_validation,
                                                mock_gpm_list):
        mock_input.return_value = ''
        mock_menu().draw_menu.return_value = ''
        mock_validation.is_int.side_effect = [True, True, False]
        mock_menu().draw_menu.side_effect = ['name', 'project_type']
        mock_gpm_list.return_value = {'name': 'id'}

        bdo = BDO()
        bdo.create_project()
        self.assertEqual(mock_validation.is_int.call_count, 3)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_input.call_count, 7)

    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_create_project_invalid_start_date(self, mock_print, mock_menu, mock_input, mock_validation, mock_gpm_list):
        mock_input.return_value = ''
        mock_menu().draw_menu.return_value = ''
        mock_validation.is_int.return_value = True
        mock_validation.start_date.return_value = False
        mock_menu().draw_menu.side_effect = ['name', 'project_type']
        mock_gpm_list.return_value = {'name': 'id'}

        bdo = BDO()
        bdo.create_project()
        self.assertEqual(mock_validation.is_int.call_count, 3)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_input.call_count, 8)
        mock_validation.start_date.assert_called_once()

    @mock.patch('mgnrega.bdo.BDO.get_gpm_list')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_create_project_invalid_end_date(self, mock_print, mock_menu, mock_input, mock_validation, mock_gpm_list):
        mock_input.return_value = ''
        mock_menu().draw_menu.return_value = ''
        mock_validation.is_int.return_value = True
        mock_validation.start_date.return_value = True
        mock_validation.end_date.return_value = False
        mock_menu().draw_menu.side_effect = ['name', 'project_type']
        mock_gpm_list.return_value = {'name': 'id'}

        bdo = BDO()
        bdo.create_project()
        self.assertEqual(mock_validation.is_int.call_count, 3)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_input.call_count, 9)
        mock_validation.start_date.assert_called_once()
        mock_validation.end_date.assert_called_once()

    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_update_project_type(self, mock_print, mock_menu, mock_input, mock_db, mock_project_list):
        mock_input.return_value = ''
        mock_project_list.return_value = {'name': 'id'}
        mock_menu().draw_menu.side_effect = ['name', 'PROJECT_TYPE', 'road_project']
        bdo = BDO()
        bdo.update_project()

        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(mock_print.call_count, 4)
        self.assertEqual(mock_menu().draw_menu.call_count, 3)
        mock_db().update_project.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_project_list.assert_called_once()

    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_update_project_invalid_area(self, mock_print, mock_menu, mock_input, mock_project_list, mock_validation):
        mock_input.return_value = ''
        mock_project_list.return_value = {'name': 'id'}
        mock_menu().draw_menu.side_effect = ['name', 'AREA_OF_PROJECT']
        mock_validation.is_int.return_value = False
        bdo = BDO()
        bdo.update_project()

        self.assertEqual(mock_input.call_count, 4)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        mock_project_list.assert_called_once()
        mock_validation.is_int.assert_called_once()

    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_update_project_invalid_labour_numbers(self, mock_print, mock_menu, mock_input, mock_project_list
                                                   , mock_validation):
        mock_input.return_value = ''
        mock_project_list.return_value = {'name': 'id'}
        mock_menu().draw_menu.side_effect = ['name', 'TOTAL_LABOUR_REQUIRED']
        mock_validation.is_int.return_value = False
        bdo = BDO()
        bdo.update_project()

        self.assertEqual(mock_input.call_count, 4)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        mock_project_list.assert_called_once()
        mock_validation.is_int.assert_called_once()

    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_update_project_invalid_cost(self, mock_print, mock_menu, mock_input, mock_project_list
                                                   , mock_validation):
        mock_input.return_value = ''
        mock_project_list.return_value = {'name': 'id'}
        mock_menu().draw_menu.side_effect = ['name', 'ESTIMATED_COST']
        mock_validation.is_int.return_value = False
        bdo = BDO()
        bdo.update_project()

        self.assertEqual(mock_input.call_count, 4)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        mock_project_list.assert_called_once()
        mock_validation.is_int.assert_called_once()

    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_update_project_invalid_start_date(self, mock_print, mock_menu, mock_input, mock_project_list
                                               , mock_validation):
        mock_input.return_value = ''
        mock_project_list.return_value = {'name': 'id'}
        mock_menu().draw_menu.side_effect = ['name', 'ESTIMATED_START_DATE']
        mock_validation.start_date.return_value = False
        bdo = BDO()
        bdo.update_project()

        self.assertEqual(mock_input.call_count, 4)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        mock_project_list.assert_called_once()
        mock_validation.start_date.assert_called_once()

    @mock.patch('mgnrega.bdo.ConnectDb.get_project_start_date')
    @mock.patch('mgnrega.bdo.Validation')
    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('builtins.print')
    def test_update_project_invalid_end_date(self, mock_print, mock_menu, mock_input, mock_project_list,
                                             mock_validation, mock_db):
        mock_input.return_value = ''
        mock_project_list.return_value = {'name': 'id'}
        mock_menu().draw_menu.side_effect = ['name', 'ESTIMATED_END_DATE']
        mock_validation.end_date.return_value = False
        bdo = BDO()
        bdo.update_project()

        self.assertEqual(mock_input.call_count, 4)
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        mock_project_list.assert_called_once()
        mock_validation.end_date.assert_called_once()

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    def test_update_project_back(self, mock_project_list, mock_menu, mock_input):
        mock_project_list.return_value = {'name1': 'id1'}
        mock_menu().draw_menu.side_effect = ['BACK']
        bdo = BDO()
        bdo.update_project()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_project_list.assert_called_once()

    @mock.patch('mgnrega.bdo.BDO.project_deletion')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    @mock.patch('builtins.print')
    def test_delete_project(self, mock_print, mock_project_list, mock_menu, mock_input, mock_project_deletion):
        mock_project_list.return_value = {'name': 'id'}
        mock_menu().draw_menu.return_value = 'name'
        mock_input.return_value = ''
        bdo = BDO()
        bdo.delete_project()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_project_list.assert_called_once()
        mock_project_deletion.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('mgnrega.bdo.input')
    @mock.patch('mgnrega.bdo.Menu')
    @mock.patch('mgnrega.bdo.BDO.get_project_list')
    def test_delete_project_back(self, mock_project_list, mock_menu, mock_input):
        mock_project_list.return_value = {'name1': 'id1'}
        mock_menu().draw_menu.side_effect = ['BACK']
        bdo = BDO()
        bdo.delete_project()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_project_list.assert_called_once()

    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.raw_data_to_table')
    def test_show_projects(self, mock_table, mock_db):
        bdo = BDO()
        bdo.show_projects()
        mock_db().get_bdo_project_details.assert_called_once()
        mock_db().get_bdo_project_details().fetchall.assert_called_once()
        mock_table.assert_called_once()

    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_get_project_list(self, mock_db):
        mock_db().get_bdo_project_names.return_value = [['name', 'id']]
        sample_dict = {'name': 'id'}
        bdo = BDO()
        result = bdo.get_project_list()
        mock_db().get_bdo_project_names.assert_called_once()
        self.assertEqual(result, sample_dict)

    @mock.patch('mgnrega.bdo.BDO.delete_project_members')
    @mock.patch('mgnrega.bdo.PrettyTable')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.Menu')
    def test_show_request_approved_wage(self, mock_menu, mock_db, mock_print, mock_input, mock_table,
                                        mock_delete_members):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [['APPROVAL', 'dummy', 'WAGE|sample_member|ea32d0e'
                                                                                           '8-298a-4967-9fbd-72dc595294'
                                                                                           'fb|334aabf5-8663-492d-bf75'
                                                                                           '-6a5d7ece032d|project1',
                                                                      'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'APPROVED'
        mock_input.side_effect = ['0', '']
        bdo = BDO()
        bdo.show_requests()
        mock_menu().draw_menu.assert_called_once()
        mock_delete_members.assert_called_once()
        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().resolve_request.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.bdo.PrettyTable')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.Menu')
    def test_show_request_approved_member(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [
            ['APPROVAL', 'dummy', 'MEMBER|sample_member|ea32d0e8-'
                                  '298a-4967-9fbd-72dc595294fb|334aabf5-'
                                  '8663-492d-bf75-6a5d7ece032d|project1',
             'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'APPROVED'
        mock_input.side_effect = ['0', '']
        mock_db().get_project_members_required.return_value = [2]
        mock_db().get_project_members.return_value = ['id1']

        bdo = BDO()
        bdo.show_requests()

        mock_menu().draw_menu.assert_called_once()
        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().resolve_request.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().assign_project_members.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.bdo.PrettyTable')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.Menu')
    def test_show_request_approved_member_exceeded(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [
            ['APPROVAL', 'dummy', 'MEMBER|sample_member|ea32d0e8-'
                                  '298a-4967-9fbd-72dc595294fb|334aabf5-'
                                  '8663-492d-bf75-6a5d7ece032d|project1',
             'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'APPROVED'
        mock_input.side_effect = ['0', '']
        mock_db().get_project_members_required.return_value = [2]
        mock_db().get_project_members.return_value = ['id1', 'id2']

        bdo = BDO()
        bdo.show_requests()

        mock_menu().draw_menu.assert_called_once()
        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.bdo.PrettyTable')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.Menu')
    def test_show_request_rejected_approval(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [
            ['APPROVAL', 'dummy', 'MEMBER|sample_member|ea32d0e8-'
                                  '298a-4967-9fbd-72dc595294fb|334aabf5-'
                                  '8663-492d-bf75-6a5d7ece032d|project1',
             'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'REJECTED'
        mock_input.side_effect = ['0', '']

        bdo = BDO()
        bdo.show_requests()

        mock_menu().draw_menu.assert_called_once()
        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().resolve_request.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.bdo.PrettyTable')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.Menu')
    def test_show_request_rejected_issue(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [
            ['ISSUES', 'dummy', 'MEMBER|sample_member|ea32d0e8-'
                                  '298a-4967-9fbd-72dc595294fb|334aabf5-'
                                  '8663-492d-bf75-6a5d7ece032d|project1',
             'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'REJECTED'
        mock_input.side_effect = ['0', '']

        bdo = BDO()
        bdo.show_requests()

        mock_menu().draw_menu.assert_called_once()
        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().resolve_request.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.bdo.PrettyTable')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.Menu')
    def test_show_request_approved_issue(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [
            ['ISSUES', 'dummy', 'MEMBER|sample_member|ea32d0e8-'
                                '298a-4967-9fbd-72dc595294fb|334aabf5-'
                                '8663-492d-bf75-6a5d7ece032d|project1',
             'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'APPROVED'
        mock_input.side_effect = ['0', '']

        bdo = BDO()
        bdo.show_requests()

        mock_menu().draw_menu.assert_called_once()
        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().resolve_request.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_show_request_no_request(self, mock_db, mock_print):
        mock_db().get_requests.return_value.fetchall.return_value = []
        mock_db().get_requests.return_value.description.return_value = ()
        bdo = BDO()
        bdo.show_requests()

        mock_db().get_requests.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 1)

    @mock.patch('mgnrega.bdo.PrettyTable')
    @mock.patch('mgnrega.bdo.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    @mock.patch('mgnrega.bdo.Menu')
    def test_show_request_invalid_index(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [
            ['ISSUES', 'dummy', 'MEMBER|sample_member|ea32d0e8-'
                                '298a-4967-9fbd-72dc595294fb|334aabf5-'
                                '8663-492d-bf75-6a5d7ece032d|project1',
             'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'APPROVED'
        mock_input.side_effect = ['invalid_row', '']

        bdo = BDO()
        bdo.show_requests()

        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_show_request_exception(self, mock_db, mock_print):
        mock_db().get_requests.side_effect = Exception
        bdo = BDO()
        bdo.show_requests()
        mock_print.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_delete_project_members_none(self, mock_db):
        mock_db().get_members_assigned_project.return_value = None
        bdo = BDO()
        bdo.delete_project_members()
        mock_db().get_members_assigned_project.assert_called_once()

    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_delete_project_members(self, mock_db):
        mock_db().get_members_assigned_project.return_value = ['dummy', 'dummy', '2020-02-23']
        mock_db().find_project_is_assigned.return_value = []
        bdo = BDO()
        bdo.delete_project_members()
        mock_db().get_members_assigned_project.assert_called_once()
        mock_db().register_project_completion.assert_called_once()
        mock_db().remove_project_member.assert_called_once()
        mock_db().find_project_is_assigned.assert_called_once()
        mock_db().update_project.assert_called_once()

    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_project_deletion(self, mock_db):
        mock_db().get_project_members_list.return_value = [['dummy', 'dummy', '2020-02-23']]
        mock_db().get_bdo_approvals_list.return_value = [['dummy_id', 'MEMBER|sample_member|ea32d0e8-298a-4967-'
                                                                      '9fbd-72dc595294fb|334aabf5-8663-492d-bf75-'
                                                                      '6a5d7ece032d|project1']]
        bdo = BDO()
        bdo.project_id = '334aabf5-8663-492d-bf75-6a5d7ece032d'
        bdo.project_deletion()
        mock_db().get_project_members_list.assert_called_once()
        mock_db().register_project_completion.assert_called_once()
        mock_db().remove_project_all_members.assert_called_once()
        mock_db().get_bdo_approvals_list.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().resolve_request.assert_called_once_with("'True'", mock.ANY)
        mock_db().update_project.assert_called_once_with('is_deleted', 'True', mock.ANY)

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.bdo.ConnectDb')
    def test_project_deletion_exception(self, mock_db, mock_print):
        mock_db().get_project_members_list.side_effect = Exception
        bdo = BDO()
        bdo.project_deletion()
        mock_print.assert_called_once()
        mock_db().get_project_members_list.assert_called_once()
        mock_db().rollback_data.assert_called_once()


if __name__ == '__main__':
    unittest.main()

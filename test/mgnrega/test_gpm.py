import sqlite3
import unittest
import mock
from mgnrega.gpm import GPM


class GpmTest(unittest.TestCase):
    @mock.patch('mgnrega.gpm.GPM.show_projects')
    @mock.patch('mgnrega.gpm.getattr')
    @mock.patch('mgnrega.gpm.input', return_value='')
    @mock.patch('mgnrega.gpm.os')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('builtins.print')
    def test_bdo_features(self, mock_print, mock_menu, mock_os, mock_input, mock_getattr, mock_show_projects):
        gpm = GPM()
        mock_getattr.side_effect = [mock_show_projects, SystemExit]
        self.assertRaises(SystemExit, gpm.gpm_features)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_getattr.call_count, 2)
        self.assertEqual(mock_input.call_count, 3)
        mock_os.system.assert_any_call('clear')
        mock_print.assert_any_call("choose feature :\n")

    @mock.patch('mgnrega.gpm.sys')
    @mock.patch('mgnrega.gpm.getattr', return_value='exception_function')
    @mock.patch('mgnrega.gpm.input', return_value='')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('builtins.print')
    def test_bdo_features_exception(self, mock_print, mock_menu, mock_input, mock_getattr, mock_sys):
        gpm = GPM()
        gpm.gpm_features()
        mock_sys.exit.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('mgnrega.gpm.raw_data_to_table')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_show_projects(self, mock_db, mock_table):
        gpm = GPM()
        gpm.gpm_id = 'sample'
        gpm.show_projects()
        mock_db().get_gpm_projects_details.assert_called_once_with('sample')
        mock_db().get_gpm_projects_details().fetchall.assert_called_once()
        mock_table.assert_called_once()

    @mock.patch('mgnrega.gpm.GPM.delete_project_request')
    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.input', return_value='')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_project_completion(self, mock_db, mock_print, mock_input, mock_menu, mock_project_list, mock_delete_request):
        mock_project_list.return_value = {'name': 'project_id'}
        mock_db().get_project_members.return_value = [['id1']]
        mock_menu().draw_menu.return_value = 'name'
        gpm = GPM()
        gpm.project_completion()

        mock_project_list.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_input.assert_called_once()
        mock_delete_request.assert_called_once()
        mock_db().get_project_members.assert_called_once()
        mock_db().commit_data.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.input', return_value='')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_project_completion_no_member(self, mock_db, mock_print, mock_input, mock_menu, mock_project_list):
        mock_project_list.return_value = {'name': 'project_id'}
        mock_db().get_project_members.return_value = []
        mock_menu().draw_menu.return_value = 'name'
        gpm = GPM()
        gpm.project_completion()

        mock_project_list.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_input.assert_called_once()
        mock_db().get_project_members.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.input', return_value='')
    @mock.patch('builtins.print')
    def test_project_completion_back(self, mock_print, mock_input, mock_menu, mock_project_list):
        mock_project_list.return_value = {'name': 'project_id'}
        mock_menu().draw_menu.return_value = 'BACK'
        gpm = GPM()
        gpm.project_completion()
        mock_project_list.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_print.assert_called_once()
        mock_input.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_project_completion_exception(self, mock_db, mock_project_list, mock_print):
        mock_project_list.side_effect = sqlite3.Error
        gpm = GPM()
        gpm.project_completion()
        self.assertEqual(mock_print.call_count, 2)
        mock_db().rollback_data.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.GPM.assign_project_members_request')
    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_assign_members_to_projects(self, mock_db, mock_input, mock_menu, mock_member_list, mock_project_list,
                                        mock_member_request, mock_print):
        mock_member_list.return_value = {'name': 'member_id', 'name2': 'member_id2'}
        mock_project_list.return_value = {'project_name': 'project_id'}
        mock_db().get_project_members.return_value = [['member_id']]
        mock_db().get_project_members_required.return_value = [2]
        mock_menu().draw_menu.side_effect = ['project_name', 'name2']

        gpm = GPM()
        gpm.assign_members_to_projects()

        mock_member_list.assert_called_once()
        mock_member_request.assert_called_once()
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_db().get_project_members_required.assert_called_once()
        mock_db().get_project_members.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.input')
    def test_assign_members_to_projects_back(self, mock_input, mock_menu, mock_project_list, mock_print):
        mock_project_list.return_value = {'project_name': 'project_id'}
        mock_menu().draw_menu.return_value = 'BACK'

        gpm = GPM()
        gpm.assign_members_to_projects()

        mock_print.assert_called_once()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_project_list.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_assign_members_to_projects_member_exceeded(self, mock_db, mock_input, mock_menu, mock_member_list,
                                                        mock_project_list, mock_print):
        mock_member_list.return_value = {'name': 'member_id', 'name2': 'member_id2'}
        mock_project_list.return_value = {'project_name': 'project_id'}
        mock_db().get_project_members.return_value = [['member_id']]
        mock_db().get_project_members_required.return_value = [1]
        mock_menu().draw_menu.return_value = 'project_name'

        gpm = GPM()
        gpm.assign_members_to_projects()

        mock_member_list.assert_called_once()
        self.assertEqual(mock_menu().draw_menu.call_count, 1)
        self.assertEqual(mock_input.call_count, 1)
        self.assertEqual(mock_print.call_count, 3)
        mock_db().get_project_members_required.assert_called_once()
        mock_db().get_project_members.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.GPM.delete_project_request')
    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_complete_member_project(self, mock_db, mock_input, mock_menu, mock_project_list, mock_delete_request,
                                     mock_print):
        mock_project_list.return_value = {'name': 'id'}
        mock_db().get_project_member_name.return_value = [['member_id', 'member_name']]
        mock_menu().draw_menu.side_effect = ['name', 'member_name']
        gpm = GPM()
        gpm.complete_member_project()

        mock_project_list.assert_called_once()
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        mock_db().commit_data.assert_called_once()
        mock_db().get_project_member_name.assert_called_once()
        mock_delete_request.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.input')
    def test_complete_member_project_back(self, mock_input, mock_menu, mock_project_list, mock_print):
        mock_project_list.return_value = {'project_name': 'project_id'}
        mock_menu().draw_menu.return_value = 'BACK'

        gpm = GPM()
        gpm.complete_member_project()

        mock_print.assert_called_once()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_project_list.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.GPM.get_project_list')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_complete_member_project_exception(self, mock_db, mock_project_list, mock_print):
        mock_project_list.side_effect = sqlite3.Error
        gpm = GPM()
        gpm.complete_member_project()
        self.assertEqual(mock_print.call_count, 2)
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.gpm.encrypt_pass')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_create_member(self, mock_db, mock_print, mock_input, mock_encrypt):
        mock_input.side_effect = ['name', 'pass@Pas123', 'username', 'state', 'district', '232323', '21', 'M']
        gpm = GPM()
        gpm.create_members()
        mock_db().add_user.assert_called_once()
        mock_db().add_personal_details.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_encrypt.assert_called_once()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 8)

    @mock.patch('mgnrega.gpm.input')
    @mock.patch('builtins.print')
    def test_create_member_invalid_password(self, mock_print, mock_input):
        mock_input.side_effect = ['name', 'pass@', '']
        gpm = GPM()
        gpm.create_members()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 3)

    @mock.patch('mgnrega.gpm.input')
    @mock.patch('builtins.print')
    def test_create_member_invalid_pincode(self, mock_print, mock_input):
        mock_input.side_effect = ['name', 'pass@Pas123', 'username', 'state', 'district', '23s2323', '']
        gpm = GPM()
        gpm.create_members()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 7)

    @mock.patch('mgnrega.gpm.input')
    @mock.patch('builtins.print')
    def test_create_member_invalid_age(self, mock_print, mock_input):
        mock_input.side_effect = ['name', 'pass@Pas123', 'username', 'state', 'district', '232323', 'invalid-age', '']
        gpm = GPM()
        gpm.create_members()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 8)

    @mock.patch('mgnrega.gpm.input')
    @mock.patch('builtins.print')
    def test_create_member_invalid_gender(self, mock_print, mock_input):
        mock_input.side_effect = ['name', 'pass@Pas123', 'username', 'state', 'district', '232323', '21', 'male', '']
        gpm = GPM()
        gpm.create_members()
        mock_print.assert_called_once()
        self.assertEqual(mock_input.call_count, 9)

    @mock.patch('mgnrega.gpm.ConnectDb')
    @mock.patch('mgnrega.gpm.input', side_effect=Exception)
    @mock.patch('builtins.print')
    def test_create_member_exception(self, mock_print, mock_input, mock_db):
        gpm = GPM()
        gpm.create_members()
        mock_input.assert_called_once()
        mock_print.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.gpm.encrypt_pass')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_update_member_user_details(self, mock_db, mock_input, mock_gpm_list, mock_print, mock_menu, mock_encrypt):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'PASSWORD']
        mock_encrypt.return_value = 'Pass@123'
        mock_input.side_effect = ['', '', 'Pass@123']
        gpm = GPM()
        gpm.update_members()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 3)
        mock_db().update_user.assert_called_once_with('PASSWORD', mock.ANY, 'Pass@123')
        mock_db().commit_data.assert_called_once()

    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.Validation')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_update_member_personal_detail(self, mock_db, mock_input, mock_gpm_list, mock_validation, mock_print,
                                           mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'AGE']
        mock_validation.age.return_value = True
        mock_input.side_effect = ['', '', '21']
        gpm = GPM()
        gpm.update_members()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        mock_validation.age.assert_called_once()
        self.assertEqual(mock_input.call_count, 3)
        mock_db().update_personal_details.assert_called_once_with('AGE', mock.ANY, '21')
        mock_db().commit_data.assert_called_once()

    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.Validation')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    @mock.patch('mgnrega.gpm.input')
    def test_update_member_invalid_age(self, mock_input, mock_gpm_list, mock_validation, mock_print, mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'AGE']
        mock_validation.age.return_value = False
        mock_input.side_effect = ['', '', 'dummy_data', '']
        gpm = GPM()
        gpm.update_members()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 4)
        mock_validation.age.assert_called_once_with('dummy_data')

    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.Validation')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    @mock.patch('mgnrega.gpm.input')
    def test_update_member_invalid_pincode(self, mock_input, mock_gpm_list, mock_validation, mock_print, mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'PINCODE']
        mock_validation.pincode.return_value = False
        mock_input.side_effect = ['', '', 'dummy_data', '']
        gpm = GPM()
        gpm.update_members()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 4)
        mock_validation.pincode.assert_called_once_with('dummy_data')

    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.Validation')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    @mock.patch('mgnrega.gpm.input')
    def test_update_member_invalid_password(self, mock_input, mock_gpm_list, mock_validation, mock_print, mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'PASSWORD']
        mock_validation.password.return_value = False
        mock_input.side_effect = ['', '', 'dummy_data', '']
        gpm = GPM()
        gpm.update_members()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 4)
        mock_validation.password.assert_called_once_with('dummy_data')

    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.Validation')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    @mock.patch('mgnrega.gpm.input')
    def test_update_member_invalid_gender(self, mock_input, mock_gpm_list, mock_validation, mock_print, mock_menu):
        mock_gpm_list.return_value = {'name1': 'id1', 'name2': 'id2'}
        mock_menu().draw_menu.side_effect = ['name1', 'GENDER']
        mock_validation.gender.return_value = False
        mock_input.side_effect = ['', '', 'dummy_data', '']
        gpm = GPM()
        gpm.update_members()

        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_print.call_count, 2)
        mock_gpm_list.assert_called_once()
        self.assertEqual(mock_input.call_count, 4)
        mock_validation.gender.assert_called_once_with('dummy_data')

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    def test_update_member_exception(self, mock_gpm_list, mock_db, mock_print):
        mock_gpm_list.side_effect = Exception
        gpm = GPM()
        gpm.update_members()
        mock_print.assert_called_once()
        mock_gpm_list.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.gpm.input')
    @mock.patch('mgnrega.gpm.Menu')
    @mock.patch('mgnrega.gpm.GPM.get_members_list')
    def test_update_gpm_back(self, mock_gpm_list, mock_menu, mock_input):
        mock_gpm_list.return_value = {'name1': 'id1'}
        mock_menu().draw_menu.side_effect = ['BACK']
        gpm = GPM()
        gpm.update_members()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()
        mock_gpm_list.assert_called_once()

    @mock.patch('mgnrega.gpm.raw_data_to_table')
    @mock.patch('mgnrega.gpm.decrypt_pass')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_show_members(self, mock_db, mock_decrypt, mock_table):
        mock_db().get_subordinate_details.return_value.fetchall.return_value = [('dummy', 'dummy', 'dummy')]
        gpm = GPM()
        gpm.show_members()

        mock_db().get_subordinate_details.assert_called_once()
        mock_db().get_subordinate_details().fetchall.assert_called_once()
        mock_decrypt.assert_called_once()
        mock_table.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_show_members_none(self, mock_db, mock_print):
        mock_db().get_subordinate_details.return_value.fetchall.return_value = []
        gpm = GPM()
        gpm.show_members()

        mock_db().get_subordinate_details.assert_called_once()
        mock_db().get_subordinate_details().fetchall.assert_called_once()
        mock_print.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_assign_project_members_request(self, mock_db, mock_print):
        mock_db().get_created_by_id.return_value = ['bdo_id']
        mock_db().get_approvals_list.return_value = [['MEMBER|member1|cc29a75e-8bf8-48e0-85f5-6990f4cc87e8|4b602623-'
                                                       '8d64-4fdf-8e9f-18b7b3f4389b|project1']]
        mock_db().get_user_name.return_value = ['name']
        mock_db().get_project_name.return_value = ['project_name']
        gpm = GPM()
        gpm.project_id = 'project_id'
        gpm.gpm_id = 'gpm_id'
        gpm.member_id = 'member_id'

        gpm.assign_project_members_request()

        mock_db().get_created_by_id.assert_called_once()
        mock_db().get_approvals_list.assert_called_once()
        mock_db().get_user_name.assert_called_once_with('member_id')
        mock_db().get_project_name.assert_called_once_with('project_id')
        mock_db().register_complain.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_print.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_assign_project_members_similar_request(self, mock_db, mock_print):
        mock_db().get_created_by_id.return_value = ['bdo_id']
        mock_db().get_approvals_list.return_value = [['MEMBER|member1|member_id|project_id|project1']]
        gpm = GPM()
        gpm.project_id = 'project_id'
        gpm.gpm_id = 'gpm_id'
        gpm.member_id = 'member_id'

        gpm.assign_project_members_request()

        mock_db().get_created_by_id.assert_called_once()
        mock_db().get_approvals_list.assert_called_once()
        mock_print.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_assign_project_members_request_exception(self, mock_db, mock_print):
        mock_db().get_created_by_id.side_effect = sqlite3.Error
        gpm = GPM()
        gpm.assign_project_members_request()
        mock_print.assert_called_once()
        mock_db().get_created_by_id.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_get_gpm_project_list(self, mock_db):
        mock_db().get_gpm_project_names.return_value = [['name', 'id']]
        sample_dict = {'name': 'id'}
        gpm = GPM()
        result = gpm.get_project_list()
        mock_db().get_gpm_project_names.assert_called_once()
        self.assertEqual(result, sample_dict)


    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_delete_project_members_request(self, mock_db, mock_print):
        mock_db().get_created_by_id.return_value = ['bdo_id']
        mock_db().get_approvals_list.return_value = [['WAGE|member1|cc29a75e-8bf8-48e0-85f5-6990f4cc87e8|4b602623-'
                                                       '8d64-4fdf-8e9f-18b7b3f4389b|project1']]
        mock_db().get_user_name.return_value = ['name']
        mock_db().get_project_name.return_value = ['project_name']
        gpm = GPM()
        gpm.project_id = 'project_id'
        gpm.gpm_id = 'gpm_id'
        gpm.member_id = 'member_id'

        gpm.delete_project_request()

        mock_db().get_created_by_id.assert_called_once()
        mock_db().get_approvals_list.assert_called_once()
        mock_db().get_user_name.assert_called_once_with('member_id')
        mock_db().get_project_name.assert_called_once_with('project_id')
        mock_db().register_complain.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_print.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_delete_project_members_similar_request(self, mock_db, mock_print):
        mock_db().get_created_by_id.return_value = ['bdo_id']
        mock_db().get_approvals_list.return_value = [['WAGE|member1|member_id|project_id|project1']]
        gpm = GPM()
        gpm.project_id = 'project_id'
        gpm.gpm_id = 'gpm_id'
        gpm.member_id = 'member_id'

        gpm.delete_project_request()

        mock_db().get_created_by_id.assert_called_once()
        mock_db().get_approvals_list.assert_called_once()
        mock_print.assert_called_once()

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_delete_project_members_request_exception(self, mock_db, mock_print):
        mock_db().get_created_by_id.side_effect = sqlite3.Error
        gpm = GPM()
        gpm.delete_project_request()
        mock_print.assert_called_once()
        mock_db().get_created_by_id.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_get_members_list(self, mock_db):
        mock_db().get_user_names.return_value = [['name', 'id']]
        sample_dict = {'name': 'id'}
        gpm = GPM()
        result = gpm.get_members_list()
        mock_db().get_user_names.assert_called_once()
        self.assertEqual(result, sample_dict)












    @mock.patch('mgnrega.gpm.PrettyTable')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    @mock.patch('mgnrega.gpm.Menu')
    def test_show_request_rejected_issue(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [
            ['ISSUES', 'dummy', 'member request msg', 'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'REJECTED'
        mock_input.side_effect = ['0', '']

        gpm = GPM()
        gpm.show_requests()

        mock_menu().draw_menu.assert_called_once()
        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().resolve_request.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('mgnrega.gpm.PrettyTable')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    @mock.patch('mgnrega.gpm.Menu')
    def test_show_request_approved_issue(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [
            ['ISSUES', 'dummy', 'request message', 'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'APPROVED'
        mock_input.side_effect = ['0', '']

        gpm = GPM()
        gpm.show_requests()

        mock_menu().draw_menu.assert_called_once()
        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().resolve_request.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_show_request_no_request(self, mock_db, mock_print):
        mock_db().get_requests.return_value.fetchall.return_value = []
        mock_db().get_requests.return_value.description.return_value = ()
        gpm = GPM()
        gpm.show_requests()

        mock_db().get_requests.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 1)

    @mock.patch('mgnrega.gpm.PrettyTable')
    @mock.patch('mgnrega.gpm.input')
    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    @mock.patch('mgnrega.gpm.Menu')
    def test_show_request_invalid_index(self, mock_menu, mock_db, mock_print, mock_input, mock_table):
        mock_db().get_requests.return_value.description.return_value = ['dummy', 'dummy', 'dummy', 'dummy', 'dummy']
        mock_db().get_requests.return_value.fetchall.return_value = [['ISSUES', 'dummy', 'request message', 'dummy', 'dummy']]
        mock_menu().draw_menu.return_value = 'APPROVED'
        mock_input.side_effect = ['invalid_row', '']

        gpm = GPM()
        gpm.show_requests()

        mock_table.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().get_requests().fetchall.assert_called_once()
        self.assertEqual(mock_print.call_count, 3)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('builtins.print')
    @mock.patch('mgnrega.gpm.ConnectDb')
    def test_show_request_exception(self, mock_db, mock_print):
        mock_db().get_requests.side_effect = Exception
        gpm = GPM()
        gpm.show_requests()
        mock_print.assert_called_once()
        mock_db().get_requests.assert_called_once()
        mock_db().rollback_data.assert_called_once()

if __name__ == '__main__':
    unittest.main()

import unittest
import mock
import sqlite3
from common.connect_db import ConnectDb


class DbConnectTest(unittest.TestCase):

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_user_with_role(self, mock_cursor):
        # arrange
        name = 'sample_name'
        role = 1
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_user_with_role(name, role)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, (name, role))
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sys')
    @mock.patch('common.connect_db.sqlite3.connect', side_effect=sqlite3.Error)
    def test_db_connection_fail(self, mock_cursor, mock_sys):
        ConnectDb()
        mock_sys.exit.assert_called_once()

    @mock.patch('common.connect_db.yaml')
    @mock.patch('common.connect_db.sqlite3.connect')
    def test_db_connection(self, mock_cursor, mock_yaml):
        ConnectDb()
        mock_yaml.load.assert_called_once()
        mock_cursor.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_db_script(self, mock_cursor):
        db = ConnectDb()
        db.db_script()

        mock_cursor().cursor().executescript.assert_called_once()
        mock_cursor().commit.assert_called_once()
        mock_cursor().cursor().close.assert_called_once()
        mock_cursor().close.assert_called_once()

    @mock.patch.object(ConnectDb, 'commit_data', side_effect=sqlite3.Error)
    @mock.patch('common.connect_db.sys')
    @mock.patch('common.connect_db.sqlite3.connect')
    def test_db_script_fail(self, mock_cursor, mock_sys, mock_connect):
        db = ConnectDb()
        db.db_script()

        mock_sys.exit.assert_called_once()
        mock_cursor().cursor().close.assert_called_once()
        mock_cursor().rollback.assert_called_once()
        mock_cursor().close.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_member_details(self, mock_cursor):
        # arrange
        member_id = 'member-id'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_member_details(member_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [member_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_member_project(self, mock_cursor):
        # arrange
        member_id = 'member-id'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_member_project(member_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [member_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_bdo_gpm_for_member(self, mock_cursor):
        # arrange
        member_id = 'member-id'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_bdo_gpm_for_member(member_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [member_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.uuid')
    @mock.patch('common.connect_db.sqlite3.connect')
    def test_register_complain(self, mock_cursor, mock_uuid):
        # arrange
        issue = 'sample-issue'
        sender_id = 'sample_id'
        request_msg = 'msg'
        recipient_id = 'recipient-id'
        request_id = '1234'
        mock_uuid.uuid4.return_value = request_id
        # act
        db = ConnectDb()
        db.register_complain(issue, sender_id, request_msg, recipient_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [issue, sender_id, request_msg, mock.ANY,
                                                                          recipient_id, request_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_gpm_projects_details(self, mock_cursor):
        # arrange
        gpm_id = 'sample-id'
        # act
        db = ConnectDb()
        result = db.get_gpm_projects_details(gpm_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [gpm_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_project_members(self, mock_cursor):
        # arrange
        project_id = 'project-id'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_project_members(project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_project_members_required(self, mock_cursor):
        # arrange
        project_id = 'project-id'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_project_members_required(project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_project_member_name(self, mock_cursor):
        # arrange
        project_id = 'project-id'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_project_member_name(project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_add_user(self, mock_cursor):
        # arrange
        user_id = '1234'
        encrypted_pass = 'pass'
        user_name = 'username'
        role_id = 2
        created_at = '2020-01-01'
        updated_at = '2020-02-02'
        name = 'name'
        is_deleted = 'False'
        # act
        db = ConnectDb()
        db.add_user(user_id, encrypted_pass, user_name, role_id, created_at, updated_at, name, is_deleted)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [user_id, encrypted_pass, user_name, role_id,
                                                                          created_at, updated_at, name, is_deleted])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_add_personal_details(self, mock_cursor):
        # arrange
        user_id = '1234'
        state = 'state'
        district = 'distrcit'
        pincode = '123456'
        age = 21
        gender = 'male'
        created_by = '2020-02-02'

        # act
        db = ConnectDb()
        db.add_personal_details(user_id, state, district, pincode, age, gender, created_by)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [user_id, state, district, pincode, age,
                                                                          gender, created_by])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_update_user(self, mock_cursor):
        # arrange
        member_id = '1234'
        field = 'sample-field'
        user_input = 'sample-input'
        # act
        db = ConnectDb()
        db.update_user(field, member_id, user_input)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [user_input, mock.ANY, member_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_update_personal_details(self, mock_cursor):
        # arrange
        member_id = '1234'
        field = 'sample-field'
        user_input = 'sample-input'
        # act
        db = ConnectDb()
        db.update_personal_details(field, member_id, user_input)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [user_input, member_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_subordinate_details(self, mock_cursor):
        # arrange
        subordinate_id = '1234'
        # act
        db = ConnectDb()
        db.get_subordinate_details(subordinate_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [subordinate_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_created_by_id(self, mock_cursor):
        # arrange
        gpm_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_created_by_id(gpm_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [gpm_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_user_name(self, mock_cursor):
        # arrange
        user_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_user_name(user_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [user_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_project_name(self, mock_cursor):
        # arrange
        project_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_project_name(project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_approvals_list(self, mock_cursor):
        # arrange
        gpm_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = ['dummy']
        # act
        db = ConnectDb()
        result = db.get_approvals_list(gpm_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [gpm_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_requests(self, mock_cursor):
        # arrange
        receiver_id = '1234'
       # act
        db = ConnectDb()
        db.get_requests(receiver_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [receiver_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_resolve_request(self, mock_cursor):
        # arrange
        status = 'True'
        request_id = '1234'
        # act
        db = ConnectDb()
        db.resolve_request(status, request_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [mock.ANY, request_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_user_names(self, mock_cursor):
        # arrange
        creator_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = ['dummy']
        # act
        db = ConnectDb()
        result = db.get_user_names(creator_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [creator_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_update_member_gpm(self, mock_cursor):
        # arrange
        gpm_id = '1234'
        old_gmp_id = '4467'
       # act
        db = ConnectDb()
        db.update_member_gpm(gpm_id, old_gmp_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [gpm_id, old_gmp_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_gpm_projects(self, mock_cursor):
        # arrange
        gpm_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = ['dummy']
        # act
        db = ConnectDb()
        result = db.get_gpm_projects(gpm_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [gpm_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_create_project(self, mock_cursor):
        # arrange
        project_id = '1233'
        project_name = 'name'
        labours = 23
        cost = 23
        area = 234
        start_date = '2020-01-02'
        end_date = '2020-02-20'
        gpm_id = '1234'
        created_by = '4353'
        project_type = 'type'
        is_deleted = 'False'
        # act
        db = ConnectDb()
        db.create_project(project_id, project_name, labours, cost, area, start_date, end_date,gpm_id, created_by,
                       project_type, is_deleted)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id, project_name, labours, cost, area,
                                                                          start_date, end_date, gpm_id, created_by,
                                                                          project_type, is_deleted])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_update_project(self, mock_cursor):
        # arrange
        field = 'field_name'
        user_input = 'user_input'
        project_id = '1234'
        # act
        db = ConnectDb()
        db.update_project(field, user_input, project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [user_input, project_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_bdo_project_details(self, mock_cursor):
        # arrange
        bdo_id = '1234'
        # act
        db = ConnectDb()
        db.get_bdo_project_details(bdo_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [bdo_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_bdo_project_names(self, mock_cursor):
        # arrange
        bdo_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = ['dummy']
        # act
        db = ConnectDb()
        result = db.get_bdo_project_names(bdo_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [bdo_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_gpm_project_names(self, mock_cursor):
        # arrange
        gpm_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = ['dummy']
        # act
        db = ConnectDb()
        result = db.get_gpm_project_names(gpm_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [gpm_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_assign_project_members(self, mock_cursor):
        # arrange
        project_id = '1234'
        member_id = '2345'
        # act
        db = ConnectDb()
        db.assign_project_members(project_id, member_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id, member_id, mock.ANY])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_project_members_list(self, mock_cursor):
        # arrange
        project_id = '1234'
        mock_cursor.cursor().execute().fetchall.return_value = [['dummy']]
        # act
        db = ConnectDb()
        result = db.get_project_members_list(project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_members_assigned_project(self, mock_cursor):
        # arrange
        member_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = ['dummy']
        # act
        db = ConnectDb()
        result = db.get_members_assigned_project(member_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [member_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_register_project_completion(self, mock_cursor):
        # arrange
        project_id = '1234'
        member_id = '2345'
        assigned_date = '2020-01-02'
        total_days = 20
        wage = 2000
        # act
        db = ConnectDb()
        db.register_project_completion(project_id, member_id, assigned_date, total_days, wage)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id, member_id, assigned_date,
                                                                          total_days, wage])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_remove_project_member(self, mock_cursor):
        # arrange
        member_id = '2345'
        # act
        db = ConnectDb()
        db.remove_project_member(member_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [member_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_remove_project_all_members(self, mock_cursor):
        # arrange
        project_id = '2345'
        # act
        db = ConnectDb()
        db.remove_project_all_members(project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_find_project_is_assigned(self, mock_cursor):
        # arrange
        project_id = '2345'
        mock_cursor.cursor().execute().fetchone.return_value = ['dummy']
        # act
        db = ConnectDb()
        result = db.find_project_is_assigned(project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_bdo_approvals_list(self, mock_cursor):
        # arrange
        bdo_id = '2345'
        mock_cursor.cursor().execute().fetchone.return_value = ['dummy']
        # act
        db = ConnectDb()
        result = db.get_bdo_approvals_list(bdo_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [bdo_id])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, ['dummy']

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_close_conn(self, mock_cursor):
        # act
        db = ConnectDb()
        db.close_conn()
        # assert
        mock_cursor().cursor().close.assert_called_once()
        mock_cursor().close.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_commit_data(self, mock_cursor):
        # act
        db = ConnectDb()
        db.commit_data()
        # assert
        mock_cursor().commit.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_rollback_data(self, mock_cursor):
        # act
        db = ConnectDb()
        db.rollback_data()
        # assert
        mock_cursor().rollback.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_project_start_date(self, mock_cursor):
        # arrange
        project_id = '1234'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_project_start_date(project_id)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [project_id])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

if __name__ == '__main__':
    unittest.main()

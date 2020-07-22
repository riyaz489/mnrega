""" this file is used to perform database related operations."""

import sqlite3
import yaml
import sys
import datetime
import uuid


class ConnectDb:
    """ this is a class for database related operations.
        Attributes:
            conn (sqlite connection): connection object.
            cur (connection cursor): cursor object.
    """
    def __init__(self):
        """sqlite connection initialization."""
        try:
            with open("mgnrega/config.yaml", 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
                db_path = cfg['mysql']['db']
                conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(e)
            sys.exit()
        else:
            self.conn = conn
            self.cur = self.conn.cursor()

    def close_conn(self):
        """this method is used to close connection and cursor object."""
        self.cur.close()
        self.conn.close()

    def commit_data(self):
        """this method is used to commit changes on connection."""
        self.conn.commit()

    def rollback_data(self):
        """this method is used to rollback changes on connection ."""
        self.conn.rollback()

    def db_script(self):
        """this method is used to create schema for mgnrega project. """
        try:
            with open('data/schema_script.sql', 'r') as sql_file:
                sql_script = sql_file.read()
                self.cur.executescript(sql_script)
                self.commit_data()

        except sqlite3.Error:
            print('unable to run database script')
            self.rollback_data()
            sys.exit()
        finally:
            self.close_conn()

    def get_user_with_role(self, user_name, role_id):
        """
        this method is used to get user details for authentication purpose.
        :param user_name: string, user_name of user.
        :param role_id: int, role id of user.
        :return: list, user details.
        """
        query = "select * from users where user_name= ?  AND role_id = ? AND is_deleted = 'False'"
        user = self.cur.execute(query, (user_name, role_id))
        return user.fetchone()

    def get_member_details(self, member_id):
        """
        this method is used to get member details.
        :param member_id: string, member id.
        :return: list, member detail.
        """
        query = "select member.id,member.password,member.user_name,member.created_at,member.name,pd.state," \
                "pd.district,pd.pincode,pd.age,pd.gender,gpo.name as gpm_name from users member inner join" \
                " personal_details pd on member.id= pd.user_id  inner join users gpo on gpo.id=pd.created_by " \
                "where member.id=? and member.is_deleted='False'"
        return self.cur.execute(query, [member_id]).fetchone()

    def get_member_project(self, member_id):
        """
        this method is used to get members project.
        :param member_id: string, member id.
        :return: list, member project details.
        """
        query = "select project_members.assigned_date,projects.name, projects.project_type from project_members " \
                 "inner join projects on projects.id = project_members.project_id where member_id=?"
        return self.cur.execute(query, [member_id]).fetchone()

    def get_bdo_gpm_for_member(self, member_id):
        """
        this method is used to get bdo and gpm for member.
        :param member_id: string, member id.
        :return: list, bdo, gpm and member name.
        """
        query = "select member.user_id,member.created_by,gpo.created_by from personal_details member inner join " \
                "personal_details gpo on gpo.user_id = member.created_by where member.user_id = ?"
        return self.cur.execute(query, [member_id]).fetchone()

    def register_complain(self, issue, sender_id, request_msg, recipient_id):
        """
        this method is used to insert complain/issues/approvals.
        :param issue: string, issue type.
        :param sender_id: string, sender id.
        :param request_msg: string,  request message.
        :param recipient_id: string, recipient id.
        """
        query = "insert into requests (type,raised_by,request_msg,issued_on,raised_for, id) values(?,?,?,?,?,?)"
        self.cur.execute(query, [issue, sender_id, request_msg, datetime.datetime.now().date(), recipient_id,
                                 str(uuid.uuid4())])

    def get_gpm_projects_details(self, gpm_id):
        """
        this method is used to get gpm project details.
        :param gpm_id: string, gpm id.
        :return: cursor, iterable cursor contains data for gpm project.
        """
        query = "select projects.NAME as PROJECT_NAME,projects.project_type as PROJECT_TYPE,TOTAL_LABOUR_REQUIRED," \
                "ESTIMATED_COST,AREA_OF_PROJECT,ESTIMATED_START_DATE,ESTIMATED_END_DATE,users.NAME as BDO_NAME" \
                " from projects inner join users on users.id=projects.created_by where projects.is_deleted='False'" \
                " and projects.gpm_id=?"
        return self.cur.execute(query, [gpm_id])

    def get_project_members(self, project_id):
        """
        this method is used to get list of members ids in given project.
        :param project_id: string, project id.
        :return: list, member ids list.
        """
        query = "select member_id from project_members where project_id= ? "
        return self.cur.execute(query, [project_id]).fetchall()

    def get_project_members_required(self, project_id):
        """
        this method is used to get total number of required members in project.
        :param project_id: sting, project id.
        :return: list, total number of labour required in given project.
        """
        query = "select total_labour_required from projects where is_deleted='False' and id=?"
        return self.cur.execute(query, [project_id]).fetchone()

    def get_project_member_name(self, project_id):
        """
        this method is used to get member names and ids in given project.
        :param project_id: string, project id.
        :return: list, list of member ids and names.
        """
        query = "select member_id, users.name from project_members inner join users on users.id=" \
                "project_members.member_id where project_id= ? "
        result = self.cur.execute(query, [project_id])
        return result.fetchall()

    def add_user(self, id, encrypted_pass, user_name, role_id, created_at, updated_at, name, is_deleted):
        """
        this method is used to add new user.
        :param id: string, user id.
        :param encrypted_pass: string, encrypted password.
        :param user_name: string, user name.
        :param role_id: string, role id.
        :param created_at: datetime, created at date.
        :param updated_at: datetime, updated at date.
        :param name: string, name.
        :param is_deleted: bool, is deleted check.
        """
        query = "insert into users values (?,?,?,?,?,?,?,?)"
        self.cur.execute(query, [id, encrypted_pass, user_name, role_id, created_at, updated_at, name, is_deleted])

    def add_personal_details(self, id, state, district, pincode, age, gender, created_by):
        """
        this method is used to add personal details of given user.
        :param id: string, user id.
        :param state: string, user current state.
        :param district: string, user current district.
        :param pincode: int, user pincode.
        :param age: int, user age.
        :param gender: string, user gender.
        :param created_by: datetime, created at date.
        """
        query = "insert into personal_details values(?,?,?,?,?,?,?) "
        self.cur.execute(query, [id, state, district, pincode, age, gender, created_by])

    def update_user(self, field, member_id, user_input):
        """
        this method is used to update given user details.
        :param field: string, field name to update.
        :param member_id: string, member id.
        :param user_input: string, new data.
        """
        query = "update users set " + str(field) + " = ? ,updated_at=? where id= ?"
        self.cur.execute(query, [user_input, datetime.datetime.now().date(), member_id])

    def update_personal_details(self, field, member_id, user_input):
        """
        this method is used to update given user personal details.
        :param field: string, field name to update.
        :param member_id: string, member id.
        :param user_input: string, new data.
        """
        query = "update personal_details set " + str(field) + " = ? where user_id= ?"
        self.cur.execute(query, [user_input, member_id])

    def get_subordinate_details(self, user_id):
        """
        this method is used to get user subordinates.
        :param user_id: string, user_id.
        :return: cursor, iterable cursor object contains user subordinated details.
        """
        query = "select users.name, users.id,users.password,users.user_name,users.created_at," \
                "personal_details.state,personal_details.district,personal_details.pincode,personal_details.age," \
                "personal_details.gender from users inner join personal_details on users.id = personal_details.user_" \
                "id where personal_details.created_by=?  and users.is_deleted='False'"
        return self.cur.execute(query, [user_id])

    def get_created_by_id(self, user_id):
        """
        this method is used to get creator id.
        :param user_id: string, user_id.
        :return: list/None, creator id.
        """
        query = "select created_by from personal_details where user_id= ? "
        result = self.cur.execute(query, [user_id])
        return result.fetchone()

    def get_user_name(self, user_id):
        """
         this method is used to get user name.
        :param user_id: string, user id.
        :return: list/None, user name.
        """
        query = "select name from users where id =?"
        result = self.cur.execute(query, [user_id])
        return result.fetchone()

    def get_project_name(self, project_id):
        """
         this method is used to get project name.
        :param project_id: string, project id.
        :return: list/None, project name.
        """
        query = "select name from projects where id =?"
        result = self.cur.execute(query, [project_id])
        return result.fetchone()

    def get_approvals_list(self, gpm_id):
        """
         this method is used to get approvals types requests.
        :param gpm_id: string, gpm id.
        :return: list, all approval type requests for current gpm.
        """
        query = "select request_msg from requests where resolved_on is null and type='APPROVAL' and raised_by=?"
        result = self.cur.execute(query, [gpm_id])
        return result.fetchall()

    def get_requests(self, receiver_id):
        """
         this method is used to get request for current receiver.
        :param receiver_id: string, receiver id.
        :return: cursor, iterable cursor contains requests details.
        """
        query = "select type as request_type,name as raised_by,request_msg as request_message,issued_on,requests.id " \
                "from requests inner join users on raised_by = users.id where raised_for=? and resolved_on is null "
        return self.cur.execute(query, [receiver_id])

    def resolve_request(self, status, request_id):
        """
         this method is used to resolve requests.
        :param status: string, request status.
        :param request_id: string, request id.
        """
        # using string.format() to inserting null value in database if nothing happens to request
        query = "update requests set is_accepted={},resolved_on=? where id=?".format(status)
        self.cur.execute(query, [datetime.datetime.now().date(), request_id])

    def get_user_names(self, creator_id):
        """
        this method is used to get subordinates names and ids.
        :param creator_id: strong, creator user id.
        :return: list, list of users ids and names.
        """
        query = "select users.name, users.id from users inner join personal_details on  personal_details.user_id = id " \
                " where users.is_deleted ='False' and created_by=?"
        projects = self.cur.execute(query, [creator_id])
        return projects.fetchall()

    def update_member_gpm(self, gpm_id, old_gmp_id):
        """
        this method is used to update members gpm.
        :param gpm_id: string, new gpm id.
        :param old_gmp_id: string, old gpm id.
        """
        query = "update personal_details set created_by = ? where created_by=?"
        self.cur.execute(query, [gpm_id, old_gmp_id])

    def get_gpm_projects(self, gpm_id):
        """
        this method is used to et gpm projects list.
        :param gpm_id: string, gpm id.
        :return: list, projects ids.
        """
        query = "select id from projects where gpm_id= ?"
        result = self.cur.execute(query, [gpm_id])
        return result.fetchall()

    def create_project(self, project_id, project_name, labours, cost, area, start_date, end_date,gpm_id, created_by,
                       project_type, is_deleted):
        """
        this method is used to create a new project.
        :param project_id: string, project id.
        :param project_name: string, project name.
        :param labours: int, total labours required.
        :param cost: int, project estimated cost.
        :param area: int, project area.
        :param start_date: datetime, project start date.
        :param end_date: datetime, project end date.
        :param gpm_id: string, gpm id.
        :param created_by: string, creator user id.
        :param project_type: string, project type.
        :param is_deleted: bool, project is deleted status.
        """
        query = "insert into projects values (?,?,?,?,?,?,?,?,?,?,?)"
        self.cur.execute(query, [project_id, project_name, labours, cost, area, start_date, end_date, gpm_id,
                                 created_by, project_type, is_deleted])

    def update_project(self, field, user_input, project_id):
        """
        this method is used to update project details.
        :param field: string, project field.
        :param user_input: string, user input.
        :param project_id: string, project id.
        """
        query = "update projects set " + str(field) + " = ? where id= ?"
        self.cur.execute(query, [user_input, project_id])

    def get_bdo_project_details(self, bdo_id):
        """
        this method is used to get bdo project details.
        :param bdo_id: string, bdo id.
        :return: cursor, iterable cursor contains project details.
        """
        query = "select projects.NAME ,TOTAL_LABOUR_REQUIRED,ESTIMATED_COST,AREA_OF_PROJECT,ESTIMATED_START_DATE," \
                "ESTIMATED_END_DATE,users.NAME as GPM_NAME,projects.PROJECT_TYPE from projects inner join users" \
                " on users.id=projects.gpm_id where projects.is_deleted='False' and projects.created_by=?"
        return self.cur.execute(query, [bdo_id])

    def get_bdo_project_names(self, bdo_id):
        """
        this method is used to bdo project names.
        :param bdo_id: string, bdo id.
        :return: list, list of bdo project names and ids.
        """
        query = "select name, id from projects where is_deleted ='False' and created_by=?"
        projects = self.cur.execute(query, [bdo_id])
        return projects.fetchall()

    def get_gpm_project_names(self, gpm_id):
        """
        this method is used to get gpm project names and ids.
        :param gpm_id: string, gpm id.
        :return: list, list of all gpm project names and ids.
        """
        query = "select name, id from projects where is_deleted ='False' and gpm_id=?"
        projects = self.cur.execute(query, [gpm_id])
        return projects.fetchall()

    def assign_project_members(self, project_id, member_id):
        """
        this method is used to add new member to given project.
        :param project_id:string, project id.
        :param member_id: string, member id.
        """
        query = "insert into project_members values (?,?,?)"
        self.cur.execute(query, [project_id, member_id, datetime.datetime.now().date()])

    def get_members_assigned_project(self, member_id):
        """
        this method is used to get project members list for given project.
        :param member_id: string, member id.
        :return: list, list of all member ids.
        """
        query = "select * from project_members where member_id =?"
        project_member = self.cur.execute(query, [member_id])
        return project_member.fetchone()

    def get_project_members_list(self, project_id):
        """
        this method is used to get project members list for given project.
        :param project_id: string, project id.
        :return: list, list of all member ids.
        """
        query = "select * from project_members where project_id =?"
        project_member = self.cur.execute(query, [project_id])
        return project_member.fetchall()

    def register_project_completion(self, project_id, member_id, assigned_date, total_days, wage):
        """
        this method is used to store member project completion details.
        :param project_id: string, project id.
        :param member_id: string, member id.
        :param assigned_date: datetime, assigned date.
        :param total_days: int, total working days.
        :param wage: int, total wage of member.
        """
        query = "insert into completed_project_members values (?,?,?,?,?)"
        self.cur.execute(query, [project_id, member_id, assigned_date, total_days, wage])

    def remove_project_member(self, member_id):
        """
        this method is used to remove member from current project.
        :param member_id: string, member id.
        """
        query = "delete from project_members where member_id =?"
        self.cur.execute(query, [member_id])

    def remove_project_all_members(self, project_id):
        """
        this method is used to remove all members from given project.
        :param project_id: string, project id.
        """
        query = "delete from project_members where project_id =?"
        self.cur.execute(query, [project_id])

    def find_project_is_assigned(self, project_id):
        """
        this method is used to find if anyone still assigned to given project.
        :param project_id: string, project id.
        :return: list, list of project id.
        """
        query = "select project_id from project_members where project_id =?"
        return self.cur.execute(query, [project_id]).fetchall()

    def get_bdo_approvals_list(self, bdo_id):
        """
        this method is used to get approvals type requests for current bdo.
        :param bdo_id: string, bdo id.
        :return: list, list of request ids and request messages.
        """
        query = "select id, request_msg from requests where resolved_on is null and type='APPROVAL' and raised_for=?"
        result = self.cur.execute(query, [bdo_id])
        return result.fetchall()

    def get_project_start_date(self, project_id):
        """
        this method is used to get project start date .
        :param project_id: string, gpm id.
        :return: list, return project start date.
        """
        query = "select estimated_start_date from projects where id = ?"
        projects = self.cur.execute(query, [project_id])
        return projects.fetchone()



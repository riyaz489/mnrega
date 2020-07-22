""" this file is used to perform gpm related operations."""

from common.constants import GpmFeatures, ApprovalType, RequestType, Role, Color, Base, GpmUpdateFields, \
    RequestResult, BackButton
from common.helper import Menu, PrettyTable
from future.builtins import input
from common.validations import Validation
from common.connect_db import ConnectDb
import datetime
import sqlite3
import uuid
import sys
from common.password_encryption import encrypt_pass, decrypt_pass
from common.helper import raw_data_to_table
import os


class GPM:
    """this is a class for GPM related operations.
            Attributes:
                conn (sqlite connection): connection object.
                bdo_id (string): bdo id.
                project_id (string): project id.
                gpm_id (string): gpm id.
                member_id (string): member id.
        """
    def __init__(self):
        """
               initializing GPM class .
        """
        self.conn = ConnectDb()
        self.project_id = ' '
        self.gpm_id = ' '
        self.bdo_id = ''
        self.member_id = ''

    def __del__(self):
        """
            closing database connection.
        """
        self.conn.close_conn()

    def gpm_features(self):
        """
            this method is used to print all gpm features on console.
        """
        try:
            print("choose feature :\n")
            menu = Menu()
            features = [x.name for x in GpmFeatures]
            features.extend([str(BackButton.EXIT.name)])
            feature = menu.draw_menu(features)
            input()
            required_feature = getattr(self, feature.lower())
            required_feature()
            # again calling gpm menu
            input()
            os.system('clear')
            self.gpm_features()

        except Exception as e:
            print(e)
            sys.exit()

    def show_projects(self):
        """
            this method is used to print all project of current gpm.
        """
        projects = self.conn.get_gpm_projects_details(self.gpm_id)
        result = projects.fetchall()
        raw_data_to_table(result, projects)

    def project_completion(self):
        """
            this method is used to complete project of current gpm.
        """
        try:
            print("choose project")
            project_list = self.get_project_list()
            menu = Menu()
            project_names = [x for x in project_list.keys()]
            project_names.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
            project_name = menu.draw_menu(project_names)
            input()
            if str(BackButton.BACK.name) == project_name:
                return
            project_id = project_list[project_name]
            self.project_id = project_id
            member_ids = self.conn.get_project_members(self.project_id)
            if len(member_ids) == 0:
                print(Color.F_Red+"Can't send project completion request to BDO \n because "
                                  "no member assigned to this project \n"+Base.END)
            else:
                for member_id in member_ids:
                    self.member_id = member_id[0]
                    self.delete_project_request()
                self.conn.commit_data()
                print(Color.F_Green + "Wage Request sent to BDO for all the assigned members \n "+ Base.END)
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback_data()

    def assign_members_to_projects(self):
        """
              this method is used to assign member to project of current gpm.
        """
        print("choose project")
        project_list = self.get_project_list()
        menu = Menu()
        project_names = [x for x in project_list.keys()]
        project_names.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
        project_name = menu.draw_menu(project_names)
        input()
        if str(BackButton.BACK.name) == project_name:
            return
        project_id = project_list[project_name]
        print("choose member for project")
        members_list = self.get_members_list()
        self.project_id = project_id
        project_members_id = self.conn.get_project_members(self.project_id)
        # removing already assigned members from the list
        for id in project_members_id:
            temp = None
            for key, value in members_list.items():
                if id[0] == value:
                    temp = key
                    break
            members_list.pop(temp, None)
        members_required = self.conn.get_project_members_required(self.project_id)
        # checking if total number of members in given project are less then actual project requirement
        if int(members_required[0]) <= len(project_members_id):
            print(Color.F_Red + "members limit exceeded" + Base.END)
            return
        menu = Menu()
        member_names = [x for x in members_list.keys()]
        member_names.extend([str(BackButton.EXIT.name)])
        member_name = menu.draw_menu(member_names)
        input()
        member_id = members_list[member_name]
        self.member_id = member_id
        self.assign_project_members_request()

    def complete_member_project(self):
        """
            this method is used to complete project of current gpm.
        """
        try:
            print("choose project")
            project_list = self.get_project_list()
            menu = Menu()
            project_names = [x for x in project_list.keys()]
            project_names.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
            project_name = menu.draw_menu(project_names)
            input()
            if str(BackButton.BACK.name) == project_name:
                return
            project_id = project_list[project_name]
            self.project_id = project_id
            member_ids = self.conn.get_project_member_name(self.project_id)
            member_dict = {}
            for data in member_ids:
                member_dict[data[1]] = data[0]
            menu = Menu()
            member_names = [x for x in member_dict.keys()]
            member_names.extend([str(BackButton.EXIT.name)])
            member_name = menu.draw_menu(member_names)
            input()
            member_id = member_dict[member_name]
            self.member_id = member_id
            self.delete_project_request()
            self.conn.commit_data()
            print(Color.F_Green + "member removal request sent to BDO" + Base.END)
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback_data()

    def create_members(self):
        """
             this method is used to create member under current gpm.
        """

        try:
            name = input("enter member name ")
            id = str(uuid.uuid4())
            password = input("enter password for member ")
            if not Validation.password(password):
                print("password is weak")
                input()
                return
            user_name = input("enter user name for member ")
            role_id = int(Role.Member.value)
            created_at = datetime.datetime.now().date()
            updated_at = datetime.datetime.now().date()
            is_deleted = 'False'
            state = input("enter state ")
            district = input("enter district ")
            pincode = input("enter pincode ")
            if not Validation.pincode(pincode):
                print("pincode is not valid")
                input()
                return
            age = input("enter age ")
            if not Validation.age(age):
                print("age is not valid")
                input()
                return
            gender = input("enter gender ")
            if not Validation.gender(gender):
                print("gender is not valid")
                input()
                return
            created_by = self.gpm_id
            encrypted_pass = encrypt_pass(password)
            self.conn.add_user(id, encrypted_pass, user_name, role_id, created_at, updated_at, name, is_deleted)
            self.conn.add_personal_details(id, state, district, pincode, age, gender, created_by)
            self.conn.commit_data()
            print("\n" + Color.F_Green + "record inserted" + Base.END)
        except Exception as e:
            print(e)
            self.conn.rollback_data()

    def update_members(self):
        """
           this method is used to update member details of current gpm.
        """
        try:
            members_list = self.get_members_list()
            menu = Menu()
            members_names = [x for x in members_list.keys()]
            members_names.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
            members_name = menu.draw_menu(members_names)
            input()
            if str(BackButton.BACK.name) == members_name:
                return
            members_id = members_list[members_name]
            print("select the field to update: \n")
            menu = Menu()
            details = [x.name for x in GpmUpdateFields]
            details.extend([str(BackButton.EXIT.name)])
            field = menu.draw_menu(details)
            input()
            user_input = input("enter new value for " + str(field)+" ")
            user_table_fields = [1, 2, 3]

            # validations
            if field == str(GpmUpdateFields.PASSWORD.name):
                if not Validation.password(user_input):
                    print("password is weak")
                    input()
                    return
                user_input = encrypt_pass(user_input)
            if field == str(GpmUpdateFields.GENDER.name):
                if not Validation.gender(user_input):
                    print("gender is not valid")
                    input()
                    return
            if field == str(GpmUpdateFields.PINCODE.name):
                if not Validation.pincode(user_input):
                    print("pincode is not valid")
                    input()
                    return
            if field == str(GpmUpdateFields.AGE.name):
                if not Validation.age(user_input):
                    print("age is not valid")
                    input()
                    return
            # if field belong to user table
            if user_table_fields.count(GpmUpdateFields[field].value) == 1:
                self.conn.update_user(str(field), members_id, user_input)
            else:
                self.conn.update_personal_details(str(field), members_id, user_input)
            self.conn.commit_data()
            print("\n" + Color.F_Green + "record updated" + Base.END)

        except Exception as e:
            print(e)
            self.conn.rollback_data()

    def show_members(self):
        """
            this method is used to print all members of current gpm.
        """
        details_cursor = self.conn.get_subordinate_details(self.gpm_id)
        members_list = details_cursor.fetchall()
        if len(members_list) == 0:
            print(Color.F_Green + "you don't have any member under you" + Base.END)
            return
        # converting list of tuples into list of list
        list_data = [list(elem) for elem in members_list]
        for member in list_data:
            member[2] = decrypt_pass(member[2])

        raw_data_to_table(list_data, details_cursor)

    def get_project_list(self):
        """
            this method is used to get all project of current gpm.
        :return: dict, project name and id dictionary
        """
        result = self.conn.get_gpm_project_names(self.gpm_id)
        gpm_dict = {}
        for data in result:
            gpm_dict[data[0]] = data[1]
        return gpm_dict

    def assign_project_members_request(self):
        """
            this method is used send wage request for given member of current project.
        """
        try:
            bdo_id = self.conn.get_created_by_id(self.gpm_id)
            self.bdo_id = bdo_id[0]
            # check for similar request
            old_requests = self.conn.get_approvals_list(self.gpm_id)
            for old_request in old_requests:
                old_request_data = old_request[0].split('|')
                if old_request_data[0] == str(ApprovalType.MEMBER.name) and old_request_data[2] == self.member_id and\
                        old_request_data[3] == self.project_id:
                    print(Color.F_Red + "already have similar request" + Base.END)
                    return
            request_msg = str(ApprovalType.MEMBER.name) + "|"
            name = self.conn.get_user_name(self.member_id)
            project_name = self.conn.get_project_name(self.project_id)
            request_msg += str(name[0]) + "|" + self.member_id + "|" + self.project_id+'|'+str(project_name[0])
            self.conn.register_complain(str(RequestType.APPROVAL.name), self.gpm_id, request_msg, self.bdo_id)
            self.conn.commit_data()
            print(Color.F_Green+"member assigned request sent to BDO"+Base.END)
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback_data()

    def delete_project_request(self):
        """
           this method is used send wage request for all members of current project.
        """
        try:
            bdo_id = self.conn.get_created_by_id(self.gpm_id)
            self.bdo_id = bdo_id[0]
            # check for similar request
            old_requests = self.conn.get_approvals_list(self.gpm_id)
            for old_request in old_requests:
                old_request_data = old_request[0].split('|')
                if old_request_data[0] == str(ApprovalType.WAGE.name) and old_request_data[2] == self.member_id and \
                        old_request_data[3] == self.project_id:
                    print(Color.F_Red + "already have similar request" + Base.END)
                    return
            request_msg = str(ApprovalType.WAGE.name)+"|"
            name = self.conn.get_user_name(self.member_id)
            project_name = self.conn.get_project_name(self.project_id)
            request_msg += str(name[0])+"|"+self.member_id+"|"+self.project_id+'|'+str(project_name[0])
            self.conn.register_complain(str(RequestType.APPROVAL.name), self.gpm_id, request_msg, self.bdo_id)
            self.conn.commit_data()
            print(Color.F_Green+"member project wage request sent to BDO"+Base.END)
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback_data()

    def show_requests(self):
        """
            this method is used show request and resolve request of current gpm.
        """
        try:
            projects = self.conn.get_requests(self.gpm_id)
            result = projects.fetchall()
            counter = 0
            # getting columns for showing requests and adding index column at first in list
            projects_fields = (('index'),) + projects.description
            # request is empty then returning early with a message
            if len(result) == 0:
                print(Color.F_Red + "there is no pending request" + Base.END)
                return
            temp = result
            # converting list of tuples into list of list
            temp = [list(elem) for elem in temp]
            print("write index of request to manage:\n")
            for request in temp:
                request.insert(0, counter)
                counter += 1
            table = PrettyTable()
            table.field_names = [column[0] for column in projects_fields[:-1]]
            for row in temp:
                table.add_row(row[:-1])
            print(table)
            row_number = input("enter index number: ")
            if not Validation.is_int(row_number):
                print("row number is not valid")
                input()
                return
            menu = Menu()
            result_names = [x.name for x in RequestResult]
            result_names.extend([str(BackButton.EXIT.name)])
            result_name = menu.draw_menu(result_names)
            input()
            status = "NULL"
            if str(result_name) == str(RequestResult.APPROVED.name):
                status = "'True'"
            elif str(result_name) == str(RequestResult.REJECTED.name):
                status = "'False'"

            self.conn.resolve_request(status, result[int(row_number)][4])
            self.conn.commit_data()
            print(Color.F_Green + "Request completed successfully" + Base.END)
        except Exception as e:
            print(e)
            self.conn.rollback_data()

    def get_members_list(self):
        """
        returns members list under given gpm
        :return: dict, member names and id dictionary
        """
        result = self.conn.get_user_names(self.gpm_id)
        gpm_dict = {}
        for data in result:
            gpm_dict[data[0]] = data[1]
        return gpm_dict

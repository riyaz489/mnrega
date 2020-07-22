""" this file is used to perform bdo related operations."""

import sys
import uuid
import datetime
import os
from prettytable import PrettyTable
from common.validations import Validation
from common.constants import BdoFeatures
from common.helper import Menu
from future.builtins import input
from common.connect_db import ConnectDb
from common.helper import raw_data_to_table
from mgnrega.gpm import GPM
from common.password_encryption import encrypt_pass, decrypt_pass
from common.constants import Role, ProjectType, ProjectsUpdateFields, Color, Base, GpmUpdateFields,\
    RequestType, RequestResult, ApprovalType, BackButton


class BDO:
    """this is a class for BDO related operations.
        Attributes:
            conn (sqlite connection): connection object.
            bdo_id (string): bdo id.
            project_id (string): project id.
            gpm_id (string): gpm id.
            member_id (string): member id.
    """
    def __init__(self):
        """
        initializing BDO class .
        """
        self.conn = ConnectDb()
        self.bdo_id = ''
        self.project_id = ' '
        self.gpm_id = ' '
        self.member_id = ''

    def __del__(self):
        """
        closing database connection.
        """
        self.conn.close_conn()

    def bdo_features(self):
        """
        this method is used to print all bdo features on console.
        """
        try:
            while True:
                print("choose feature :\n")
                menu = Menu()
                features = [x.name for x in BdoFeatures]
                features.extend([str(BackButton.EXIT.name)])
                feature = menu.draw_menu(features)
                input()
                required_feature = getattr(self, feature.lower())
                required_feature()
                # again calling gpm menu
                input()
                os.system('clear')
                self.bdo_features()

        except Exception as e:
            print(e)
            sys.exit()

    def show_gpm(self):
        """
        this method is used to print all gpm of current bdo.
        """
        print("GPM's list:\n")
        result = self.conn.get_subordinate_details(self.bdo_id)
        data = result.fetchall()
        if len(data) == 0:
            print(Color.F_Green+"you don't have any GPM under you"+Base.END)
            return
        # converting list of tuples into list of list
        list_data = [list(elem) for elem in data]
        for gpm in list_data:
            gpm[2] = decrypt_pass(gpm[2])
        raw_data_to_table(list_data, result)

    def show_members(self):
        """
        this method is used to print members and gpm of current bdo.
        """
        print("members List:\n")
        gpm_list = self.conn.get_user_names(self.bdo_id)
        if len(gpm_list) == 0:
            print(Color.F_Green+"you don't have any GPM  and members under you"+Base.END)
            return
        for gpm_detail in gpm_list:
            print('GPM name '+gpm_detail[0])
            gpm = GPM()
            gpm.gpm_id = gpm_detail[1]
            gpm.show_members()

    def create_gpm(self):
        """
        this method is used to create gpm for current bdo.
        """
        try:
            name = input("enter gpm name ")
            id = str(uuid.uuid4())
            password = input("enter password for gpm ")
            if not Validation.password(password):
                print("weak password")
                input()
                return
            user_name = input("enter user name for gpm ")
            role_id = int(Role.GPM.value)
            created_at = datetime.datetime.now().date()
            updated_at = datetime.datetime.now().date()
            is_deleted = 'False'
            state = input("enter state ")
            district = input("enter district ")
            pincode = input("enter pincode ")
            if not Validation.pincode(pincode):
                print("pin code is not valid")
                input()
                return

            age = input("enter age ")
            if not Validation.is_int(age):
                print("age is not valid")
                input()
                return
            gender = input("enter gender ")
            if not Validation.gender(gender):
                print("gender is not valid")
                input()
                return
            created_by = self.bdo_id
            encrypted_pass = encrypt_pass(password)
            self.conn.add_user(id, encrypted_pass, user_name, role_id, created_at, updated_at, name, is_deleted)
            self.conn.add_personal_details(id, state, district, pincode, age, gender,created_by)
            self.conn.commit_data()
            print("\n"+Color.F_Green + "record inserted"+Base.END)
        except Exception as e:
            print(e)
            self.conn.rollback_data()

    def delete_gpm(self):
        """
          this method is used to delete gpm for current bdo.
        """
        try:
            print("choose gmp to delete:\n")
            gpm_list = self.get_gpm_list()
            menu = Menu()
            gpm_names = [x for x in gpm_list.keys()]
            gpm_names.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
            gpm_name = menu.draw_menu(gpm_names)
            input()
            if gpm_name == str(BackButton.BACK.name):
                return
            self.gpm_id = gpm_list.pop(gpm_name)
            os.system('clear')
            print('choose another gpm to assign current gpm members:\n')
            menu2 = Menu()
            if len(gpm_list.keys()) == 0:
                print(Color.F_Red+"Can't delete GPM because you don't have any alternative GPM "+Base.END)
                return
            alternative_gpm_names = [x for x in gpm_list.keys()]
            alternative_gpm_names.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
            alternative_gpm_name = menu2.draw_menu(alternative_gpm_names)
            input()
            if alternative_gpm_name == str(BackButton.BACK.name):
                return
            # assigning new gpm to members
            self.conn.update_member_gpm(gpm_list[alternative_gpm_name], self.gpm_id)
            # completing all gpm projects
            project_ids = self.conn.get_gpm_projects(self.gpm_id)
            for project_id in project_ids:
                self.project_id = project_id[0]
                member_ids = self.conn.get_project_members(self.project_id)
                for member_id in member_ids:
                    self.member_id = member_id[0]
                    self.delete_project_members()
            self.conn.update_user('is_deleted', self.gpm_id, 'True')
            self.conn.commit_data()
        except Exception as e:
            print(e)
            self.conn.rollback_data()

    def update_gpm(self):
        """
          this method is used to update gpm for current bdo.
        """
        try:
            gpm_list = self.get_gpm_list()
            menu = Menu()
            gpm_names = [x for x in gpm_list.keys()]
            gpm_names.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
            gpm_name = menu.draw_menu(gpm_names)
            input()
            if str(BackButton.BACK.name) == gpm_name:
                return
            gpm_id = gpm_list[gpm_name]
            print("select the field to update: \n")
            menu = Menu()
            details = [x.name for x in GpmUpdateFields]
            details.extend([str(BackButton.EXIT.name)])
            field = menu.draw_menu(details)
            input()
            user_input = input("enter new value for " + str(field)+" ")
            user_table_fields = [1, 2, 3]
            # validating field
            if field == str(GpmUpdateFields.PASSWORD.name):
                if not Validation.password(user_input):
                    print("password is weak")
                    input()
                    return
                user_input = encrypt_pass(user_input)
            if field == str(GpmUpdateFields.AGE.name):
                if not Validation.age(user_input):
                    print("age is not valid")
                    input()
                    return
            if field == str(GpmUpdateFields.PINCODE.name):
                if not Validation.pincode(user_input):
                    print("pincode is not valid")
                    input()
                    return
            if field == str(GpmUpdateFields.GENDER.name):
                if not Validation.gender(user_input):
                    print("gender is not valid")
                    input()
                    return

            query = ""
            # if field belong to user table
            if user_table_fields.count(GpmUpdateFields[field].value) == 1:
                self.conn.update_user(str(field), gpm_id, user_input)
            else:
                self.conn.update_personal_details(str(field), gpm_id, user_input)
            self.conn.commit_data()
            print("\n" + Color.F_Green + "record updated" + Base.END)
        except Exception as e:
            print(e)
            self.conn.rollback_data()

    def get_gpm_list(self):
        """
          this method is used to get gpm for current bdo.
        :return: dict, gpm name and id dictionary.
        """
        result = self.conn.get_user_names(self.bdo_id)
        gpm_dict = {}
        for data in result:
            gpm_dict[data[0]] = data[1]
        return gpm_dict

    def create_project(self):
        """
          this method is used to create project for current bdo.
        """
        try:
            print("choose gpm for project\n")
            gpm_list = self.get_gpm_list()
            menu = Menu()
            gpm_names = [x for x in gpm_list.keys()]
            gpm_names.extend([str(BackButton.EXIT.name)])
            gpm_name = menu.draw_menu(gpm_names)
            input()
            gpm_id = gpm_list[gpm_name]

            print("choose project type:\n")
            menu2 = Menu()
            project_types = [x.name for x in ProjectType]
            project_types.extend([str(BackButton.EXIT.name)])
            project_type = menu2.draw_menu(project_types)
            input()

            project_id = str(uuid.uuid4())
            project_name = input("enter project name: ")
            labours = input("enter expected labours:  ")
            if not Validation.is_int(labours):
                print("labours count is not valid")
                input()
                return
            cost = input("enter estimated project cost: ")
            if not Validation.is_int(cost):
                print("cost is not valid")
                input()
                return
            area = input("enter estimated project area: ")
            if not Validation.is_int(area):
                print("area is not valid")
                input()
                return
            start_date = input("enter estimated start date: ")
            if not Validation.start_date(start_date):
                print("start date is not valid")
                input()
                return
            end_date = input("enter estimated end date: ")
            if not Validation.end_date(start_date, end_date):
                print("end date is not valid")
                input()
                return
            is_deleted = 'False'
            created_by = self.bdo_id
            self.conn.create_project(project_id, project_name, labours, cost, area, start_date, end_date,gpm_id,
                                     created_by, project_type, is_deleted)
            self.conn.commit_data()
            print("\n"+Color.F_Green + "project created"+Base.END)
        except Exception as e:
            print(e)
            self.conn.rollback_data()

    def update_project(self):
        """
          this method is used to update project for current bdo.
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

        print("select the field to update: \n")
        menu2 = Menu()
        details = [x.name for x in ProjectsUpdateFields]
        details.extend([str(BackButton.EXIT.name)])
        field = menu2.draw_menu(details)
        input()
        user_input = ""
        if ProjectsUpdateFields[field].value == ProjectsUpdateFields.PROJECT_TYPE.value:
            print("choose project type: \n")
            menu3 = Menu()
            project_types = [x.name for x in ProjectType]
            project_types.extend([str(BackButton.EXIT.name)])
            user_input = menu3.draw_menu(project_types)
            input()
        else:
            user_input = input("enter new value for " + str(field)+" ")
            # validations
            if field == str(ProjectsUpdateFields.AREA_OF_PROJECT.name):
                if not Validation.is_int(user_input):
                    print("area is not valid")
                    input()
                    return
            if field == str(ProjectsUpdateFields.TOTAL_LABOUR_REQUIRED.name):
                if not Validation.is_int(user_input):
                    print("labour required is not valid")
                    input()
                    return

            if field == str(ProjectsUpdateFields.ESTIMATED_START_DATE.name):
                if not Validation.start_date(user_input):
                    print("start date is not valid")
                    input()
                    return
            if field == str(ProjectsUpdateFields.ESTIMATED_END_DATE.name):
                start_date = self.conn.get_project_start_date(project_id)
                if not Validation.end_date(start_date, user_input):
                    print("end date is not valid")
                    input()
                    return
            if field == str(ProjectsUpdateFields.ESTIMATED_COST.name):
                if not Validation.is_int(user_input):
                    print("cost is not valid")
                    input()
                    return
        self.conn.update_project(field, user_input, project_id)
        self.conn.commit_data()
        print("\n" + Color.F_Green + "record updated" + Base.END)

    def delete_project(self):
        """
          this method is used to delete project for current bdo.
        """
        print("choose project")
        project_list = self.get_project_list()
        menu = Menu()
        project_names = [x for x in project_list.keys()]
        project_names.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
        project_name = menu.draw_menu(project_names)
        input()
        if project_name == str(BackButton.BACK.name):
            return
        project_id = project_list[project_name]
        self.project_id = project_id
        self.project_deletion()
        print(Color.F_Green+"project deleted successfully "+Base.END)

    def show_projects(self):
        """
          this method is used to print projects for current bdo.
        """
        result = self.conn.get_bdo_project_details(self.bdo_id)
        raw_data_to_table(result.fetchall(), result)

    def get_project_list(self):
        """
          this method is used to get projects list for current bdo.
        :return: dict, project name and id dictionary.
        """
        result = self.conn.get_bdo_project_names(self.bdo_id)
        gpm_dict = {}
        for data in result:
            gpm_dict[data[0]] = data[1]
        return gpm_dict

    def show_requests(self):
        """
          this method is used to show and resolve all requests for current bdo.
        """
        try:
            projects = self.conn.get_requests(self.bdo_id)
            # adding index column to given result
            projects_fields = (('index'),) + projects.description
            result = projects.fetchall()
            counter = 0
            # request is empty then returning early with a message
            if len(result) == 0:
                print(Color.F_Red+"there is no pending request"+Base.END)
                return

            print("write index of request to manage:\n")
            temp = result
            # converting list of tuples into list of list
            temp = [list(elem) for elem in temp]
            for request in temp:
                if str(RequestType.APPROVAL.name) == str(request[0]):
                    temp2 = str(request[2]).split('|')
                    request[2] = temp2[0] + " request for " + temp2[4] + " project for " + temp2[1] + " member"
                # inserting data for index column
                request.insert(0, counter)
                counter += 1
            table = PrettyTable()
            # assigning field names to pretty table object and removing request id column
            table.field_names = [column[0] for column in projects_fields[:-1]]
            for row in temp:
                # removing request id from temp list and adding to table row
                table.add_row(row[:-1])
            print(table)
            row_number = input("enter index number: ")
            if not Validation.is_int(row_number):
                print("index number is not valid")
                input()
                return
            menu = Menu()
            result_names = [x.name for x in RequestResult]
            result_names.extend([str(BackButton.EXIT.name)])
            result_name = menu.draw_menu(result_names)
            input()
            status = "NULL"
            if str(RequestType.APPROVAL.name) == str(result[int(row_number)][0]):
                temp = str(result[int(row_number)][2]).split('|')
                req_type = str(temp[0])
                self.project_id = str(temp[3])
                self.member_id = str(temp[2])
                if req_type == str(ApprovalType.WAGE.name) and str(result_name) == str(RequestResult.APPROVED.name):
                    self.delete_project_members()
                    status = "'True'"
                elif req_type == str(ApprovalType.MEMBER.name) and str(result_name) == str(RequestResult.APPROVED.name):
                    project_members_id = self.conn.get_project_members(self.project_id)
                    members_required = self.conn.get_project_members_required(self.project_id)
                    # checking if total number of members in given project are less then actual project requirement
                    if int(members_required[0]) <= int(len(project_members_id)):
                        print(Color.F_Red + "project members limit exceeded can't accept request" + Base.END)
                        return
                    self.conn.assign_project_members(self.project_id, self.member_id)
                    status = "'True'"
                elif str(result_name) == str(RequestResult.REJECTED.name):
                    status = "'False'"
            else:
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

    def delete_project_members(self):
        """
          this method is used to delete project members for current bdo.
        """
        result = self.conn.get_members_assigned_project(self.member_id)
        if result is None:
            return
        # removing member from project
        duration = datetime.datetime.now() - datetime.datetime.strptime(str(result[2]), '%Y-%m-%d')
        wage = duration.days * 100
        self.conn.register_project_completion(result[0], self.member_id, result[2], datetime.datetime.now().date(), wage)
        self.conn.remove_project_member(self.member_id)
        # checking if other members are assigned to this project
        result2 = self.conn.find_project_is_assigned(result[0])
        # deleting whole project
        if len(result2) == 0:
            self.conn.update_project('is_deleted', 'True', result[0])

    def project_deletion(self):
        """
          this method is used to delete project for current bdo.
        """
        try:
            result = self.conn.get_project_members_list(self.project_id)
            if len(result) != 0:
                for project_member in result:
                    duration = datetime.datetime.now() - datetime.datetime.strptime(str(project_member[2]), '%Y-%m-%d')
                    wage = duration.days * 100
                    self.conn.register_project_completion(project_member[0], project_member[1], project_member[2],
                                                          datetime.datetime.now().date(), wage)

                self.conn.remove_project_all_members(self.project_id)
            self.conn.update_project('is_deleted', 'True', self.project_id)
            # removing project pending requests
            pending_requests = self.conn.get_bdo_approvals_list(self.bdo_id)
            pending_requests_ids = []
            for request in pending_requests:
                temp = str(request[1]).split('|')
                if str(temp[3]) == str(self.project_id):
                    pending_requests_ids.append(request[0])
            for pending_requests_id in pending_requests_ids:
                self.conn.resolve_request("'True'", pending_requests_id)
            self.conn.commit_data()
        except Exception as e:
            print(e)
            self.conn.rollback_data()

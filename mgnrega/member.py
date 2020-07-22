""" this file is used to perform member related operations."""

from common.constants import MemberFeatures, Base, Color, ComplainRecipients, RequestType, BackButton
from common.helper import Menu
from common.password_encryption import decrypt_pass
from future.builtins import input
from common.connect_db import ConnectDb
import sys
import datetime
import sqlite3
import os


class Member:
    """this is a class for member related operations.
            Attributes:
                conn (sqlite connection): connection object.
                member_id (string): member id.
        """
    def __init__(self):
        """
              initializing BDO class .
        """
        self.conn = ConnectDb()
        self.member_id = ""

    def __del__(self):
        """
           closing database connection.
        """
        self.conn.close_conn()

    def member_features(self):
        """
            this method is used to print all bdo features on console.
        """
        try:

            print("choose feature :\n")
            menu = Menu()
            features = [x.name for x in MemberFeatures]
            features.extend([str(BackButton.EXIT.name)])
            feature = menu.draw_menu(features)
            input()
            required_feature = getattr(self, feature.lower())
            required_feature()
            # calling member features again
            input()
            os.system('clear')
            self.member_features()

        except Exception as e:
            print(e)
            sys.exit()

    def view_details(self):
        """
            this method is used to print member details on console.
        """
        member_details = self.conn.get_member_details(self.member_id)
        if member_details is None:
            print("you are not longer part of this system")
            input()
            sys.exit()
        project_details = self.conn.get_member_project(self.member_id)
        password = decrypt_pass(member_details[1])
        # printing personal details
        print(Base.BOLD+"Personal Details"+Base.END+"\n")
        print("Name: " + Color.F_Green + member_details[4] + Base.END)
        print("Password: " + Color.F_Green + password + Base.END)
        print("User name: " + Color.F_Green + member_details[2] + Base.END)
        print("Created at: " + Color.F_Green + member_details[3] + Base.END)
        print("State: " + Color.F_Green + member_details[5] + Base.END)
        print("District: " + Color.F_Green + member_details[6] + Base.END)
        print("Pincode: " + Color.F_Green + str(member_details[7]) + Base.END)
        print("Age: " + Color.F_Green + str(member_details[8]) + Base.END)
        print("Gender: " + Color.F_Green + member_details[9] + Base.END)
        print("Assigned Gram Panchayat Member: " + Color.F_Green + member_details[10] + Base.END+"\n")

        # printing member project details
        print(Base.BOLD + "Project Details" + Base.END + "\n")
        if project_details is None:
            print(Color.F_Red+"you are not assigned to any project\n"+Base.END)
        else:
            duration = datetime.datetime.now() - datetime.datetime.strptime(str(project_details[0]), '%Y-%m-%d')
            wage = duration.days * 100
            print("Project Name: "+Color.F_Green+project_details[1]+Base.END)
            print("assigned Date: "+Color.F_Green+project_details[0]+Base.END)
            print("Project Type: "+Color.F_Green+project_details[2]+Base.END)
            print("Total working days: "+Color.F_Green+str(duration)+Base.END)
            print("Total wage: "+Color.F_Green+str(wage)+Base.END)

    def file_complain(self):
        """
          this method is used to file complain for current member to bdo/gpm.
        """
        try:
            print("Choose a complain recipient:\n")
            menu = Menu()
            recipients = [x.name for x in ComplainRecipients]
            recipients.extend([str(BackButton.EXIT.name), str(BackButton.BACK.name)])
            recipient = menu.draw_menu(recipients)
            input()
            if str(BackButton.BACK.name) == recipient:
                return
            member_details = self.conn.get_bdo_gpm_for_member(self.member_id)
            if member_details is None:
                print("you don't have any manager to file complain")
                return
            recipient_id = ""
            if recipient == str(ComplainRecipients.BDO.name):
                recipient_id = member_details[2]
            elif recipient == str(ComplainRecipients.GPM.name):
                recipient_id = member_details[1]
            else:
                print(Color.F_Red+"Invalid option"+Base.END)
                return
            request_msg = input("enter your request: ")
            self.conn.register_complain(str(RequestType.ISSUES.name), self.member_id, request_msg, recipient_id)
            self.conn.commit_data()
            print(Color.F_Green+"Request sent to "+recipient+Base.END)
        except sqlite3.Error as e:
            print(e)
            self.conn.rollback_data()






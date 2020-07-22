""" this file is used to perform login related operations."""

from common.constants import Role, Color, Base, BackButton
from common.helper import Menu
from common.connect_db import ConnectDb
from future.builtins import input
from mgnrega.bdo import BDO
from mgnrega.gpm import GPM
from mgnrega.member import Member
from getpass import getpass
from common.password_encryption import decrypt_pass
import os
import sys


def main():
    """
    this method is used to call main menu for login
    """
    conn = ConnectDb()
    try:
        os.system('clear')
        # select role for login
        print("login as:\n")
        menu = Menu()
        roles = [x.name for x in Role]
        roles.extend([str(BackButton.EXIT.name)])
        role = menu.draw_menu(roles)
        role_id = Role[role].value
        input()

        # get user name and password for login
        user_name = input("enter user name: ")
        password = getpass()

        # check user authentication
        result = conn.get_user_with_role(user_name, role_id)
        flag = True
        if result is not None:
            os.system('clear')
            actual_pass = decrypt_pass(result[1])
            if str(actual_pass.decode("utf-8")) == password:
                flag = False
                if role_id == int(Role.BDO.value):
                    bdo = BDO()
                    bdo.bdo_id = result[0]
                    bdo.bdo_features()
                elif role_id == int(Role.GPM.value):
                    gpm = GPM()
                    gpm.gpm_id = result[0]
                    gpm.gpm_features()
                elif role_id == int(Role.Member.value):
                    member = Member()
                    member.member_id = result[0]
                    member.member_features()
        if result is None or flag:
            print(Color.F_Red + 'wrong credentials' + Base.END)
            input()
            main()

    except Exception as e:
        print(e)
        sys.exit()
    finally:
        conn.close_conn()


# only executes when login file run as main script or run directly from terminal
if __name__ == '__main__':
    """
    creating db schema and calling main function
    """
    con = ConnectDb()
    con.db_script()
    main()








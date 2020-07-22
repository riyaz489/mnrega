""" this class is used to provide input validation"""
import datetime
import re


class Validation:

    @staticmethod
    def age(user_input):
        try:
            temp = int(user_input)
            if temp > 150 or temp < 18:
                return False
            return True
        except:
            return False

    @staticmethod
    def pincode(user_input):
        try:
            temp = int(user_input)
            if temp < 0:
                return False
            if len(str(temp)) == 6:
                return True
            return False
        except:
            return False

    @staticmethod
    def is_int(user_input):
        try:
            temp = int(user_input)
            if temp < 0:
                return False
            return True
        except:
            return False

    @staticmethod
    def gender(user_input):
        return str(user_input) == 'M' or str(user_input) == 'F'

    @staticmethod
    def start_date(user_input):
        try:
            input_date = datetime.datetime.strptime(user_input, '%Y-%m-%d')
            return (datetime.datetime.now() - input_date).days <= 0
        except:
            return False

    @staticmethod
    def end_date(input_start_date, input_end_date):
        try:
            start_date = datetime.datetime.strptime(input_start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(input_end_date, '%Y-%m-%d')
            return (start_date - end_date).days <= 0
        except:
            return False

    @staticmethod
    def password(password):

        if len(password) < 8:
            return False
        elif not re.search("[a-z]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not re.search("[_@$]", password):
            return False
        elif re.search("\s", password):
            return False
        else:
            return True



import unittest
from common.validations import Validation
import datetime


class ValidationTest(unittest.TestCase):

    def test_age(self):
        inputs = ['45', '200', 'invalid_age']
        self.assertEqual(True, Validation.age(inputs[0]))
        self.assertEqual(False, Validation.age(inputs[1]))
        self.assertEqual(False, Validation.age(inputs[2]))

    def test_pincode(self):
        inputs = ['452323', '2020', 'invalid_piincode', '-23234']
        self.assertEqual(True, Validation.pincode(inputs[0]))
        self.assertEqual(False, Validation.pincode(inputs[1]))
        self.assertEqual(False, Validation.pincode(inputs[2]))
        self.assertEqual(False, Validation.pincode(inputs[3]))

    def test_is_int(self):
        inputs = ['2020', 'invalid_int', '-34']
        self.assertEqual(True, Validation.is_int(inputs[0]))
        self.assertEqual(False, Validation.is_int(inputs[1]))
        self.assertEqual(False, Validation.is_int(inputs[2]))

    def test_gender(self):
        inputs = ['M', 'F', 'invalid_gender']
        self.assertEqual(True, Validation.gender(inputs[0]))
        self.assertEqual(True, Validation.gender(inputs[1]))
        self.assertEqual(False, Validation.gender(inputs[2]))

    def test_start_date(self):
        inputs = [str(datetime.datetime.now().date()), '2000-01-01', '3421-14-23', 'invalid_date']
        self.assertEqual(True, Validation.start_date(inputs[0]))
        self.assertEqual(False, Validation.start_date(inputs[1]))
        self.assertEqual(False, Validation.start_date(inputs[2]))
        self.assertEqual(False, Validation.start_date(inputs[3]))

    def test_end_date(self):
        start_inputs = ['2020-01-01', '2020-03-01', '2020-01-01', '3421-14-23', 'invalid_date']
        end_inputs = ['2020-03-01', '2020-01-01', '2020-13-01', '2020-03-01', 'invalid_date']
        self.assertEqual(True, Validation.end_date(start_inputs[0], end_inputs[0]))
        self.assertEqual(False, Validation.end_date(start_inputs[1], end_inputs[1]))
        self.assertEqual(False, Validation.end_date(start_inputs[2], end_inputs[2]))
        self.assertEqual(False, Validation.end_date(start_inputs[3], end_inputs[3]))
        self.assertEqual(False, Validation.end_date(start_inputs[4], end_inputs[4]))

    def test_password(self):
        inputs = ['Monty@123sgahRma', '1231', 'invalid_pass', '@#$%^^', 'ASDFDFGDG', 'sdf sdSASf', 'asASASAS',
                  'ASasd123213', 'Monty@123sgahRma asd']
        self.assertEqual(True, Validation.password(inputs[0]))
        self.assertEqual(False, Validation.password(inputs[1]))
        self.assertEqual(False, Validation.password(inputs[2]))
        self.assertEqual(False, Validation.password(inputs[3]))
        self.assertEqual(False, Validation.password(inputs[4]))
        self.assertEqual(False, Validation.password(inputs[5]))
        self.assertEqual(False, Validation.password(inputs[6]))
        self.assertEqual(False, Validation.password(inputs[7]))
        self.assertEqual(False, Validation.password(inputs[8]))


if __name__ == '__main__':
    unittest.main()

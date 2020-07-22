import unittest
import mock
from pynput.keyboard import Key
from common.helper import raw_data_to_table, Menu, always_true

class HelperTest(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('common.helper.PrettyTable')
    @mock.patch('common.connect_db.sqlite3.connect')
    def test_raw_data_to_table(self, mock_cursor, mock_table, mock_print):
        raw_data = [[1, 2], [3, 4]]
        mock_cursor.cursor().description.return_value = ['a', 'b']
        raw_data_to_table(raw_data, mock_cursor.cursor)
        self.assertEqual(mock_table().add_row.call_count, 2)
        mock_print.assert_called_once()

    def test_always_true(self):
        self.assertEqual(always_true(), True)

    def test_on_press_up(self):
        mock_press_key = mock.Mock()
        mock_press_key.name = 'up'
        menu = Menu()
        menu.count = 3
        menu.on_press(mock_press_key)
        self.assertEqual(menu.index, 3)
        menu.on_press(mock_press_key)
        self.assertEqual(menu.index, 2)

    def test_on_press_down(self):
        mock_press_key = mock.Mock()
        mock_press_key.name = 'down'
        menu = Menu()
        menu.count = 3
        menu.index = 3
        self.assertEqual(menu.on_press(mock_press_key), False)
        self.assertEqual(menu.index, 0)
        menu.on_press(mock_press_key)
        self.assertEqual(menu.index, 1)

    @mock.patch('common.helper.Key')
    def test_on_press_enter(self, mock_key):
        mock_press_key = mock_key.enter
        menu = Menu()
        menu.count = 3
        self.assertEqual(menu.on_press(mock_press_key), False)
        self.assertEqual(menu.flag, 1)

    @mock.patch('common.helper.Key')
    def test_on_press_exception(self, mock_key):
        mock_press_key = Exception
        menu = Menu()
        self.assertEqual(menu.on_press(mock_press_key), False)

    @mock.patch('common.helper.Listener')
    def test_draw_menu(self, mock_listener):
        menu = Menu()
        items = ['first', 'second', 'EXIT']
        menu.index = 1
        menu.flag = 1
        result = menu.draw_menu(items)
        self.assertEqual(result, items[1])

    @mock.patch('builtins.print')
    @mock.patch('common.helper.Listener')
    def test_draw_menu_exit(self, mock_listener, mock_print):
        menu = Menu()
        items = ['first', 'second', 'EXIT']
        menu.index = 2
        menu.flag = 1
        self.assertRaises(SystemExit, menu.draw_menu, items)
        mock_print.assert_called_once_with('exiting from system')

    @mock.patch('common.helper.always_true')
    @mock.patch('common.helper.os')
    @mock.patch('builtins.print')
    @mock.patch('common.helper.Listener')
    def test_draw_menu_print(self, mock_listener, mock_print, mock_os, mock_always_true):
        mock_always_true.return_value = False
        menu = Menu()
        items = ['first', 'second', 'EXIT']
        menu.index = 1
        menu.flag = 0
        menu.draw_menu(items)

        self.assertEqual(mock_print.call_count, 3)
        mock_listener.assert_called_once()
        mock_os.system.assert_called_once_with('clear')


if __name__ == '__main__':
    unittest.main()

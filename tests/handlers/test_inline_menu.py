from unittest.mock import MagicMock, PropertyMock

from telegram import InlineKeyboardButton

from app.handlers import inline_menu
from tests.base import BaseTestCase


class TestInlineMenu(BaseTestCase):
    def test_callback_data(self):
        update = MagicMock()
        type(update.callback_query).data = PropertyMock(return_value='123 1 False What?')
        self.assertEqual(('1', 'False', 'What?'), inline_menu.callback_data(update))

    def test_close_button(self):
        menu = inline_menu.InlineMenu([[('manual_close', ['cancel', 'test', 'what?'])]], 'close_button')
        self.assertEqual(['0 test what?', '0'], [x[0].callback_data for x in menu.inline_keyboard])
        self.assertEqual([[InlineKeyboardButton('manual_close', callback_data='0 test what')],
                          [InlineKeyboardButton('close_button', callback_data='0')]], menu.inline_keyboard)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import unittest
from dotenv import load_dotenv

from telegram import Bot


class TestTelegramBot(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        load_dotenv()
        token = os.getenv("TOKEN", "")
        self.chat_id = os.getenv("CHAT_ID")
        update_offset = 0
        update_timeout = 0

        self.bot = Bot(token, update_offset, update_timeout)

    async def test_get_me(self):
        response = await self.bot.get_me()
        self.assertIsNotNone(response)

    async def test_get_updates(self):
        response = await self.bot.get_updates()
        self.assertIsNotNone(response)

    async def test_send_message(self):
        text = "Este es un mensaje de prueba"
        response = await self.bot.send_message(text, self.chat_id)
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()

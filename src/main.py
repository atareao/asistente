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

import asyncio
import logging
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot


async def main(token, chat_id):
    bot = Bot(token)
    logging.debug(await bot.get_me())
    msg = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    logging.debug(await bot.send_message(msg, chat_id))
    msg = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
    logging.debug(await bot.send_message(msg, chat_id))
    while True:
        response = await bot.get_updates()
        if response["ok"] and response["result"]:
            for item in response["result"]:
                if "message" in item:
                    username = item["message"]["from"]["username"]
                    if re.match("^/hora", item["message"]["text"]):
                        hora = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")
                        msg = f"{username}, son las {hora}"
                        logging.debug(await bot.send_message(msg, chat_id))


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TOKEN")
    chat_id = os.getenv("CHAT_ID")
    log_level = logging.getLevelName(os.getenv("LOG_LEVEL", "DEBUG"))
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s: %(message)s"
    )
    asyncio.run(main(token, chat_id))

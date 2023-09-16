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

import aiohttp
import logging

logger = logging.getLogger(__name__)


class Bot:
    """A Telegram Bot"""

    def __init__(self, token: str, update_offset: int = 0,
                 update_timeout: int = 60) -> None:
        """Init the bot

        Parameters
        ----------
        token : str
            Token of the bot
        update_offset : int
            First uptate to get
        update_timeout : int
            Timeout between calls
        """
        logger.debug("__init__")
        self._url = f"https://api.telegram.org/bot{token}"
        self._update_offset = update_offset
        self._update_timeout = update_timeout

    async def get_me(self) -> dict:
        """Get info about the bot

        Returns
        -------
        dict
            Info about the bot
        """
        logger.info("get_me")
        return await self._get("getMe")

    async def get_updates(self) -> dict:
        """Get updates

        Returns
        -------
        dict
            Updates
        """
        logger.info("get_updates")
        params = {
            "offset": self._update_offset,
            "timeout": self._update_timeout
        }
        return await self._get("getUpdates", params)

    async def send_message(self, text: str, chat_id: int,
                           thread_id: int = 0) -> dict:
        """Send a message

        Parameters
        ----------
        text : str
            The message
        chat_id : int
            The chat_it
        thread_id : int
            The thread_id if any

        Returns
        -------
        dict
            The response
        """
        logger.info("send_message")
        data = {
            "chat_id": chat_id,
            "text": text
        }
        if thread_id > 0:
            data.update({"message_thread_id": thread_id})
        return await self._post("sendMessage", data)

    async def _get(self, endpoint: str, params: dict = {}) -> dict:
        """Send a generic GET

        Parameters
        ----------
        endpoint : str
            The endpoint
        params : dict
            Params for the query

        Returns
        -------
        dict
            Response from Telegram
        """
        logger.info("_get")
        logger.debug(f"endpoint: {endpoint}")
        logger.debug(f"params: {params}")
        async with aiohttp.ClientSession() as session:
            url = f"{self._url}/{endpoint}"
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    content = await response.text()
                    msg = f"Error HTTP {response.status}. {content}"
                    raise Exception(msg)
                response = await response.json()
                logging.debug(f"Response: {response}")
                return response

    async def _post(self, endpoint: str, data: dict = {}) -> dict:
        """Send a generic POST

        Parameters
        ----------
        endpoint : str
            The endpoint
        data : dict
            Data to send

        Returns
        -------
        dict
            Response from Telegram
        """
        logger.info("_post")
        logger.debug(f"endpoint: {endpoint}")
        logger.debug(f"data: {data}")
        async with aiohttp.ClientSession() as session:
            url = f"{self._url}/{endpoint}"
            async with session.post(url, json=data) as response:
                if response.status != 200:
                    content = await response.text()
                    msg = f"Error HTTP {response.status}. {content}"
                    raise Exception(msg)
                response = await response.json()
                logging.debug(f"Response: {response}")
                return response

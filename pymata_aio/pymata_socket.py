# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 Alan Yorinks All rights reserved.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

import asyncio


# noinspection PyStatementEffect,PyUnresolvedReferences,PyUnresolvedReferences
class PymataSocket:
    def __init__(self, ip_address, port, loop):
        self.ip_address = ip_address
        self.port = port
        self.loop = loop
        self.reader = None
        self.writer = None

    async def start(self):
        """
        This method opens an IP connection on the IP device

        :return: None
        """
        self.reader, self.writer = await asyncio.open_connection(
            self.ip_address, self.port, loop=self.loop)

    async def write(self, data):
        """
        This method writes sends data to the IP device
        :param data:

        :return: None
        """
        self.writer.write((bytes([ord(data)])))
        await self.writer.drain()

    async def read(self):
        """
        This method reads one byte of data from IP device

        :return: Next byte
        """
        buffer = await self.reader.read(1)
        return ord(buffer)

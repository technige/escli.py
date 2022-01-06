#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Nigel Small
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from escli.commands import Command


class IndexCreateCommand(Command):
    """ Create an index.
    """

    def get_name(self):
        return "mk"

    def get_description(self):
        return self.__doc__.strip()

    def register(self, subparsers):
        parser = subparsers.add_parser(self.get_name(), description=self.get_description())
        parser.add_argument("name", metavar="NAME",
                            help="Name of new index to add.")
        parser.set_defaults(f=lambda args: self.spi.client.create_index(args.name))
        return parser


class IndexDeleteCommand(Command):
    """ Delete an index.
    """

    def get_name(self):
        return "rm"

    def get_description(self):
        return self.__doc__.strip()

    def register(self, subparsers):
        parser = subparsers.add_parser(self.get_name(), description=self.get_description())
        parser.add_argument("name", metavar="NAME",
                            help="Name of index to delete.")
        parser.set_defaults(f=lambda args: self.spi.client.delete_index(args.name))
        return parser


class IndexListCommand(Command):
    """ List available indexes.
    """

    def get_name(self):
        return "ls"

    def get_description(self):
        return self.__doc__.strip()

    def register(self, subparsers):
        parser = subparsers.add_parser(self.get_name(), description=self.get_description())
        parser.add_argument("-a", "--all", action="store_true",
                            help="List all indexes, including those starting with '.'.")
        parser.set_defaults(f=self.print_indexes)
        return parser

    def print_indexes(self, args):
        """
        """
        for index in self.spi.client.get_indexes(include_all=args.all):
            print(index)

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


from csv import reader
from json import dumps as json_dumps

from escli.commands import Command


class JsonifyCommand(Command):
    """ Convert input data to JSON documents.
    """

    def get_name(self):
        return "jsonify"

    def get_description(self):
        return self.__doc__.strip()

    def register(self, subparsers):
        parser = subparsers.add_parser(self.get_name(), description=self.get_description())
        parser.add_argument("file", metavar="FILE",
                            help="Filename from which to load data.")
        parser.add_argument("-i", "--include", default="*",
                            help="Fields to include (comma-separated list).")
        parser.set_defaults(f=self.jsonify)
        return parser

    def jsonify(self, args):
        """ Convert input data to JSON documents.
        """
        with open(args.file, newline="") as csv_file:
            csv_reader = reader(csv_file)
            keys = None
            for line_no, line in enumerate(csv_reader):
                if line_no == 0:
                    keys = line
                    if args.include == "" or args.include == "*":
                        include_keys = None
                    else:
                        include_keys = args.include.split(",")
                else:
                    values = list(map(simplify_type, line))
                    data = dict(zip(keys, values))
                    if include_keys:
                        data = dict(zip(include_keys, [data[k] for k in include_keys]))
                    print(json_dumps(data))


def simplify_type(value):
    try:
        int_value = int(value)
    except ValueError:
        try:
            float_value = float(value)
        except ValueError:
            return value
        else:
            return float_value
    else:
        return int_value

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


from tabulate import tabulate

from escli.commands import Command


class SearchCommand(Command):
    """ Search an index.
    """

    def __init__(self, client):
        super().__init__()
        self.client = client

    def add_parser(self, subparsers):
        parser = subparsers.add_parser("search", description=SearchCommand.__doc__)
        parser.add_argument("index", help="Target index to search. Multiple index names can be provided "
                                          "as a comma-separated list, or use '*' to search all indices.")
        parser.add_argument("-f", "--format", help="Output table format", default="simple")
        parser.add_argument("-i", "--include", help="Source fields to include in matching documents", default="*")
        parser.add_argument("-n", "--size", type=int, default=10)
        parser.add_argument("-s", "--sort")
        parser.set_defaults(f=self.execute)
        return parser

    def execute(self, args):
        res = self.client.search(index=args.index, _source_includes=args.include, size=args.size, sort=args.sort,
                                 query={"match_all": {}})
        print("Got %d Hits:" % res['hits']['total']['value'])
        print(tabulate([hit["_source"] for hit in res['hits']['hits']], headers="keys", tablefmt=args.format))

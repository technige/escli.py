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
from escli.writer import print_data


class SearchCommand(Command):
    """ Perform a search query against an index.

    By default, this is a 'match_all' query, although other more
    specialised query types are also available, such as 'match'
    and 'term'.
    """

    def attach(self, subparsers):
        parser = subparsers.add_parser("search", description=SearchCommand.__doc__)
        parser.add_argument("index", metavar="INDEX",
                            help="Target index to search. Multiple index names can be provided "
                                 "as a comma-separated list, or use '*' to search all indices.")
        parser.add_argument("pattern", metavar="FIELD=VALUE", nargs="?", default=None,
                            help="Pattern to match in the form 'FIELD=VALUE'.")
        parser.add_argument("-f", "--format", default="simple",
                            help="Output table format")
        parser.add_argument("-i", "--include", default="*",
                            help="Source fields to include in matching documents")
        parser.add_argument("-n", "--size", type=int, default=10)
        parser.add_argument("-s", "--sort")
        parser.set_defaults(f=self.search)
        return parser

    def search(self, args):
        """ Execute the search query and retrieve and display the results.
        """
        if args.pattern:
            field, _, value = args.pattern.partition("=")
            criteria = (field, value)
        else:
            criteria = None
        hits = self.spi.client.search(args.index, criteria,
                                      include=args.include, size=args.size, sort=args.sort)
        print_data(hits, args.format)

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
    """ Perform a search query against a repository.
    """

    def attach(self, subparsers):
        parser = subparsers.add_parser("search", description=SearchCommand.__doc__)
        parser.add_argument("repo", metavar="REPO",
                            help="Target repository to search. For Elasticsearch, this will be an index name; "
                                 "for Enterprise Search, this will be an engine name.")
        parser.add_argument("query", metavar="QUERY", nargs="?", default=None,
                            help="Search query. For Elasticsearch, this should be in the form 'FIELD=VALUE'.")
        parser.add_argument("-f", "--format", default="simple",
                            help="Output table format")
        parser.add_argument("-i", "--include", default=None,
                            help="Fields to include in matching documents.")
        parser.add_argument("-s", "--sort",
                            help="Field to sort by. Prefixing the field name with '~' will sort in reverse order.")
        parser.add_argument("-n", "--page-size", type=int, default=10,
                            help="Number of results per page.")
        parser.add_argument("-p", "--page-number", type=int, default=1,
                            help="Page number to return.")
        parser.set_defaults(f=self.search)
        return parser

    def search(self, args):
        """ Execute the search query and retrieve and display the results.
        """
        hits = self.spi.client.search(args.repo, args.query, fields=args.include,
                                      sort=args.sort, page_size=args.page_size, page_number=args.page_number)
        print_data(hits, args.format)

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


class SearchQuery(Command):
    """ Perform a search query against an index.

    By default, this is a 'match_all' query, although other more
    specialised query types are also available, such as 'match'
    and 'term'.
    """

    def __init__(self, client):
        super().__init__()
        self.client = client

    def attach(self, subparsers):
        parser = subparsers.add_parser("search", description=SearchQuery.__doc__)
        parser.add_argument("index", metavar="INDEX",
                            help="Target index to search. Multiple index names can be provided "
                                 "as a comma-separated list, or use '*' to search all indices.")
        parser.add_argument("-f", "--format", default="simple",
                            help="Output table format")
        parser.add_argument("-i", "--include", default="*",
                            help="Source fields to include in matching documents")
        parser.add_argument("-n", "--size", type=int, default=10)
        parser.add_argument("-s", "--sort")
        parser.set_defaults(f=self.execute)
        search_subparsers = parser.add_subparsers()
        MatchSearchQuery(self.client).attach(search_subparsers)
        TermSearchQuery(self.client).attach(search_subparsers)
        return parser

    def execute(self, args):
        """ Execute the search query and retrieve and display the results.
        """
        res = self.client.search(index=args.index, _source_includes=args.include, size=args.size, sort=args.sort,
                                 query=self.make_query(args))
        print_data([hit["_source"] for hit in res["hits"]["hits"]], args.format)

    def make_query(self, args):
        """ Build and return the query body for a given set of arguments.
        """
        return {"match_all": {}}


class MatchSearchQuery(SearchQuery):
    """ Perform a 'match' search query against an index.
    """

    def attach(self, subparsers):
        parser = subparsers.add_parser("match", description=MatchSearchQuery.__doc__)
        parser.add_argument("pattern", metavar="FIELD=QUERY",
                            help="Pattern to match in the form 'FIELD=QUERY'.")
        parser.set_defaults(f=self.execute)
        return parser

    def make_query(self, args):
        field, _, query = args.pattern.partition("=")
        return {"match": {field: query}}


class TermSearchQuery(SearchQuery):
    """ Perform a 'term' search query against an index.
    """

    def attach(self, subparsers):
        parser = subparsers.add_parser("term", description=TermSearchQuery.__doc__)
        parser.add_argument("pattern", metavar="FIELD=VALUE",
                            help="Term to match in the form 'FIELD=VALUE'.")
        parser.set_defaults(f=self.execute)
        return parser

    def make_query(self, args):
        field, _, value = args.pattern.partition("=")
        return {"term": {field: value}}

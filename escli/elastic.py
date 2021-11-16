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


from argparse import ArgumentParser
from os import getenv

from elasticsearch import Elasticsearch

from escli.commands.search import SearchCommand
from escli.commands.version import VersionCommand


class ElasticsearchWrapper:

    def __init__(self, client=None, parser=None):
        self.client = client or default_client()
        self.parser = parser or default_parser(self.client)

    def execute(self, args=None, namespace=None):
        args = self.parser.parse_args(args=args, namespace=namespace)
        return args.f(args)


def default_client():
    """ Construct a default Elasticsearch client instance.
    """
    es_user = getenv("ES_USER", "elastic")
    es_password = getenv("ES_PASSWORD")
    if es_password:
        # with auth
        es = Elasticsearch(http_auth=(es_user, es_password))
    else:
        # without auth
        es = Elasticsearch()
    return es


def default_parser(client):
    """ Construct a default ArgumentParser instance for a given client.
    """
    parser = ArgumentParser(description=__doc__)
    parser.set_defaults(f=lambda _: parser.print_usage())
    subparsers = parser.add_subparsers()
    VersionCommand().add_parser(subparsers)
    SearchCommand(client).add_parser(subparsers)
    return parser

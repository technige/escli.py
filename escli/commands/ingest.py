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


from logging import getLogger

from escli.commands import Command
from escli.io import iter_json, iter_ndjson, csv_formats, iter_csv

log = getLogger(__name__)


class IngestCommand(Command):
    """ Load data into an Elasticsearch index.
    """

    def attach(self, subparsers):
        parser = subparsers.add_parser("ingest", description=IngestCommand.__doc__)
        parser.add_argument("repo", metavar="REPO",
                            help="Target repository to ingest into. For Elasticsearch, this will be an index name; "
                                 "for Enterprise Search, this will be an engine name.")
        parser.add_argument("files", metavar="FILE", nargs="*",
                            help="Files from which to load data. Data must be in JSON format, "
                                 "and the filename '-' can be used to read from standard input.")
        parser.add_argument("-f", "--format", default="json",
                            help="Input data format")
        parser.set_defaults(f=self.load)
        return parser

    def load(self, args):
        if args.format == "json":
            self.load_json(args.repo, args.files)
        elif args.format == "ndjson":
            self.load_ndjson(args.repo, args.files)
        elif args.format in csv_formats:
            self.load_csv(args.repo, args.files, dialect=csv_formats[args.format])
        else:
            raise ValueError("Unsupported input format %r" % args.format)

    def load_json(self, repo, files):
        for document, filename in iter_json(files):
            res = self.spi.client.ingest(repo, document)
            log.info("Ingested JSON data from file %r with result %s" % (filename, res))

    def load_ndjson(self, repo, files):
        for document, filename, line_no in iter_ndjson(files):
            res = self.spi.client.ingest(repo, document)
            log.info("Ingested JSON data from file %r, line %d with result %s" % (filename, line_no, res))

    def load_csv(self, repo, files, dialect):
        for document, filename, line_no in iter_csv(files, dialect):
            res = self.spi.client.ingest(repo, document)
            log.info("Ingested CSV data from file %r, line %d with result %s" % (filename, line_no, res))

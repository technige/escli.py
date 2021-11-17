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


from fileinput import FileInput
from json import loads, JSONDecodeError
from logging import getLogger

from escli.commands import Command


log = getLogger(__name__)


class IngestCommand(Command):
    """ Load data into an Elasticsearch index.
    """

    def __init__(self, client):
        super().__init__()
        self.client = client

    def attach(self, subparsers):
        parser = subparsers.add_parser("ingest", description=IngestCommand.__doc__)
        parser.add_argument("index", metavar="INDEX",
                            help="Target index into which to ingest data.")
        parser.add_argument("files", metavar="FILE", nargs="*",
                            help="Files from which to load data. Data must be in JSON format, "
                                 "and the filename '-' can be used to read from standard input.")
        parser.set_defaults(f=self.execute)
        return parser

    def execute(self, args):
        for filename, lines in multi_read(args.files):
            try:
                document = loads("".join(lines))
            except JSONDecodeError as ex:
                log.error("Failed to parse file %r (%s)" % (filename, ex))
            else:
                res = self.client.index(args.index, document=document)
                log.info("Ingested JSON data from file %r with result %s" % (filename, res))


def multi_read(files):
    """ Iterate through a sequence of input files, reading and yielding
    a (filename, lines) tuple for each.

    Each item in `files` is a string holding the name of a file to
    read. This function wraps the built-in FileInput class from the
    fileinput module and, as such, an empty list or a '-' filename
    will instead read from stdin.
    """
    last_filename = None
    lines = []
    with FileInput(files) as file_input:
        for line in file_input:
            if file_input.isfirstline():
                if last_filename is not None:
                    yield last_filename, "".join(lines)
                last_filename = file_input.filename()
                lines[:] = []
            lines.append(line)
    if last_filename is not None:
        yield last_filename, "".join(lines)

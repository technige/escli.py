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


from abc import ABC, abstractmethod
from argparse import ArgumentParser
from logging import getLogger

from escli.services import ClientAuthError


log = getLogger(__name__)


class CLI:
    """ Command line interface.
    """

    def __init__(self, spi, args=None, namespace=None):
        self.spi = spi
        self.parser = self.default_parser(self.spi)
        self.args = self.parser.parse_args(args=args, namespace=namespace)

    def process(self):
        """ Process the parsed arguments.
        """
        try:
            return self.args.f(self.args) or 0
        except ClientAuthError as ex:
            log.error(str(ex))
            log.warning("Check that the ESCLI_USER and ESCLI_PASSWORD environment variables are correctly set.")
            status = 1
        except Exception as ex:
            log.error(str(ex))
            status = 1
        return status

    @classmethod
    def default_parser(cls, spi):
        """ Build and return an ArgumentParser for the given SPI.
        """
        # TODO: avoid local imports
        from escli.commands.formats import FormatsCommand
        from escli.commands.ingest import IngestCommand
        from escli.commands.search import SearchCommand
        from escli.commands.version import VersionCommand
        parser = ArgumentParser(description=__doc__)
        parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity")
        parser.add_argument("-q", "--quiet", action="count", default=0, help="Decrease verbosity")
        parser.add_argument("-a", "--app", action="store_true", help="Use App Search instead of Elasticsearch")
        parser.set_defaults(f=lambda _: parser.print_usage())
        subparsers = parser.add_subparsers()
        VersionCommand(spi).attach(subparsers)
        FormatsCommand(spi).attach(subparsers)
        SearchCommand(spi).attach(subparsers)
        IngestCommand(spi).attach(subparsers)
        return parser


class Command(ABC):
    """ Abstract base class for commands available through the command
    line interface.
    """

    def __init__(self, spi):
        self.spi = spi

    @abstractmethod
    def attach(self, subparsers):
        """ Attach a parser for this command to the given subparsers
        collection.
        """

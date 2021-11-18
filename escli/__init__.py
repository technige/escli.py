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
from logging import basicConfig, getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from os import getenv

from elasticsearch import Elasticsearch, ConnectionError, AuthenticationException, TransportError

from escli.commands.formats import FormatsCommand
from escli.commands.ingest import IngestCommand
from escli.commands.search import SearchQuery
from escli.commands.version import VersionCommand
from escli.version import get_version


__version__ = get_version()

log = getLogger(__name__)

LOG_FORMAT = "\x1b[36m%(levelname)s: [%(name)s] %(message)s\x1b[39m"


def make_client():
    """ Construct a default Elasticsearch client instance.
    """
    es_host = getenv("ES_HOST", "localhost")
    es_user = getenv("ES_USER", "elastic")
    es_password = getenv("ES_PASSWORD")
    if es_password:
        # with auth
        es = Elasticsearch(hosts=es_host.split(","), http_auth=(es_user, es_password))
    else:
        # without auth
        es = Elasticsearch()
    return es


def make_parser(client):
    """ Build and return an ArgumentParser.
    """
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity")
    parser.add_argument("-q", "--quiet", action="count", default=0, help="Decrease verbosity")
    parser.set_defaults(f=lambda _: parser.print_usage())
    subparsers = parser.add_subparsers()
    VersionCommand().attach(subparsers)
    FormatsCommand().attach(subparsers)
    SearchQuery(client).attach(subparsers)
    IngestCommand(client).attach(subparsers)
    return parser


def configure_logging(verbosity):
    """ Configure logging according to the defined level of verbosity.

    The verbosity levels available are as follows:

        Level +2
          DEBUG, INFO, WARNING, ERROR, CRITICAL
        Level +1
          INFO, WARNING, ERROR, CRITICAL
        Level 0
          WARNING, ERROR, CRITICAL
        Level -1
          ERROR, CRITICAL
        Level -2
          CRITICAL

    """
    if verbosity >= 2:
        basicConfig(format=LOG_FORMAT, level=DEBUG)
    elif verbosity >= 1:
        basicConfig(format=LOG_FORMAT, level=INFO)
    elif verbosity >= 0:
        basicConfig(format=LOG_FORMAT, level=WARNING)
    elif verbosity >= -1:
        basicConfig(format=LOG_FORMAT, level=ERROR)
    else:
        basicConfig(format=LOG_FORMAT, level=CRITICAL)


def process_args(args):
    try:
        return args.f(args) or 0
    except ConnectionError as ex:
        log.error(str(ex))
        log.debug(ex.info)
        status = 1
    except AuthenticationException as ex:
        log.error(str(ex))
        log.debug(ex.info)
        log.warning("Check that the ES_USER and ES_PASSWORD environment variables are correctly set.")
        status = 1
    except TransportError as ex:
        log.error(str(ex))
        log.debug(ex.info)
        status = 1
    except Exception as ex:
        log.error(str(ex))
        status = 1
    return status

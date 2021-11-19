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
from logging import basicConfig, getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL

log = getLogger(__name__)


class SPI:
    """ Service provider interface.

    This interface decouples the consumers from the providers of backend
    services, allowing greater flexibility in their assembly.
    """

    log_format = "\x1b[36m%(levelname)s: [%(name)s] %(message)s\x1b[39m"

    def __init__(self):
        self.__client = None

    @property
    def client(self):
        if self.__client is None:
            log.critical("Service provider has not been configured with a client instance")
            raise TypeError("No client configured")
        return self.__client

    def init_logging(self, verbosity):
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
            basicConfig(format=self.log_format, level=DEBUG)
        elif verbosity >= 1:
            basicConfig(format=self.log_format, level=INFO)
        elif verbosity >= 0:
            basicConfig(format=self.log_format, level=WARNING)
        elif verbosity >= -1:
            basicConfig(format=self.log_format, level=ERROR)
        else:
            basicConfig(format=self.log_format, level=CRITICAL)

    def init_client(self, use_app_search=False):
        self.__client = Client.create(use_app_search=use_app_search)


class Client(ABC):
    """ Base client abstraction.
    """

    @classmethod
    def create(cls, use_app_search=False):
        # TODO: avoid local import
        if use_app_search:
            from escli.services.enterprisesearch import AppSearchClient
            return AppSearchClient()
        else:
            from escli.services.elasticsearch import ElasticsearchClient
            return ElasticsearchClient()

    @abstractmethod
    def search(self, repo, query, fields=None, sort=None, page_size=10, page_number=1):
        """ Carry out a search.
        """

    @abstractmethod
    def ingest(self, repo, document):
        """ Ingest data.
        """


class ClientConnectionError(Exception):

    pass


class ClientAuthError(Exception):

    pass


class ClientAPIError(Exception):

    pass

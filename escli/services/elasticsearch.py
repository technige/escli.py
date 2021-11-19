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


from os import getenv
from logging import getLogger

from elasticsearch import Elasticsearch, ConnectionError, AuthenticationException, TransportError

from escli.services import Client, ClientConnectionError, ClientAuthError, ClientAPIError


log = getLogger(__name__)


class ElasticsearchClient(Client):

    def __init__(self):
        """ Construct a default Elasticsearch client instance.
        """
        es_host = getenv("ES_HOST", "localhost")
        es_user = getenv("ES_USER", "elastic")
        es_password = getenv("ES_PASSWORD")
        with ElasticsearchExceptionWrapper():
            if es_password:
                # with auth
                self.es = Elasticsearch(hosts=es_host.split(","), http_auth=(es_user, es_password))
            else:
                # without auth
                self.es = Elasticsearch()

    def search_all(self, index, include=None, size=None, sort=None):
        """ Carry out a search, matching all results.
        """
        with ElasticsearchExceptionWrapper():
            res = self.es.search(index=index, _source_includes=include, size=size, sort=sort,
                                 query={"match_all": {}})
        return [hit["_source"] for hit in res["hits"]["hits"]]

    def search(self, index, field, value, include=None, size=None, sort=None):
        """ Carry out a search, matching results where the `value` can
        be found in the `field`.
        """
        with ElasticsearchExceptionWrapper():
            res = self.es.search(index=index, _source_includes=include, size=size, sort=sort,
                                 query={"match": {field: value}})
        return [hit["_source"] for hit in res["hits"]["hits"]]

    def search_exact(self, index, field, value, include=None, size=None, sort=None):
        """ Carry out a search, matching results where the `field` is an
        exact match for the `value`.
        """
        with ElasticsearchExceptionWrapper():
            res = self.es.search(index=index, _source_includes=include, size=size, sort=sort,
                                 query={"term": {field: value}})
        return [hit["_source"] for hit in res["hits"]["hits"]]

    def ingest(self, index, document):
        """ Ingest data.
        """
        with ElasticsearchExceptionWrapper():
            res = self.es.index(index=index, document=document)
        return res  # TODO: something more intelligent


class ElasticsearchExceptionWrapper:
    """ Wrapper to catch and promote exceptions to the appropriate level
    of abstraction.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            return
        try:
            raise exc_val
        except ConnectionError as ex:
            log.debug(ex.info)
            raise ClientConnectionError("Connection error: %s" % ex) from ex
        except AuthenticationException as ex:
            log.debug(ex.info)
            raise ClientAuthError("Auth error: %s" % ex) from ex
        except TransportError as ex:
            log.debug(ex.info)
            raise ClientAPIError("API error: %s" % ex) from ex

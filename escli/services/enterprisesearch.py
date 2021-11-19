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

from elastic_enterprise_search import AppSearch, ConnectionError, TransportError

from escli.services import Client, ClientConnectionError, ClientAuthError, ClientAPIError


log = getLogger(__name__)


class AppSearchClient(Client):
    """ Client for use with Enterprise App Search.
    """

    def __init__(self):
        host = getenv("ESCLI_HOST")
        user = getenv("ESCLI_USER", "enterprise_search")
        password = getenv("ESCLI_PASSWORD")
        with EnterpriseSearchExceptionWrapper():
            self._client = AppSearch(hosts=["http://" + h for h in host.split(",")] if host else None,
                                     http_auth=(user, password) if password else None)

    def search(self, repo, query, fields=None, sort=None, page_size=10, page_number=1):
        body = {
            "query": query or "",
            "page": {
                "size": page_size,
                "current": page_number,
            },
        }
        if fields:
            body["result_fields"] = {field: {"raw": {}} for field in fields.split(",")}
        if sort:
            if sort.startswith("~"):
                body["sort"] = {sort[1:]: "desc"}
            else:
                body["sort"] = {sort: "asc"}
        with EnterpriseSearchExceptionWrapper():
            response = self._client.search(engine_name=repo, body=body)
        # TODO: don't throw away metadata
        return [{key: value["raw"] for key, value in result.items() if not key.startswith("_")}
                for result in response["results"]]

    def ingest(self, repo, document):
        with EnterpriseSearchExceptionWrapper():
            res = self._client.index_documents(engine_name=repo, documents=[document])
        return res  # TODO: something more intelligent


class EnterpriseSearchExceptionWrapper:
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
            raise ClientConnectionError("Connection error: %s" % ex) from ex
        except TransportError as ex:
            raise ClientAPIError("API error: %s" % ex) from ex

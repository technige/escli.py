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

from elastic_enterprise_search import AppSearch, ConnectionError, TransportError

from escli.services import Client, ClientConnectionError, ClientAPIError


log = getLogger(__name__)


class AppSearchClient(Client):
    """ Client for use with Enterprise App Search.
    """

    def __init__(self):
        with EnterpriseSearchExceptionWrapper():
            self._client = AppSearch(**self.get_settings_from_env())

    def search(self, target, query, fields=None, sort=None, page_size=10, page_number=1):
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
            response = self._client.search(engine_name=target, body=body)
        # TODO: don't throw away metadata
        return [{key: value["raw"] for key, value in result.items() if not key.startswith("_")}
                for result in response["results"]]

    def ingest(self, target, document):
        with EnterpriseSearchExceptionWrapper():
            res = self._client.index_documents(engine_name=target, documents=[document])
        return res  # TODO: something more intelligent

    def get_indexes(self, include_all=False):
        engines = {}
        with EnterpriseSearchExceptionWrapper():
            r = self._client.list_engines()
            for result in r["results"]:
                name = result.pop("name")
                if include_all or not name.starts_with("."):
                    engines[name] = result
        return engines

    def create_index(self, name):
        with EnterpriseSearchExceptionWrapper():
            self._client.create_engine(name)

    def delete_index(self, name):
        with EnterpriseSearchExceptionWrapper():
            self._client.delete_engine(name)


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

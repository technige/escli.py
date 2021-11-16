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


class Command(ABC):
    """ Abstract base class for commands available through the command
    line interface.
    """

    @abstractmethod
    def add_parser(self, subparsers):
        """ Add a parser for this command to the given subparsers
        collection.
        """

    @abstractmethod
    def execute(self, args):
        """ Execute this command using the given arguments.
        """

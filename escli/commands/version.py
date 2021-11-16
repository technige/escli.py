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


from escli import __version__
from escli.commands import Command


class VersionCommand(Command):
    """ Show the version.
    """

    def attach(self, subparsers):
        parser = subparsers.add_parser("version", description=VersionCommand.__doc__)
        parser.set_defaults(f=lambda _: print("escli version %s" % __version__))
        return parser

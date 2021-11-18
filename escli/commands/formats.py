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


from escli.commands import Command
from escli.writer import output_formats


class FormatsCommand(Command):
    """ Display information on supported formats.
    """

    def attach(self, subparsers):
        parser = subparsers.add_parser("formats", description=FormatsCommand.__doc__)
        parser.set_defaults(f=lambda _: print_formats())
        return parser


def print_grid(items, item_width, items_per_row, indent):
    h_pos = items_per_row - 1
    for i, fmt in enumerate(items):
        h_pos = i % items_per_row
        if h_pos == 0:
            print(" " * indent, end="")
        print(fmt.ljust(item_width), end="")
        if h_pos == items_per_row - 1:
            print()
    if h_pos != items_per_row - 1:
        print()


def print_formats():
    print("Output formats for search results:")
    print_grid(sorted(output_formats), item_width=19, items_per_row=4, indent=2)

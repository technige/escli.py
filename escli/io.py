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


from csv import list_dialects, reader, writer
from fileinput import FileInput
from json import dumps, loads, JSONDecodeError
from logging import getLogger
from sys import stdout

from tabulate import tabulate, tabulate_formats


log = getLogger(__name__)


csv_formats = {"csv_{}".format(dialect.replace("-", "_")): dialect
               for dialect in list_dialects()}
if "csv_excel" in csv_formats:
    csv_formats["csv"] = csv_formats.pop("csv_excel")
if "csv_excel_tab" in csv_formats:
    csv_formats["tsv"] = csv_formats.pop("csv_excel_tab")

output_formats = set(tabulate_formats) | csv_formats.keys() | {"ndjson"}


def print_data(data, fmt):
    if fmt == "ndjson":
        for datum in data:
            print(dumps(datum))
    elif fmt in csv_formats:
        csv_writer = writer(stdout, dialect=csv_formats[fmt])
        for i, datum in enumerate(data):
            if i == 0:
                csv_writer.writerow(datum.keys())
            csv_writer.writerow(datum.values())
    elif fmt in tabulate_formats:
        print(tabulate(data, headers="keys", tablefmt=fmt))
    else:
        raise ValueError("Unsupported output format %r" % fmt)


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


def iter_json(files):
    """ Iterate through each of the files supplied, parsing and yielding
    a JSON document for each.
    """
    for filename, lines in multi_read(files):
        src = "".join(lines)
        try:
            document = loads(src)
        except JSONDecodeError as ex:
            log.error("Failed to parse JSON in file %r (%s)" % (filename, ex))
        else:
            yield document, filename


def iter_ndjson(files):
    with FileInput(files) as file_input:
        for src in file_input:
            if not src:
                continue  # skip blank lines
            try:
                document = loads(src)
            except JSONDecodeError as ex:
                log.error("Failed to parse JSON in file %r, line %d (%s)" % (
                    file_input.filename(), file_input.filelineno(), ex))
            else:
                yield document, file_input.filename(), file_input.filelineno()


def iter_csv(files, dialect):
    with FileInput(files) as file_input:
        csv_reader = reader(file_input, dialect=dialect)
        keys = next(csv_reader)
        for values in csv_reader:
            document = dict(zip(keys, values))
            yield document, file_input.filename(), file_input.filelineno()

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


from escli import make_client, make_parser, configure_logging, process_args


def main():
    client = make_client()
    parser = make_parser(client)
    args = parser.parse_args()
    configure_logging(args.verbose - args.quiet)
    status = process_args(args)
    exit(status)


if __name__ == '__main__':
    main()

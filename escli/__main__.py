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


from escli.commands import CLI
from escli.services import SPI


def main(mode=None):
    spi = SPI()
    cli = CLI(spi)
    spi.init_logging(cli.args.verbose - cli.args.quiet)
    spi.init_client(mode)
    status = cli.process()
    exit(status)


def main_app():
    main(mode="app")


def main_serverless():
    main(mode="serverless")


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters_remove_outdated import bincrafters_remove_outdated
import sys


def run():
    bincrafters_remove_outdated.main(sys.argv[1:])


if __name__ == '__main__':
    run()

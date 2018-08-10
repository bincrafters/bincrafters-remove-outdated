#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info.major == 3:
    from bincrafters_remove_outdated import bincrafters_remove_outdated
else:
    import bincrafters_remove_outdated


def run():
    bincrafters_remove_outdated.main(sys.argv[1:])


if __name__ == '__main__':
    run()

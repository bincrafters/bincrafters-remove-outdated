#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import colorama
import termcolor
from conans.client import conan_api
from conans.model.ref import ConanFileReference

__author__  = "Uilian Ries"
__license__ = "MIT"
__version__ = '0.3.1'


class Command(object):
    """ Execute Travis file update
    """

    def __init__(self):
        """ Fill regex compiler
        """
        self._arguments = None
        self._conan_instance, _, _ = conan_api.Conan.factory()
        colorama.init()

    def set_conan_instance(self, conan_instance):
        """Setter for conan instance API
        """
        self._conan_instance = conan_instance

    def _parse_arguments(self, *args):
        """ Add program arguments

        :param args: User arguments
        """
        parser = argparse.ArgumentParser(description="Conan Remove Outdated")
        parser.add_argument('remote', type=str, help='Conan remote to be cleaned e.g conan-center')
        parser.add_argument('--yes', '-y', action='store_true', help='Do not ask for confirmation')
        parser.add_argument('--ignore', '-i', action='store_true', help='Ignore errors receive from remote')
        parser.add_argument('--dry-run', '-d', action='store_true', help='Check which packages will be removed only')
        parser.add_argument('--pattern', '-p', default='*', help='Pattern to filter package name to be removed. e.g Boost/*')
        parser.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(__version__))
        args = parser.parse_args(*args)
        return args

    def _notify_error(self, message):
        """Raise exception or print a message if ignore errors
        """
        if not self._arguments.ignore:
            raise Exception(message)
        print(termcolor.colored("ERROR: {}".format(message), 'red'))

    def run(self, *args):
        """ Process file update

        :param args: User arguments
        """
        self._arguments = self._parse_arguments(*args)
        if not self._arguments.remote:
            raise Exception("Remote is not defined.")

        self._clean_remote(self._arguments.remote, self._arguments.yes)

    def _clean_remote(self, remote, skip_input):
        """Remove all outdated recipes from Conan remote

        :param remote: Conan remote name
        :param skip_input: Do not ask for confirmation
        """
        if skip_input:
            print(termcolor.colored("WARNING: Using --skip_input option. Conan won't ask before to remove!", "yellow"))
        print(termcolor.colored("Fetching recipes from {}".format(remote), "blue"))
        recipes = self._get_recipes_from_remote(remote)
        for recipe in recipes:
            print(termcolor.colored("{}: Searching for outdated packages".format(recipe), "blue"))
            if self._are_there_outdated_packages(remote, recipe):
                print(termcolor.colored("{}: Found outdated packages. Removing ...".format(recipe), "blue"))
                try:
                    if not self._arguments.dry_run:
                        self._conan_instance.remove(recipe, remote=remote, outdated=True, force=skip_input)
                except Exception as error:
                    self._notify_error(error)

    def _get_recipes_from_remote(self, remote):
        """List all recipes on remote server

        :param remote: Conan remote name
        :return: list of recipes
        """
        result = self._conan_instance.search_recipes(self._arguments.pattern, remote=remote)
        if result.get('error'):
            self._notify_error("Could not retrieve recipes from remote: {}".format(result.get('results')))

        if not result['results']:
            self._notify_error("Could not retrieve recipes with pattern: {}".format(self._arguments.pattern))

        recipes = [recipe['recipe']['id'] for recipe in result['results'][0]['items']]

        print(termcolor.colored("Found {} recipes on remote {}:".format(len(recipes), remote), "blue"))
        for recipe in recipes:
            print(recipe)

        return recipes

    def _are_there_outdated_packages(self, remote, recipe):
        reference = ConanFileReference.loads(recipe)
        result = self._conan_instance.search_packages(reference, remote=remote, outdated=True)
        if result.get('error'):
            self._notify_error("Could not obtain remote package info")
        packages = result['results'][0]['items'][0]['packages']
        for package in packages:
            if package.get('outdated'):
                print(termcolor.colored("{}: Package id {} is outdated".format(recipe, package.get('id'))))
        return packages


def main(args):
    """ Execute command update

    :param args: User arguments
    """
    try:
        command = Command()
        command.run(args)
    except Exception as error:
        print(termcolor.colored("ERROR: {}".format(error), 'red'))
        sys.exit(1)

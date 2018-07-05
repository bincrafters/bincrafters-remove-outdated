#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import logging
from conans.client import conan_api
from conans.model.ref import ConanFileReference
from bincrafters_remove_outdated import __version__ as version


LOGGING_FORMAT = '[%(levelname)s]\t%(asctime)s %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')


class Command(object):
    """ Execute Travis file update
    """

    def __init__(self):
        """ Fill regex compiler
        """
        self._logger = logging.getLogger(__file__)
        self._logger.setLevel(logging.DEBUG)
        self._conan_instance, _, _ = conan_api.Conan.factory()

    def set_conan_instance(self, conan_instance):
        """Setter for conan instance API
        """
        self._conan_instance = conan_instance

    def _parse_arguments(self, *args):
        """ Add program arguments

        :param args: User arguments
        """
        parser = argparse.ArgumentParser(description="Conan Remove Outdated")
        parser.add_argument('remote', type=str, help='Conan remote to be cleaned')
        parser.add_argument('--yes', '-y', action='store_true', help='Do not ask for confirmation')
        parser.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(version))
        args = parser.parse_args(*args)
        return args

    def run(self, *args):
        """ Process file update

        :param args: User arguments
        """
        arguments = self._parse_arguments(*args)
        if not arguments.remote:
            raise Exception("Remote is not defined.")

        self._clean_remote(arguments.remote, arguments.yes)

    def _clean_remote(self, remote, skip_input):
        """Remove all outdated recipes from Conan remote

        :param remote: Conan remote name
        :param skip_input: Do not ask for confirmation
        """
        recipes = self._get_recipes_from_remote(remote)
        for recipe in recipes:
            if self._are_there_outdated_packages(remote, recipe):
                self._conan_instance.remove(recipe, outdated=True, force=skip_input)

    def _get_recipes_from_remote(self, remote):
        """List all recipes on remote server

        :param remote: Conan remote name
        :return: list of recipes
        """
        result = self._conan_instance.search_recipes("*", remote=remote)
        if result.get('error'):
            raise Exception("Could not retrieve recipes from remote: {}".format(result.get('results')))

        recipes = [recipe['recipe']['id'] for recipe in result['results'][0]['items']]
        self._logger.debug("RECIPES: {}".format(recipes))
        return recipes

    def _are_there_outdated_packages(self, remote, recipe):
        reference = ConanFileReference.loads(recipe)
        result = self._conan_instance.search_packages(reference, remote=remote, outdated=True)
        if result.get('error'):
            raise Exception("Could not obtain remote package info")
        return result['results'][0]['items'][0]['packages']


def main(args):
    """ Execute command update

    :param args: User arguments
    """
    try:
        command = Command()
        command.run(args)
    except Exception as error:
        logging.error("ERROR: {}".format(error))
        sys.exit(1)

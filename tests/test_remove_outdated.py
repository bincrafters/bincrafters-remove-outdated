#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import tempfile
from conans.client import conan_api
from conans.model.ref import ConanFileReference
from bincrafters_remove_outdated import bincrafters_remove_outdated


@pytest.fixture
def server():
    from conans.test.utils.tools import TestServer
    test_server = TestServer(read_permissions=[("*/*@*/*", "*")],
                                  write_permissions=[("*/*@foobar/stable", "conanuser")],
                                  users={"conanuser": "conanpass"})
    return test_server


@pytest.fixture()
def client(server):
    from conans.test.utils.tools import TestClient
    conanfile = """from conans import ConanFile
class MyPkg(ConanFile):
    name = "Hello"
    version = "0.1.0"
    exports_sources = "*"
    def package(self):
        self.copy("*")
"""
    test_client = TestClient(servers={"testing": server}, users={"testing": [("conanuser", "conanpass")]})
    test_client.save({"conanfile.py": conanfile})
    test_client.run("create . conanuser/testing")
    test_client.run("upload Hello/0.1.0@conanuser/testing -r testing --all --force")
    conanfile = """from conans import ConanFile
class MyPkg(ConanFile):
    name = "Hello"
    version = "0.1.0"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports_sources = "*"
    def package(self):
        self.copy("*")
"""
    test_client.save({"conanfile.py": conanfile})
    test_client.run("create . conanuser/testing")
    test_client.run("upload Hello/0.1.0@conanuser/testing -r testing --all --force")
    return test_client


def create_temp_file(package_list):
    for package in package_list:
        with tempfile.NamedTemporaryFile(delete=False) as file:
            file.write(package.encode())
            return file.name


def create_valid_package_file():
    return create_temp_file(['Hello/0.1.0@conanuser/testing'])


def create_invalid_package_file():
    return create_temp_file(['Hello/0.1.0@conanuser/testing', 'Boost/*', '1234', 'foobar'])


def has_outdated_packages(packages):
    assert not packages['error']
    results = packages['results']
    assert results
    for result in results:
        items = result['items']
        assert items
        for item in items:
            packages = item['packages']
            assert packages
            for package in packages:
                if package['outdated'] == True:
                    return True
    return False


def get_package_list(conan_instance):
    reference = ConanFileReference.loads("Hello/0.1.0@conanuser/testing")
    return conan_instance.search_packages(reference, remote_name='testing')


def test_valid_package_list(client):
    conan_instance = conan_api.Conan(client.client_cache, client.user_io, client.runner, client.remote_manager)
    command = bincrafters_remove_outdated.Command()
    package_list_file = create_valid_package_file()
    command.set_conan_instance(conan_instance)
    command.run(['testing', '--yes', '--package-list-file={}'.format(package_list_file)])
    packages = get_package_list(conan_instance)
    assert not has_outdated_packages(packages)


def test_invalid_package_list(client):
    conan_instance = conan_api.Conan(client.client_cache, client.user_io, client.runner, client.remote_manager)
    command = bincrafters_remove_outdated.Command()
    package_list_file = create_invalid_package_file()
    command.set_conan_instance(conan_instance)
    command.run(['testing', '--yes', '--package-list-file={}'.format(package_list_file)])
    packages = get_package_list(conan_instance)
    assert not has_outdated_packages(packages)


def test_remove_outdate_package(client):
    conan_instance = conan_api.Conan(client.client_cache, client.user_io, client.runner, client.remote_manager)
    command = bincrafters_remove_outdated.Command()
    packages = get_package_list(conan_instance)
    assert has_outdated_packages(packages)
    command.set_conan_instance(conan_instance)
    command.run(['testing', '--yes'])
    packages = get_package_list(conan_instance)
    assert not has_outdated_packages(packages)


def test_remove_outdate_package_with_pattern(client):
    conan_instance = conan_api.Conan(client.client_cache, client.user_io, client.runner, client.remote_manager)
    command = bincrafters_remove_outdated.Command()
    command.set_conan_instance(conan_instance)
    command.run(['testing', '--pattern=Hello/*', '--yes'])
    packages = get_package_list(conan_instance)
    assert not has_outdated_packages(packages)


def test_remove_outdate_package_with_wrong_pattern(client):
    conan_instance = conan_api.Conan(client.client_cache, client.user_io, client.runner, client.remote_manager)
    command = bincrafters_remove_outdated.Command()
    command.set_conan_instance(conan_instance)
    try:
        command.run(['testing', '--pattern=Boost/*', '--yes'])
        pytest.fail('Boost should not be found')
    except Exception as error:
        assert 'Could not retrieve recipes with pattern: Boost/*' == str(error)
    packages = get_package_list(conan_instance)
    assert has_outdated_packages(packages)


def test_remove_outdate_package_with_ignore(client):
    conan_instance = conan_api.Conan(client.client_cache, client.user_io, client.runner, client.remote_manager)
    command = bincrafters_remove_outdated.Command()
    command.set_conan_instance(conan_instance)
    command.run(['testing', '--yes', '--ignore'])
    packages = get_package_list(conan_instance)
    assert not has_outdated_packages(packages)


def test_dry_run_outdate_package(client):
    conan_instance = conan_api.Conan(client.client_cache, client.user_io, client.runner, client.remote_manager)
    command = bincrafters_remove_outdated.Command()
    command.set_conan_instance(conan_instance)
    command.run(['testing', '--dry-run'])
    packages = get_package_list(conan_instance)
    assert has_outdated_packages(packages)

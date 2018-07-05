#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from conans.client import conan_api
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
    test_client.run("upload Hello/0.1.0@conanuser/testing -r testing")
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
    test_client.run("upload Hello/0.1.0@conanuser/testing -r testing")
    return test_client


def test_remove_outdate_package(client):
    conan_instance = conan_api.Conan(client.client_cache, client.user_io, client.runner, client.remote_manager, None, None)
    command = bincrafters_remove_outdated.Command()
    command.set_conan_instance(conan_instance)
    command.run(['testing'])

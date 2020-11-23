from modules import crypto
from modules import file_io
from objects import cls_service
from getpass import getpass


def init_crypto():
    password = getpass("Enter Password: ")
    crypto.set_key(password)
    file_io.crypto_test()


def add_service(services, name, username, password, note):
    new_service = cls_service.service(name, username, password, note)
    services[name] = new_service
    file_io.write_file(services)


def remove_service(services, name):
    services.pop(name)
    file_io.write_file(services)

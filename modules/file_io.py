from modules import crypto
from objects import cls_service
import os
import pathlib


abs_path = pathlib.Path(__file__).parent.absolute()
data_file = str(abs_path) + "/profile.dat"
data_file = data_file.replace('\\', '/')
data_file = data_file.replace('/modules', '')
#Yes, I know, this is dirty.


def crypto_test():
    if os.path.exists(data_file):
        file = open(data_file, 'rb')

        try:
            decrypt_data = crypto.decrypt(file.read())
        except:
            print("Wrong key used for existing profile")
            exit()


def write_file(services):
    if os.path.exists(data_file):
        os.remove(data_file)

    lines = ""

    for key in services:
        lines += services[key].get_name() + ';' + services[key].get_username() + ';' + services[key].get_password() + ';' + services[key].get_note() + "; \n"

    file = open(data_file, 'wb')
    file.write(crypto.encrypt(lines))
    file.close()


def read_file():
    services = {}

    if os.path.exists(data_file):
        file = open(data_file, 'rb')
        lines = crypto.decrypt(file.read())
        file.close()

        for line in lines.splitlines():
            elements = line.split(";")
            new_service = cls_service.service(elements[0], elements[1], elements[2], elements[3])
            services[elements[0]] = new_service

    return services

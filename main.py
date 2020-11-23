from modules.routines import *
from os import system, name
import pyperclip


services = {}


def list_services():
    if not services:
        print("No services added")
    else:
        service_list = []
        for key in services:
            service_list.append(services[key].get_name())

        service_list = sorted(service_list)
        count = 0
        for service in service_list:
            count += 1
            print(f"{count:02d}", service)


def clear():
    if name == 'nt':
        # For windows
        _ = system('cls')
    else:
        #For Mac and Linux
        _ = system('clear')


def interpret_cmd(command):
    if command == "list":
        list_services()


    elif command == "add":
        name = input("Enter name of service: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        note = input("(Optional) Enter note: ")

        if name != "":
            add_service(services, name, username, password, note)
            print(name, "added")
        else:
            print("Service must have a name")


    elif "quickadd " in command:
        parsed_command = command.replace("quickadd ", "")
        split = parsed_command.split(' ')

        name = split[0]
        username = split[1]
        password = split[2]
        note = ""
        if len(split) > 3:
            for i in range(3, len(split)):
                note += split[i] + " "

        if name != "" and password != "":
            add_service(services, name, username, password, note)
            print(name, "added")
        else:
            print("Services require a username and password")


    elif "remove " in command:
        name = command.replace('remove ', '')
        if name in services:
            remove_service(services, name)
            print(name, "removed")
        else:
            print("Service not found, be sure to type case-sensitively")


    elif "get " in command and " --pvt" in command:
        command = command.replace('get ', '')
        name = command.replace(' --pvt', '')
        if name in services:
            print("Username:", '*' * (len(services[name].get_username()) - 4) + services[name].get_username()[len(services[name].get_username()) - 4:])
            print("Password:", '*' * (len(services[name].get_password()) - 4) + services[name].get_password()[len(services[name].get_password()) - 4:])
            print("Note:", services[name].get_note())
        else:
            print("Service not found, be sure to type case-sensitively")


    elif "get " in command:
        name = command.replace('get ', '')
        if name in services:
            print("Username:", services[name].get_username())
            print("Password:", services[name].get_password())
            print("Note:", services[name].get_note())
        else:
            print("Service not found, be sure to type case-sensitively")


    elif "getpass " in command:
        name = command.replace('getpass ', '')
        if name in services:
            pyperclip.copy(services[name].get_password())
            print("Password copied to clipboard")
        else:
            print("Service not found, be sure to type case-sensitively")


    elif command == "clear":
        clear()


    elif command == "help":
        print("add - adds a new service or edits an existing one the slow way\n"
              "quickadd name username password note - if you want no note, just leave the arg blank\n"
              "remove 'service name' - removes a service given its name\n"
              "get 'service name' [--option] - gets the details of a service given its name.\n"
              "     available options: --pvt - gets the details with the user and pass censored.\n"
              "getuser 'service name' - copies the desired username to the clipboard\n"
              "getpass 'service name' - copies the desired password to the clipboard\n"
              "clear - clears this terminal window"
              "exit - quits the program")


    elif command == "exit":
        exit()


    else:
        print("Unrecognized Command...")

    print()


if __name__ == '__main__':
    init_crypto()
    services = file_io.read_file()
    clear()

    while True:
        interpret_cmd(input("Enter a command: "))

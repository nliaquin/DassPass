from modules.routines import *
from modules.password_generator import generate_password
from os import system, name
import pyperclip

services = {}
service_names = []

def list_services():
    global service_names

    if not services:
        print("No services added")
    else:
        if not service_names:
            populate_service_names()

        service_names = sorted(service_names)
        count = 0
        for service in service_names:
            count += 1
            print(f"{count:02d}", service)


def populate_service_names():
    service_names.clear()
    for key in services:
        service_names.append(services[key].get_name())


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
    elif "add " in command:
        parsed_command = command.replace("quickadd ", "")
        split = parsed_command.split(' ')
        name = split[0]
        username = split[1]
        password = ''
        note = ''

        if len(split) == 2:
            #This means the user expects the program to automatically generate a password
            password += generate_password()
        elif len(split) == 3:
            #This just means there's no note to process, but a password was given
            password += split[3]
        elif len(split) > 3:
            #Now we have a note to process, but notes are never just one line
            for i in range(3, len(split)):
                note += split[i] + " "

        if name != "" and password != "":
            add_service(services, name, username, password, note)
            service_names.append(name)
            print(name, "added")
        else:
            print("Services require a username and password")
    elif "remove " in command:
        name = command.replace('remove ', '')
        if name in services:
            remove_service(services, name)
            service_names.remove(name)
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
    elif "getuser " in command:
        name = command.replace('getuser ', '')
        if name in services:
            pyperclip.copy(services[name].get_username())
            print("Username copied to clipboard")
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
        print("add 'name' 'username' 'password' 'note' - if you want no note, just leave the arg blank, and notes can also include spaces\n"
              "remove 'service name' - removes a service given its name\n"
              "get 'service name' [--option] - gets the details of a service given its name.\n"
              "     available options: --pvt - gets the details with the user and pass censored.\n"
              "getuser 'service name' - copies the desired username to the clipboard\n"
              "getpass 'service name' - copies the desired password to the clipboard\n"
              "clear - clears this terminal window"
              "exit - quits the program")
    elif command == "exit":
        clear()
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

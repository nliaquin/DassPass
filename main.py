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
        parsed_command = command.replace("add ", "")
        split = parsed_command.split(' ')
        name = split[0]
        if name in service_names:
            print("Service already exists")
        else:
            username = split[1]
            password = ''
            note = ''

            if len(split) == 2:
                #This means the user expects the program to automatically generate a password
                password += generate_password()
            elif len(split) == 3:
                #This just means there's no note to process, but a password was given
                password += split[2]
            elif len(split) > 3:
                #Now we have a note to process, but notes are never just one line
                for i in range(3, len(split)):
                    note += split[i] + " "

            if name != "" and password != "":
                add_service(services, name, username, password, note)
                service_names.append(name)
                print(name, "added")
            else:
                print(name, username, password, note)
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
    elif "setname " in command:
        command = command.replace("setname ", "")
        args = command.split(" ")

        if len(args) == 2:
            name = args[0]
            newname = args[1]

            if name in service_names:
                services[name].set_name(newname)
                services[newname] = services.pop(name)
                save_to_file(services)
                service_names.remove(name)
                service_names.append(newname)
                print(f"{name} name changed to {newname}")
            else:
                print("Service not found")
        else:
            print("Too many arguments given")
    elif "setuser " in command:
        command = command.replace("setuser ", "")
        args = command.split(" ")

        if len(args) == 2:
            name = args[0]
            user = args[1]

            if name in service_names:
                services[name].set_username(user)
                save_to_file(services)
                print(f"{name} username changed")
            else:
                print("Service not found")
        else:
            print("Too many arguments given")
    elif "setpass " in command:
        command = command.replace("setpass ", "")
        args = command.split(" ")

        if len(args) < 3:
            name = args[0]
            new_password = ''

            if len(args) == 2:
                new_password += args[1]
            else:
                new_password += generate_password()

            if name in service_names:
                services[name].set_password(new_password)
                save_to_file(services)
                print(f"{name} password changed")
            else:
                print("Service not found")
        else:
            print("Too many arguments given")
    elif "setnote " in command:
        command = command.replace("setnote ", "")
        args = command.split(" ")
        name = args[0]
        note = ''

        if name in service_names:
            for x in range(1, len(args)):
                note += args[x] + " "

            services[name].set_note(note)
            print(f"Note set in {name}")
        else:
            print("Service specified does not exist")
    elif command == "clear":
        clear()
    elif command == "help":
        print("add 'service name' 'username' 'password' 'note' - if you want no note, just leave the arg blank, and notes can also include spaces\n"
              "remove 'service name' - removes a service given its name\n"
              "get 'service name' [--option] - gets the details of a service given its name\n"
              "     available options: --pvt - gets the details with the user and pass censored\n"
              "getuser 'service name' - copies the desired username to the clipboard\n"
              "getpass 'service name' - copies the desired password to the clipboard\n"
              "setname 'service name' 'new service name' - edits the name of a service\n"
              "setuser 'service name' 'new username' - edits the username for a given service\n"
              "setpass 'service name' 'new password' - edits the password for a given service\n"
              "     optionally, leave the new password arg blank to generate a password automatically"
              "setnote 'service name' 'new note' - edits the note for a given service\n"
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
    populate_service_names()
    clear()

    while True:
        interpret_cmd(input("Enter a command: "))

import os
import sys
from args import getArgs
from Passgen import Passgen
from ignore import addIgnorePath

def clear_screen():
    """Clear the console screen based on the operating system."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def prompt_exit():
    """Prompt the user to press Enter to exit and clear the screen."""
    input("\nPress Enter to exit. ")
    clear_screen()

def add_password(passObject, arguments):
    """Add a password."""
    passObject.add_password("passwords.json", arguments[2], arguments[3], arguments[4], arguments[5])

def get_password(passObject, arguments):
    """Get a password."""
    diccio = passObject.get_password("passwords.json", arguments[2], arguments[3])
    if diccio:
        print(f"Service: {arguments[2].capitalize()}")
        print(f"Username: {diccio['username']}")
        print(f"Password: {diccio['password']}")
    else:
        print("Service not found or invalid master key.")
    prompt_exit()

def list_services(passObject):
    """List all services."""
    try:
        passwords = passObject.load_passwords("passwords.json")
        services = list(passwords.keys())
        if services:
            print("Services:")
            for i, service in enumerate(services):
                print(f"{i+1}. {service.capitalize()}")
        else:
            print("No services found.")
    except Exception as e:
        print(f"Error loading services: {e}")
    prompt_exit()

def drop_passwords(passObject):
    """Delete all passwords."""
    res = input("If you are sure you want to delete all passwords, type your master key and press Enter: ")
    if passObject.check_master_key("passwords.json", res):
        try:
            with open("passwords.json", "w") as f:
                f.write("{}")
            print("All passwords have been deleted.")
        except Exception as e:
            print(f"Error deleting passwords: {e}")
    else:
        print("Invalid master key.")
    prompt_exit()

def main() -> None:
    addIgnorePath("passwords.json")
    clear_screen()
    arguments = getArgs()
    passObject = Passgen()

    if len(arguments) <= 1:
        print("No arguments provided.")
        sys.exit(1)

    command = arguments[1]
    if command == "add" and len(arguments) == 6:
        add_password(passObject, arguments)
    elif command == "get" and len(arguments) == 4:
        get_password(passObject, arguments)
    elif command == "list":
        list_services(passObject)
    elif command == "drop":
        drop_passwords(passObject)
    else:
        print("Invalid arguments.")
        sys.exit(1)

if __name__ == "__main__":
    main()

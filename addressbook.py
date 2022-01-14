#!/usr/bin/python3 
import sys
class AddressBook:
    def print_help():
        print("A simple Address book CLI program\n"
        "Usage: adressbook [--help]\n\n"
        "Available commands:\n"
        "\tAdd\t")

def main():
    addressbook = AddressBook
    _argv = sys.argv

    #if no argument given or asking for help
    if len(_argv) < 2 or _argv[1].lower() == "help" or "--help":
        addressbook.print_help()
        return

if __name__ == "__main__":
    main()

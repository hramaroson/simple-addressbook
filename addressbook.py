#!/usr/bin/python3 
import sys
import argparse

class Contact:
    def __init__(self,firstname, lastname, address="", phone="", email=""):
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.phone = phone
        self.email = email

class AddressBook:
    _addressbook = []
    def print_help():
        print("A simple Address book CLI program\n"
        "Usage: adressbook.py [--help] <command> [<args>]\n\n"
        "Available commands:\n"             
        "\tadd\tAdd a contact to the adress book")

def main():
    addressbook = AddressBook

    parser = argparse.ArgumentParser(description="A Simple Python CLI program to manage Adress book")
    parser.add_argument("command", help="Command to execute", type=str.lower, choices = ["add"])
    parser.add_argument("-fn", "--firstname", type= str.lower, help="Contact first name")
    args = parser.parse_args()

    #Add a contact to the address
    if args.command == "add": 
        #Check if contact firstname is given
        _firstname = ""
        if args.firstname:
            if len(args.firstname) > 0:
                _firstname = args.firstname
        
        if len(_firstname)<1:
            print("{appname}:'{command}': Contact first name is required. See '{appname} help'"
                .format(appname=sys.argv[0], command=args.command))
            return
        

if __name__ == "__main__":
    main()

#!/usr/bin/python3 
import pickletools
import sys
import argparse
import pickle
import re

class Contact:
    def __init__(self,lastname="John", firstname="Doe", address="", phone="", email=""):
        self.lastname = lastname
        self.firstname = firstname
        self.address = address
        self.phone = phone
        self.email = email

class AddressBook:
    def __init__(self):
        self._addressbook = []
        file = None
        try:
            file = open("addressbook.data", "br")
        except: pass

        if file:
            self._addressbook = pickle.load(file)
            file.close()
    
    def print_help():
        print("A simple Address book CLI program\n"
        "Usage: adressbook.py [--help] <command> [<args>]\n\n"
        "Available commands:\n"             
        "\tadd\tAdd a contact to the adress book")

    def addContact(self, contact):
        if contact and isinstance(contact, Contact):
            self._addressbook.append(contact)
            
            #save to file
            file = open("addressbook.data","bw")
            if file:
                pickle.dump(self._addressbook, file)
                file.close()

            print("Contact has been added")
            print("-Last Name:\t ",contact.lastname)
            print("-First Name:\t ",contact.firstname)
            print("-Address:\t ",contact.address)
            print("-Phone number(s):\t ",contact.phone)
            print("-Email(s):\t ",contact.email)
    
   
    def _filter(self, item):

        return True

    def list(self, lastname=""):
        self._lastname = lastname
        _addressbook_filtered = filter(self._filter, self._addressbook)
        print("First Name\t|Last Name\t|Address\t|Phone Numbers(s)\t|Emails(s)")
        for _contact in _addressbook_filtered:
            print(_contact.firstname if len(_contact.firstname) > 0 else "-",end="\t\t")
            print(_contact.lastname if len(_contact.lastname) > 0 else "-", end="\t\t")
            print(_contact.address if len(_contact.address) > 0 else "-", end="\t\t")
            print(";".join(_contact.phone) if len(_contact.phone) > 0 else "-", end="\t\t")
            print(";".join(_contact.email) if len(_contact.email) > 0 else "-", end="\t\t")
            print("\n",end="")


def get_str_from_args_field(args_field):
    _str = ""
    if args_field:
        if len(args_field) > 0:
            _str = args_field
    return _str

def check_and_get_phonelist(command, phoneargs, phonelist):
    _phone = get_str_from_args_field(phoneargs)

    #check if phone number is valid
    _phone_list = []
    if len(_phone) > 0:
        _phone_list = _phone.split(';')
        for i in range(len(_phone_list)):
            if not re.search("^\\s*[+]?[0-9\\s]+\\s*$", _phone_list[i]):
                print("{appname}:'{command}': Bad phone number format '{badnumber}'. See '{appname} help'"
                    .format(appname=sys.argv[0].split("/")[-1], command=command, 
                    badnumber=_phone_list[i]))
                return False

            _phone_list[i] = _phone_list[i].replace(" ","") #remove all spaces (if any)

    phonelist = _phone_list
    return True

def main():
    addressbook = AddressBook()

    parser = argparse.ArgumentParser(description="A Simple Python CLI program to manage Adress book")
    parser.add_argument("command", help="Command to execute", type=str.lower, choices = ["add", "list"])
    parser.add_argument("-ln", "--lastname", type= str, help="Last name")
    parser.add_argument("-fn", "--firstname", type= str, help="First name")
    parser.add_argument("-a", "--address", type= str, help="Address")
    parser.add_argument("-p", "--phone", type= str, help="Phone number(s)")
    parser.add_argument("-e", "--email", type= str, help="Email address(s)")
    args = parser.parse_args()

    # Add a contact to the address
    if args.command == "add": 
        #Check if contact lastname is given
        lastname = get_str_from_args_field(args.lastname)
        firstname = get_str_from_args_field(args.firstname)
        
        if len(lastname)<1 and len(firstname) <1:
            print("{appname}:'{command}': At least one of Contact last name or first name should be given. See '{appname} help'"
                .format(appname=sys.argv[0].split("/")[-1], command=args.command))
            return
        
        _phone = get_str_from_args_field(args.phone)

        #check if phone number is valid
        _phone_list = []
        if not check_and_get_phonelist(args.command, args.phone, _phone_list):
            return
            
        _email = get_str_from_args_field(args.email)

        #check if email address is valid
        _email_list = []
        if len(_email) > 0:
            _email_list = _email.split(';')
            for i in range(len(_email_list)):
                if not re.search("^\\s*\w+@\w+.\w+\\s*$", _email_list[i]):
                    print("{appname}:'{command}': Bad phone email format '{bademail}'. See '{appname} help'"
                        .format(appname=sys.argv[0].split("/")[-1], command=args.command, 
                        bademail=_email_list[i]))
                    return

                _email_list[i] = _email_list[i].replace(" ","") #remove trailing spaces (if any)
    
        _contact = Contact(lastname=lastname, firstname= firstname)
        _contact.address = get_str_from_args_field(args.address)
        _contact.phone = _phone_list
        _contact.email = _email_list
        addressbook.addContact(_contact)
    
    # List contacts
    elif args.command == "list":
        addressbook.list()      


if __name__ == "__main__":
    main()

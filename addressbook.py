#!/usr/bin/python3 
import sys
import argparse
import pickle
import re

CGREEN  = '\33[32m'
CYELLOW = '\033[93m'
CRED = '\033[31m'
CBLUE = "\033[94m"
CEND =  "\033[0m"

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
            print(CBLUE)
            print("**********************")
            print("-Last Name:\t ",contact.lastname)
            print("-First Name:\t ",contact.firstname)
            print("-Address:\t ",contact.address)
            print("-Phone number(s):\t ",contact.phone)
            print("-Email(s):\t ",contact.email)
            print(CEND)

def get_str_from_args_field(args_field):
    _str = ""
    if args_field:
        if len(args_field) > 0:
            _str = args_field
    return _str

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

    #Add a contact to the address
    if args.command == "add": 
        #Check if contact lastname is given
        _lastname = get_str_from_args_field(args.lastname)
        _firstname = get_str_from_args_field(args.firstname)
        
        if len(_lastname)<1 and len(_firstname) <1:
            print(CRED, "{appname}:'{command}': At least one of Contact last name or first name should be given. See '{appname} help'"
                .format(appname=sys.argv[0].split("/")[-1], command=args.command), CEND)
            return
        
        _phone = get_str_from_args_field(args.phone)

        #check if phone number is valid
        _phone_list = []
        if len(_phone) > 0:
            _phone_list = _phone.split(';')
            for i in range(len(_phone_list)):
                if not re.search("^\\s*[+]?[0-9\\s]+\\s*$", _phone_list[i]):
                    print(CRED, "{appname}:'{command}': Bad phone number format '{badnumber}'. See '{appname} help'"
                        .format(appname=sys.argv[0].split("/")[-1], command=args.command, 
                        badnumber=_phone_list[i]), CEND)
                    return

                _phone_list[i] = _phone_list[i].replace(" ","") #remove all spaces (if any)
        
        _email = get_str_from_args_field(args.email)

        #check if email address is valid
        _email_list = []
        if len(_email) > 0:
            _email_list = _email.split(';')
            for i in range(len(_email_list)):
                if not re.search("^\\s*\w+@\w+.\w+\\s*$", _email_list[i]):
                    print(CRED, "{appname}:'{command}': Bad phone email format '{bademail}'. See '{appname} help'"
                        .format(appname=sys.argv[0].split("/")[-1], command=args.command, 
                        bademail=_email_list[i]), CEND)
                    return

                _email_list[i] = _email_list[i].replace(" ","") #remove trailing spaces (if any)
    
        _contact = Contact(lastname=_lastname, firstname= _firstname)
        _contact.address = get_str_from_args_field(args.address)
        _contact.phone = _phone_list
        _contact.email = _email_list
        addressbook.addContact(_contact)
        

if __name__ == "__main__":
    main()

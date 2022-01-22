#!/usr/bin/python3 
import difflib
import sys
import argparse
import pickle
import re

class Contact:
    def __init__(self,lastname="John", firstname="Doe", address="", phones=[], emails=[]):
        self.lastname = lastname
        self.firstname = firstname
        self.address = address
        self.phones = phones  
        self.emails = emails

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
            print("-Last Name:\t ",contact.lastname if len(contact.lastname) >0 else "-")
            print("-First Name:\t ",contact.firstname if len(contact.firstname) >0 else "-")
            print("-Address:\t ",contact.address if len(contact.address) >0 else "-")
            print("-Phone number(s):\t ",contact.phones if len(contact.phones) >0 else "-")
            print("-Email(s):\t ",contact.emails if len(contact.emails) >0 else "-")
    
   
    def _filter(self, item):
        if len(self._lastname) > 0 and (item is not None):
            if len(item.lastname) <=0 or (len(item.lastname) >0 \
                and item.lastname.lower() != self._lastname.lower()):
                return False

        if len(self._firstname) > 0 and (item is not None):
            if len(item.firstname) <=0 or (len(item.firstname) >0 \
                and item.firstname.lower() != self._firstname.lower()):
                return False
        
        if len(self._address) >0 and (item is not None):
            if len(item.address) <=0 or (len(item.address) >0 \
                and difflib.SequenceMatcher(a=self._address, b=item.address).ratio() < 0.1):
                return False

        if len(self._phones) > 0 and (item is not None) \
            and not any(i in self._phones for i in item.phones):
            return False

        if len(self._emails) > 0 and (item is not None) \
            and not any(i in self._emails for i in item.emails):
            return False

        return True

    def list(self, lastname="", firstname="", address="", phones=[], emails=[]): 
        self._lastname = lastname
        self._firstname = firstname
        self._address = address
        self._phones = phones
        self._emails = emails
        _addressbook_filtered = filter(self._filter, self._addressbook)
        
        print("First Name\t|Last Name\t|Address\t|Phone Numbers(s)\t|Emails(s)")
        for _contact in _addressbook_filtered:
            print(_contact.firstname if len(_contact.firstname) > 0 else "-",end="\t\t")
            print(_contact.lastname if len(_contact.lastname) > 0 else "-", end="\t\t")
            print(_contact.address if len(_contact.address) > 0 else "-", end="\t\t")
            print(";".join(_contact.phones) if len(_contact.phones) > 0 else "-", end="\t\t")
            print(";".join(_contact.emails) if len(_contact.emails) > 0 else "-", end="\t\t")
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
    phonelist[:] = _phone_list
    return True

def check_and_get_emaillist(command, emailargs, emaillist):
    _email = get_str_from_args_field(emailargs)

    #Check if email is valid
    _email_list = []
    if len(_email) > 0:
        _email_list = _email.split(';')
        for i in range(len(_email_list)):
            if not re.search("^\\s*\w+@\w+.\w+\\s*$", _email_list[i]):
                print("{appname}:'{command}': Bad phone email format '{bademail}'. See '{appname} help'"
                    .format(appname=sys.argv[0].split("/")[-1], command=command, 
                        bademail=_email_list[i]))
                return False
            _email_list[i] = _email_list[i].replace(" ","") #remove trailing spaces (if any)
    emaillist[:] = _email_list
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
        _lastname = get_str_from_args_field(args.lastname)
        _firstname = get_str_from_args_field(args.firstname)
        
        if len(_lastname)<1 and len(_firstname) <1:
            print("{appname}:'{command}': At least one of Contact last name or first name should be given. See '{appname} help'"
                .format(appname=sys.argv[0].split("/")[-1], command=args.command))
            return

        #check if phone number is valid
        _phone_list = []
        if not check_and_get_phonelist(args.command, args.phone, _phone_list):
            return

        #check if email address is valid
        _email_list = []
        if not check_and_get_emaillist(args.command, args.email, _email_list):
            return 

        _contact = Contact(lastname=_lastname, firstname= _firstname)
        _contact.address = get_str_from_args_field(args.address)
        _contact.phones = _phone_list
        _contact.emails = _email_list 
        addressbook.addContact(_contact)  
    
    # List contacts
    elif args.command == "list":
        _lastname = get_str_from_args_field(args.lastname)
        _firstname = get_str_from_args_field(args.firstname)

        _phone_list = []
        if not check_and_get_phonelist(args.command, args.phone, _phone_list): 
            return
        
        _email_list = []
        if not check_and_get_emaillist(args.command, args.email, _email_list):
            return 
        
        _address = get_str_from_args_field(args.address)

        addressbook.list(lastname=_lastname, firstname=_firstname, address= _address,
            phones=_phone_list, emails=_email_list)      

if __name__ == "__main__":
    main()

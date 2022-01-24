#!/usr/bin/python3 
import difflib
import sys
import argparse
import pickle
import re

CYELLOW = '\033[93m'
CGREEN  = '\33[32m'
CEND =  '\033[0m'

class Contact:
    def __init__(self,lastname="John", firstname="Doe", address= None, phones=[], emails=[]):
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

    def _saveToFile(self):
        #save _addressbook to file
        file = None 
        try:
            file = open("addressbook.data","bw")
        except:
            pass

        if file:
            pickle.dump(self._addressbook, file)
            file.close()

    def addContact(self, contact):
        if contact and isinstance(contact, Contact):
            self._addressbook.append(contact)
            
            self._saveToFile()

            print(f"{CGREEN}Contact has been added\n{CEND}")
            self._print_aligned("-Last Name: ")
            self._print_aligned(contact.lastname \
                if contact.lastname and len(contact.lastname) >0 else "-", end="\n")
            
            self._print_aligned("-First Name: ")
            self._print_aligned(contact.firstname \
                if contact.firstname and len(contact.firstname) >0 else "-", end="\n")
            
            self._print_aligned("-Address: ")
            self._print_aligned(contact.address \
                if contact.address and len(contact.address) >0 else "-", end="\n")
            
            self._print_aligned("-Phone number(s): ")
            self._print_aligned(str(contact.phones) \
                if contact.phones and len(contact.phones) >0 else "-", end="\n")

            self._print_aligned("-Email(s): ")
            self._print_aligned(str(contact.emails) \
                if contact.emails and len(contact.emails) >0 else "-", end="\n")
   
    def _filter(self, item):
        if item and self._contact.lastname:
            if len(self._contact.lastname.replace(" ",""))>0 \
                and (item.lastname is None or (item.lastname and len(item.lastname)<1)):
                return False
            if len(self._contact.lastname.replace(" ",""))<1 \
                and (item.lastname and len(item.lastname)>0):
                return False
            if item.lastname \
                and difflib.SequenceMatcher(a=self._contact.lastname, b=item.lastname).ratio()<0.5:
                return False
        
        if item and self._contact.firstname:
            if len(self._contact.firstname.replace(" ",""))>0 \
                and (item.firstname is None or (item.firstname and len(item.lastname)<1)):
                return False
            if len(self._contact.firstname.replace(" ",""))<1 \
                and (item.firstname and len (item.firstname)>0):
                return False 
            elif item.firstname \
                and difflib.SequenceMatcher(a=self._contact.firstname, b=item.firstname).ratio()<0.5:
                return False
        
        if item and self._contact.address:
            if len(self._contact.address.replace(" ",""))>0 \
                and (item.address is None or (item.address and len(item.address)<1)):
                return False
            if len(self._contact.address.replace(" ",""))<1 \
                and (item.address and len(item.address)>0):
                return False
            elif item.address \
                and difflib.SequenceMatcher(a=self._contact.address, b=item.address).ratio()<0.5:
                return False 

        if len(self._contact.phones) > 0 and (item is not None) \
            and not any(i in self._contact.phones for i in item.phones):
            return False

        if len(self._contact.emails) > 0 and (item is not None) \
            and not any(i.lower() in self._contact.emails for i in item.emails):
            return False

        return True 

    def _print_aligned(self, str, end=""):
        print(f"{str :20s} ",end=end) 

    def _list_d(self, contact_list): 
        print("\n", end="")
        self._print_aligned("| First Name")
        self._print_aligned("| Last Name")
        self._print_aligned("| Address")
        self._print_aligned("| Phone Number(s)")
        self._print_aligned("| Email(s)")
        print("\n", end="")

        for i in range (0, 5):
            self._print_aligned("____________")
        
        print("\n", end="")
       
        for _contact in contact_list:
            self._print_aligned(_contact.firstname \
                if (_contact.firstname and len(_contact.firstname) > 0) else "-") 
            self._print_aligned(_contact.lastname \
                if (_contact.lastname and len(_contact.lastname) > 0) else "-")
            self._print_aligned(_contact.address \
                if _contact.address and len(_contact.address) > 0 else "-")
            self._print_aligned(";".join(_contact.phones) \
                if len(_contact.phones) > 0 else "-")
            self._print_aligned(";".join(_contact.emails) \
                if len(_contact.emails) > 0 else "-")
            print("\n",end="")

    def list(self, contact): 
        self._contact = contact

        _addressbook_filtered = list(filter(self._filter, self._addressbook))
        _count = len(_addressbook_filtered)
        print(f"{CYELLOW}{_count} of {len(self._addressbook)} contact(s) listed{CEND}")
        if _count <1:
            return

        self._list_d(_addressbook_filtered)   
    
    def remove(self, contact): 
        self._contact = contact

        _addressbook_filtered = list(filter(self._filter, self._addressbook))
        _count = len(_addressbook_filtered)
        print(f"{CYELLOW}{_count} of {len(self._addressbook)} contact(s) to be removed{CEND}")
        if _count <1:
            print("Nothing to do!")
            return

        self._list_d(_addressbook_filtered) 
        print("\n",end="")

        while True:
            _validated="n"
            try:
                _validated = input("Do you want to remove this/these contact(s)? [y/n]: ").lower()
            except:
                pass

            if _validated == "n":
                print("Aborted.")
                return
            elif _validated == "y":
                # Remove contacts from _addressbook_filtered in _addressbook
                self._addressbook = [c for c in self._addressbook if c not in _addressbook_filtered]
                self._saveToFile()
                print(f"{CGREEN}{_count} contact(s) removed{CEND}")
                break
            else:
                print(f"Invalid answer '{_validated}'")

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
            if not re.search("^\\s*([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+\\s*$", _email_list[i]):
                print("{appname}:'{command}': Bad phone email format '{bademail}'. See '{appname} help'"
                    .format(appname=sys.argv[0].split("/")[-1], command=command, 
                        bademail=_email_list[i]))
                return False
            _email_list[i] = _email_list[i].strip().lower() #remove trailing spaces (if any)
    emaillist[:] = _email_list
    return True  

def main():
    addressbook = AddressBook()

    parser = argparse.ArgumentParser(description="A Simple Python CLI program to manage Adress book")
    parser.add_argument("command", help="Command to execute", type=str.lower, choices = ["add", "list", "remove"])
    parser.add_argument("-ln", "--lastname", type= str, help="Last name")
    parser.add_argument("-fn", "--firstname", type= str, help="First name")
    parser.add_argument("-a", "--address", type= str, help="Address")
    parser.add_argument("-p", "--phone", type= str, help="Phone number(s)")
    parser.add_argument("-e", "--email", type= str, help="Email address(s)")
    args = parser.parse_args()

    # Add a contact to the address
    if args.command == "add": 
        #Check if contact lastname is given
        _lastname = args.lastname
        _firstname = args.firstname
        
        if (_lastname is None or (_lastname and len(_lastname)<1)) \
            and (_firstname is None or (_firstname and len(_firstname)<1)):
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

        addressbook.addContact(Contact(lastname=_lastname, firstname= _firstname, \
            address=args.address, phones=_phone_list, emails=_email_list))  
    
    # List contacts
    elif args.command == "list":
        _phone_list = []
        if not check_and_get_phonelist(args.command, args.phone, _phone_list): 
            return
        
        _email_list = []
        if not check_and_get_emaillist(args.command, args.email, _email_list):
            return 
        
        addressbook.list(Contact(lastname=args.lastname, firstname=args.firstname, address= args.address,
            phones=_phone_list, emails=_email_list))   

    elif args.command == "remove":
        _phone_list = []
        if not check_and_get_phonelist(args.command, args.phone, _phone_list): 
            return
        
        _email_list = []
        if not check_and_get_emaillist(args.command, args.email, _email_list):
            return 
        addressbook.remove(Contact(lastname=args.lastname, firstname=args.firstname))  

if __name__ == "__main__":
    main()

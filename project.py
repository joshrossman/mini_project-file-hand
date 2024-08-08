import re
def read_file(my_file, contact_data):
    with open(my_file,"r") as file:
        contact_data={}
        for line in file:
            try:    
                contact_name, phone_key, phone_number, email_key,email_address, street_key,street_address, category_key, category, *extra =line.split(":")            
                contact_data[contact_name]={phone_key:phone_number, email_key:email_address, street_key:street_address, category_key:category.strip()}
            except Exception as e:
                if line=="\n":
                    line=''  
        return contact_data
    
def check_input_data(input_data,regex_pattern,error_message):
    while True:
        try:
            if re.match(regex_pattern,input_data):
                return input_data
                break
            else:
                input_data=input(error_message)
        except Exception as e:
            return print(f"Error: {e}, {error_message}")

def add_contact(contact_data):
    contact_name= check_input_data(input("Contact Name:"),r"[a-zA-Z0-9-_+\s]+\s[a-zA-Z0-9-_+\s]","Please input a valid, first and last name.")
    item_found=False
    for keys,items in contact_data.items():
        if keys.lower()==contact_name.lower():
            item_found=True
            print(f"Contact already in contact list!")
    if not item_found:       
        phone_number= check_input_data(input("Phone Number:"),r"^[\(]?\d{3}[\)]?-?\d{3}-?\d{4}\b","Please input a valid phone number.")
        email_address= check_input_data(input("Email address:"),r"^[A-Za-z0-9_\-\+%.]+@[\w]+\.\w{2,}$\b","Please input a valid email address.")
        street_address= check_input_data(input("Street address:"),r"^[0-9-]+\s\w+\s\w+\.?$","Please input a valid street address.")
        category=input("Please enter a category (eg: Friends, Work, Family, etc.)")
        contact_data[contact_name.lower()]={"Phone Number":phone_number, "Email Address":email_address.lower(), "Street Address":street_address.lower(), "Category":category.lower()}
     
def edit_contact(contact_data):
    display_contacts(contact_data)
    contact_name= input("Please enter the name of the contact you would like to edit:")
    contact_present=False
    try:
        for key in contact_data.keys():
            if re.match(key,contact_name, re.IGNORECASE):
                contact_data[contact_name.lower()]["Phone Number"]= check_input_data(input("Phone Number:"),r"^[\(]?\d{3}[\)]?-?\d{3}-?\d{4}\b","Please input a valid phone number.")
                contact_data[contact_name.lower()]["Email Address"]= check_input_data(input("Email address:"),r"^[A-Za-z0-9_\-\+%.]+@[\w]+\.\w{2,}$\b","Please input a valid email address.")
                contact_data[contact_name.lower()]["Street Address"]= check_input_data(input("Street address:"),r"^[0-9-]+\s\w+\s\w+\.?$","Please input a valid street address.")
                contact_data[contact_name.lower()]["Category"]=input("Please enter a category (eg: Friends, Work, Family, etc.)")
                contact_present=True
                print(contact_data)
    except Exception as e:
        print(f"Error: {e}. Was not able to make changes.")
        contact_present=True
    
    if not contact_present:
        print(f"Contact {contact_name} not present in contact list. Unable to make edits.")

def delete_contact(contact_data):
    contact_name= input("Please enter the name of the contact you would like to delete:")
    contact_present=False
    
    for key in contact_data.keys():
        if re.match(key,contact_name, re.IGNORECASE):
            contact_present=True
        
    if not contact_present:
        print(f"Contact {contact_name} not present in contact list.")
    else:
        final_answer=input(f"Are you sure that you would like to delete {contact_name}? This action cannot be undone. Y/N\n")
        if final_answer.lower()=="y" or final_answer.lower()=="yes":
            contact_data.pop(contact_name.lower())
    return contact_data

def search_for_contact(contact_data):
    search_name=input("Please type the full name that you would like to search for:")
    item_found=False
    for keys,items in contact_data.items():
        if keys.lower()==search_name.lower():
            item_found=True
            print(f"Contact Found!\nName: {keys}\n", end="")
            for key, item in items.items():
                print(f"{key}: {item}\n", end="")
    print("\n")
    if not item_found:
        print(f"Contact: {search_name} not found!")

def display_contacts(contact_data):
    for key, items in contact_data.items():
        print(f"\nName: {key}\n", end="")
        for inner_key, inner_item in items.items():
            print(f"{inner_key}: {inner_item}\n", end="")
               
def custom_search(contact_data):
        #Currently, will only produce the first matching result. Will no include other results once one match found.
        my_choice=input("How would you like to search?\nContact Name\nPhone Number\nEmail Address\nStreet Address\nCategory\n")
        my_search_choices=["Contact Name","Phone Number","Email Address","Street Address", "Category"]
        item_found=False
        if my_choice.lower()=="contact name":    
            search_for_contact(contact_data)
            item_found=True
        elif my_choice in my_search_choices:    
            my_new_choice=input(f"Please enter the {my_choice} you would like to search for")
            for key, item in contact_data.items():
                if re.match(my_new_choice,contact_data[key][my_choice], re.IGNORECASE):
                    print(f"Match Found!")
                    print(f"\nName: {key}\n", end="")
                    for inner_key, inner_item in contact_data[key].items():
                        print(f"{inner_key}: {inner_item}\n", end="")
                    item_found=True
            print("\n")
        else:
            print("Sorry! Not a valid choice. Please make sure the first letter of each word is capitalized")
            item_found=True
        
        if not item_found:
            print(f"Contact: {my_choice} not found!")
               
def backup_contacts(contact_data):
    print("Current Data:")
    display_contacts(contact_data)
    my_choice=input("[1]Backup Data or [2]Restore Data From Backup File")
    if my_choice=="1":
        try:
            new_file=input("Please enter the name of a the backup file you would like to create:")
            write_file(new_file,contact_data)
        except Exception as e:
            print(f"Error: {e}. Was unable to create backup file.")
    elif my_choice=="2":
        try:
            new_file=input("Please enter the name of a the backup file you would like to restore your data from.\nPlease make sure to check the data and documents before restoring. This action cannot be undone.")
            contact_data=read_file(new_file,contact_data)
            write_file("contact_data_storage.txt",contact_data)
            return contact_data    
            
        except Exception as e:
            print(f"Error: {e}. Was unable to restore file. Please make sure you inputted a correct document for restore.")
    else:
        print("Not a valid choice!")
    
def write_file(my_file,contact_data):
    with open(my_file,"w") as file:
        for keys, items in contact_data.items():
            file.write("\n"+keys+":")
            for key, item in items.items():
                new_data=key+":"+item+":"
                file.write(new_data)

def main():
    contact_data={}
    contact_data=read_file("contact_data_storage.txt", contact_data)
    
    while True:
        print("\nWelcome to the Contact Management System! What would you like to do today?")
        my_choice=input("\n1. Add a new contact.\n2. Edit an existing contact\n3. Delete a contact\n4. Search for a contact\n5. Display all contacts\n6. *Bonus* Backup Content\n7. Quit\n")
        
        if my_choice=="1" or my_choice.lower()=="add" or my_choice.lower()=="add a new contact": 
            add_contact(contact_data)
            write_file("contact_data_storage.txt",contact_data)
        elif my_choice=="2" or my_choice.lower()=="edit" or my_choice.lower()=="edit an exsisting contact":
            if len(contact_data)>0:
                edit_contact(contact_data)
            else:
                print("There are currently no contacts to edit.")
            write_file("contact_data_storage.txt",contact_data)
        elif my_choice=="3" or my_choice.lower()=="delete" or my_choice.lower()=="delete a contact":
            if len(contact_data)>0:
                delete_contact(contact_data)
            else:
                print("There are currently no contacts to delete.")
            write_file("contact_data_storage.txt",contact_data)
        elif my_choice=="4" or my_choice.lower()=="search" or my_choice.lower()=="search for a contact":
            while True:
                my_choice=input("[1] Search by name. [2] Custom search")
                if my_choice=="1":
                    search_for_contact(contact_data)
                    break
                elif my_choice=="2":
                    custom_search(contact_data)
                    break
                else:
                    print("Not a valid choice")
        elif my_choice=="5" or my_choice.lower()=="display" or my_choice.lower()=="display all contacts":
            display_contacts(contact_data)
        elif my_choice=="6" or my_choice.lower()=="backup" or my_choice.lower()=="backup content":
            backup_contacts(contact_data)
        elif my_choice=="7" or my_choice.lower()=="exit":
            break
        else:
            print("Not a valid choice. Please choose again.")

        
        
if __name__=="__main__":
    main()


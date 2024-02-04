from Phonebook.Addressbook import Record, AddressBook

phone_book = AddressBook()

instruction = ("Hello, I am a bot assistant for work with the phone book. \n"
               "Enter the command:\n"
               "'show all' - if you want to view the entire phone book.\n"
               "'show N' - if want to view the phone book in the parts by N contacts. N must be digit.\n"
               "'exit', 'close' or 'good bye' - if you want to finish the work.\n"
               "'add_contact name birthday' - if you want to add a contact to the phone book,\n"
               "for example 'add Tom_Waits 07-12-1949'. Birthday is an optional field.\n"
               "'add_phone name phone' - if you want to add a phone number to the contact.\n"
               "Phone must consist of 10 digits. You can add different phone numbers to the contact.\n"
               "'remove_phone name phone' - if you want to remove a phone number from the contact.\n"
               "'edit_phone name old_number new_number' - if you want to edit a phone number.\n"
               "'find_phone name number' - if yoy want to find a phone number in the contact.\n"
               "'days name' - if you want to know how many days are left until the contact's birthday.\n"
               "'find_user name' - if you want to find a definite user in the phone book.\n"
               "'delete_user name' - if you want to delete a contact from the phone book.\n"
               "'find_info text' - to find users by several digits of a phone number or several letters of a name.\n")


def input_error(func):
    def inner(x):
        try:
            result = func(x)
            return result
        except IndexError as Error:
            return Error
        except KeyError as Error:
            return Error
        except ValueError as Error:
            return Error
        except AttributeError as Error:
            return Error

    return inner


@input_error
def add_contact(contact):
    if not contact:
        raise ValueError("Give me user name please")
    elif not contact[0].isalpha():
        raise ValueError("Enter correct username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name):
            raise KeyError("Contact already exists")
        else:
            if len(contact) == 1:
                username_record = Record(name)
                phone_book.add_record(username_record)
                return f'Contact {name} has been added to the phone book'
            else:
                try:
                    birthday = contact[1]
                    username_record = Record(name, birthday)
                    phone_book.add_record(username_record)
                    return f'Contact {name} with birthday {birthday} has been added to the phone book'
                except ValueError:
                    raise ValueError('Invalid data format')


@input_error
def add_phone(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter phone please")
        else:
            try:
                phone = contact[1]
                phone_book.get(name).add_phone(phone)
                return f'Phone {phone} has been added to contact {name}'
            except ValueError:
                raise ValueError("Invalid phone number")


@input_error
def remove_phone(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter phone please")
        else:
            try:
                phone = contact[1]
                phone_book.get(name).remove_phone(phone)
                return f'Phone {phone} has been removed from contact {name}'
            except ValueError:
                raise ValueError("Invalid or non-existent phone number")


@input_error
def edit_phone(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) < 3:
            raise IndexError("Enter two phone number please")
        else:
            try:
                old_phone = contact[1]
                new_phone = contact[2]
                phone_book.get(name).edit_phone(old_phone, new_phone)
                return f'Phone number {old_phone} has been changed to {new_phone} for contact {name}'
            except ValueError:
                raise ValueError("Invalid or non-existent phone number")


@input_error
def find_phone(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        elif len(contact) == 1:
            raise IndexError("Enter phone please")
        else:
            try:
                phone = contact[1]
                phone_book.get(name).find_phone(phone)
                return phone
            except ValueError:
                raise ValueError("Invalid phone number")


@input_error
def days_to_birthday(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name) is None:
            raise KeyError("No such user in phone book")
        else:
            try:
                days = phone_book.get(name).days_to_birthday
                return days
            except AttributeError:
                raise AttributeError("No information about this user's birthday")


@input_error
def find_user(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        return phone_book.get(name)


@input_error
def delete_user(contact):
    if not contact:
        raise ValueError("Enter username please")
    else:
        name = contact[0].capitalize()
        if phone_book.get(name):
            phone_book.delete(name)
            return f'Contact {name} has been deleted from the phone book'


@input_error
def find_info(info):
    return phone_book.find_info(info[0])


def show_all():
    for key in phone_book.keys():
        print(phone_book[key])


@input_error
def show(contact):
    if not contact:
        raise IndexError("Enter a number of elements")
    n = int(contact[0])
    if n > len(phone_book):
        raise ValueError(f"This number is too big, length of phone book is {len(phone_book)}")
    else:
        page = phone_book.iterator(n)
        for elem in page:
            if elem:
                print(elem)



def final():
    return 'Good bye!'


def greeting():
    return instruction


command_dict1 = {"good bye": final, "close": final, "exit": final, "hello": greeting, "show all": show_all}

command_dict2 = dict(add_contact=add_contact, add_phone=add_phone, remove_phone=remove_phone, find_phone=find_phone,
                     edit_phone=edit_phone, days=days_to_birthday, find_user=find_user, delete_user=delete_user,
                     find_info=find_info, show=show)


def get_handler1(x):
    return command_dict1[x]


def get_handler2(x):
    return command_dict2[x]


def main():
    global phone_book
    try:
        phone_book = phone_book.read_from_file(filename='phone_book.bin')
    except FileNotFoundError:
        phone_book = AddressBook()
    while True:
        command = input().lower().strip()

        if command in command_dict1:
            result = get_handler1(command)()
            print(result)
            if result == "Good bye!":
                phone_book.save_to_file(filename='phone_book.bin')
                break
        else:
            command = command.split(" ")
            contact = command[1:]

            if command[0] in command_dict2:
                result = get_handler2(command[0])(contact)
                if result is not None:
                    print(result)
            else:
                print("This is an incorrect command. Try again, please")


if __name__ == "__main__":
    main()

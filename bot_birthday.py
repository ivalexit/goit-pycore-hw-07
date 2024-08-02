from typing import List, Dict
import sys
import os
from collections import UserDict
from datetime import datetime, timedelta


# Базовий клас для полів контакту
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для збереження імені контакту
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


# Клас для збереження та валідації номера телефону
class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return value.isdigit() and len(value) == 10


# Клас для збереження дати народження
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self):
        return self.value.strftime('%d.%m.%Y')


# Клас, який представляє запис у адресній книзі
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Додавання номера телефону
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Видалення номера телефону
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    # Редагування номера телефону
    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    # Пошук номера телефону
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    # Додавання дати народження
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

# Клас адресної книги
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    # Пошук контакту
    def find(self, name):
        return self.data.get(name)

    # Видалення контакту
    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False
    
    # Отримання найближчих днів народження
    def get_upcoming_birthdays(self):
        today = datetime.now()
        list_of_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)        
                
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                difference_in_days = (birthday_this_year - today).days
                
                if 0 <= difference_in_days <= 7:
                    # Перевірка, чи не випадає день народження на вихідні
                    if birthday_this_year.weekday() == 5:
                        congratulation_date = birthday_this_year + timedelta(days=2)
                    elif birthday_this_year.weekday() == 6:
                        congratulation_date = birthday_this_year + timedelta(days=1)
                    else:
                        congratulation_date = birthday_this_year

                    list_of_birthdays.append({ 
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        return list_of_birthdays

# Декоратор для обробки помилок
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone."
        except IndexError:
            return "Invalid command format. Use: add [name] [phone], change [name] [new_phone], phone [name]"
    return inner

# Додавання контакту з обробкою помилок
@input_error
def add_contact(book: AddressBook, args: str) -> str:
    parts = args
    name = parts[0]
    phones = parts[1:]
    if not name or not phones:
        raise ValueError
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    for p in phones:
        record.add_phone(p)
    return "Contact added."

# Зміна контакту з обробкою помилок
@input_error
def change_contact(book: AddressBook, name: str, old_phone: str, new_phone: str) -> str:
    record = book.find(name)
    if record and record.edit_phone(old_phone, new_phone):
        return "Contact updated."
    return "Contact not found."

# Показати номер телефону контакту з обробкою помилок
@input_error
def show_phone(book: AddressBook, name: str) -> str:
    record = book.find(name)
    if record:
        return ', '.join(phone.value for phone in record.phones)
    return "Contact not found."

# Показати всі контакти з обробкою помилок
@input_error
def show_all(book: AddressBook) -> str:
    if book:
        return "\n".join([str(record) for record in book.values()])
    return "No contacts found."

# Видалення контакту з обробкою помилок
@input_error
def remove_contact(book: AddressBook, name: str) -> str:
    if book.delete(name):
        return "Contact removed."
    return "Contact not found."

# Додавання дати народження з обробкою помилок
@input_error
def add_birthday(book: AddressBook, name: str, birthday: str) -> str:
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

# Показати дату народження та обробка помилок
@input_error
def show_birthday(book: AddressBook, name: str) -> str:
    record = book.find(name)
    if record and record.birthday:
        return f'Birthday: {record.birthday}'
    return "Contact not found."

# Показати найближчі дні народження з обробкою помилок
@input_error
def birthdays(book: AddressBook) -> str:
    records = book.get_upcoming_birthdays()
    if records:
        return '\n'.join(['Name: ' + str(record['name'])+'. Cong_date: '+str(record['congratulation_date']) for record in records])
    return 'No upcoming birthdays.'

# Парсинг вводу користувача
def parse_input(user_input: str) -> (str, List[str]):
    parts = user_input.strip().split(maxsplit=3)
    command = parts[0].lower()
    args = parts[1:]
    return command, args

# Головна функція
def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Menu:\n1- add\n2- change \n3- phone \n4- all \n5- remove\n6- add-birthday\n7- show-birthday\n8- birthdays\n9- exit or close\n10- hello\ncommand: ")
        command, args = parse_input(user_input)

        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(book, args))
        elif command == "change":
            print(change_contact(book, *args))
        elif command == "phone":
            print(show_phone(book, *args))
        elif command == "all":
            print(show_all(book))
        elif command == "remove":
            print(remove_contact(book, *args))
        elif command == "add-birthday":
            print(add_birthday(book, *args))
        elif command == "show-birthday":
            print(show_birthday(book, *args))
        elif command == "birthdays":
            print(birthdays(book))
        elif command in ("exit", "close"):
            print("Good bye!")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
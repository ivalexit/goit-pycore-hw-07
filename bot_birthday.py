from typing import Dict, List
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
            raise ValueError('Name cannot be empty')
        super().__init__(value)

# Клас для збереження та валідації номера телефону
class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError('Phone number must have 10 digits')
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
        
# Клас для запису в адресній книзі
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
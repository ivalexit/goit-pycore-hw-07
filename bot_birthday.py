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
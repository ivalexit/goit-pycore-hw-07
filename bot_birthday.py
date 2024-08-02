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
from random import sample
from secrets import choice
from string import *


def createRandomPassword(length):
    alphabet = ascii_letters + digits + punctuation
    requirements = [ascii_uppercase,        # at least one uppercase letter
                    ascii_lowercase,        # at least one lowercase letter
                    digits,                 # at least one digit
                    punctuation,            # at least one symbol
                    *(length-4)*[alphabet]]  # rest: letters digits and symbols
    return "".join(choice(req) for req in sample(requirements, length))

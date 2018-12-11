import re


def is_phone(phone):
    if re.match("^1[34578][0-9]{9}$", phone):
        return True
    return False

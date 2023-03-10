"""Imports"""
import calendar
import datetime
import random
import string


def shift_within_range(value, min, max, reverse=False):
    """Shift numeric value within range."""
    values = range(min, max + 1)
    if reverse:
        index = values.index(value) - 1
    else:
        index = values.index(value) + 1

    return values[index % len(values)]


def shift_date(value, reverse=False):
    """Shift date to a still-valid date."""
    year = int(shift(value.year, reverse))
    month = shift_within_range(value.month, 1, 12, reverse)
    day = shift_within_range(value.day, 1, calendar.monthrange(year, month)[1], reverse)
    return datetime.date(year, month, day)


def shift(value, reverse=False):
    """Shift value to a still-valid value."""""
    if not value:
        return value

    # shift datetime values

    if type(value) is datetime.datetime or type(value) is datetime.date:
        # if already date(time) type
        return shift_date(value, reverse)
    try:
        # if valid date as string, e.g., from form save
        return shift_date(datetime.datetime.strptime(value, '%Y-%m-%d'), reverse)
    except:  # noqa
        pass

    # shift string values

    shifted = []

    for char in str(value):
        try:
            ordinal = ord(char)

            if char.isdigit():
                min = ord('0')
                max = ord('9')
            elif ordinal in range(ord('A'), ord('Z') + 1):
                min = ord('A')
                max = ord('Z')
            elif ordinal in range(ord('a'), ord('z') + 1):
                min = ord('a')
                max = ord('z')

            shifted.append(chr(shift_within_range(ordinal, min, max, reverse)))

        except:  # noqa
            shifted.append(char)

    return ''.join(shifted)


def mask(value):
    """Shift characters/numbers/date values by one to mask the value of personal data."""
    return shift(value)


def unmask(value):
    """Shift characters/numbers/date values by one to recover the original value of masked data."""
    return shift(value, True)


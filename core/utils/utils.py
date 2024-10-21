from random import randint
from datetime import datetime

from rest_framework import serializers


def prevent_future_date_validator(value):
    """PREVENT SAVING DATE VALUE TO FUTURE DATE"""
    if value and value > datetime.now().date():
        raise serializers.ValidationError(
            code="nonFieldErrors",
            detail="future  date not allowed",
        )


def prevent_past_date_validator(value):
    """PREVENT SAVING DATE VALUE TO PAST DATE"""
    if value and value < datetime.now().date():
        raise serializers.ValidationError(
            code="nonFieldErrors",
            detail="past date not allowed",
        )


def random_with_N_digits(no_digits):
    range_start = 10 ** (no_digits - 1)
    range_end = (10**no_digits) - 1
    return randint(range_start, range_end)

# -*- coding: utf-8 -*-
import re


__all__ = (
    'is_valid_identifier',
)


VALID_ID_REGEX = re.compile("^(col\d{5,}\d*|m\d{4,})$")


def is_valid_identifier(id):
    """Validate that the given `id`."""
    return VALID_ID_REGEX.match(id) is not None

# -*- coding: utf-8 -*-
import re

import cnxml


__all__ = (
    'is_valid_identifier',
    'validate_content',
)


VALID_ID_REGEX = re.compile("^(col\d{5,}\d*|m\d{4,})$")


def is_valid_identifier(id):
    """Validate that the given `id`."""
    return VALID_ID_REGEX.match(id) is not None


def validate_content(obj):
    """Runs the correct validator for the given `obj`ect."""
    from .main import Collection, Module
    validator = {
        Collection: cnxml.validate_collxml,
        Module: cnxml.validate_cnxml,
    }[type(obj)]
    return validator(obj.file)

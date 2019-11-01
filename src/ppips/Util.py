#!/usr/bin/python3

from __future__ import annotations

def are_equals(a, b) -> bool:
    if isinstance(a, (int, float, bool, str)):
        if isinstance(b, (int, float, bool, str)):
            return a == b
        return False
    return a.is_equal(b)

#!/usr/bin/python3

from __future__ import annotations

from typing import Union

from .Util import are_equals

class VarsComparison:
    def __init__(self, left, right, comp_type: str) -> None:
        self.left = left
        self.right = right
        self.comp_type = comp_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.left!r}, {self.right!r}, {self.comp_type!r})"

    def __str__(self) -> str:
        if isinstance(self.left, (int, float)):
            left = str(self.left)
        else:
            left = self.left.get_expr(True)
        if isinstance(self.right, (int, float)):
            right = str(self.right)
        else:
            right = self.right.get_expr(True)
        
        return f"<{self.__class__.__name__}: {left} {self.comp_type} {right} >"

    def evaluate(self, vars_dict) -> Union[bool, VarsComparison]:
        if isinstance(self.left, (int, float)):
            left = self.left
        else:
            left = self.left(vars_dict)

        if isinstance(self.right, (int, float)):
            right = self.right
        else:
            right = self.right(vars_dict)
        
        if self.comp_type == "<":
            return left < right
        elif self.comp_type == "<=":
            return left <= right
        elif self.comp_type == "==":
            return left == right
        elif self.comp_type == "!=":
            return left != right
        elif self.comp_type == ">":
            return left > right
        elif self.comp_type == ">=":
            return left >= right
        else:
            raise RuntimeError("Undefined comparison.")

    def __call__(self, vars_dict) -> Union[bool, VarsComparison]:
        return self.evaluate(vars_dict)

    def __bool__(self) -> bool:
        return False
    
    def get_vars(self) -> set:
        vars = set()
        if not isinstance(self.left, (int, float)):
            if bool(self.left):
                vars.add(self.left)
            else:
                for l in self.left:
                    if not isinstance(l, (int, float)) and bool(l):
                        vars.add(l)
        if not isinstance(self.right, (int, float)):
            if bool(self.right):
                vars.add(self.right)
            else:
                for r in self.right:
                    if not isinstance(r, (int, float)) and bool(r):
                        vars.add(r)
        return vars

    def is_equal(self, other: VarsComparison) -> bool:
        assert isinstance(other, VarsComparison)
        if self.comp_type == other.comp_type:
            if are_equals(self.left, other.left) and are_equals(self.right, other.right):
                return True
        if self.comp_type == "==" and other.comp_type == "==":
            if are_equals(self.left, other.right) and are_equals(self.right, other.left):
                return True
        if self.comp_type == "!=" and other.comp_type == "!=":
            if are_equals(self.left, other.right) and are_equals(self.right, other.left):
                return True
        if self.comp_type == "<" and other.comp_type == ">":
            if are_equals(self.left, other.right) and are_equals(self.right, other.left):
                return True
        if self.comp_type == ">" and other.comp_type == "<":
            if are_equals(self.left, other.right) and are_equals(self.right, other.left):
                return True
        if self.comp_type == "<=" and other.comp_type == ">=":
            if are_equals(self.left, other.right) and are_equals(self.right, other.left):
                return True
        if self.comp_type == ">=" and other.comp_type == "<=":
            if are_equals(self.left, other.right) and are_equals(self.right, other.left):
                return True
        return False

    def _distribute_mult(self) -> None:
        # distribute multipications
        if not isinstance(self.left, (int, float)):
            self.left = self.left.distrubute_mul()
        if not isinstance(self.right, (int, float)):
            self.right = self.right.distrubute_mul()

    def _move_expressions_numbers(self) -> None:
        # simple numbers to right and expressions to left
        if not isinstance(self.left, (int, float)):
            self.right -= self.left.pop_numbers()
        else:
            self.right -= self.left
            self.left = 0
        if not isinstance(self.right, (int, float)):
            elements, something_left = self.right.pop_elements()
            self.left -= elements
            if not something_left:
                self.right = 0

        if self.right < 0:
            self.left = -self.left
            self.right = -self.right
            if self.comp_type == "<":
                self.comp_type = ">"
            elif self.comp_type == "<=":
                self.comp_type = ">="
            elif self.comp_type == ">":
                self.comp_type = "<"
            elif self.comp_type == ">=":
                self.comp_type = "<"

    def _sort_expressions(self) -> None:
        pass

    def redistribute(self) -> None:
        self._distribute_mult()
        self._move_expressions_numbers()
        self.left.group_same_expressions()
        self._sort_expressions()

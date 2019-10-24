#!/usr/bin/python3

from __future__ import annotations

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

    def evaluate(self, vars_dict) -> bool:
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
            raise RuntimeError()

    def __call__(self, vars_dict) -> bool:
        return self.evaluate(vars_dict)
       

class ComparableElement:
    def __lt__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, "<")
    def __le__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, "<=")
    def __eq__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, "==")
    def __ne__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, "!=")
    def __gt__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, ">")
    def __ge__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, ">=")

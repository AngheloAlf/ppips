#!/usr/bin/python3

from typing import overload

from .IntVariable import IntVar
from .MultiVar import MultiVar

class Optimize:
    @overload
    def __init__(self, objective:IntVar): ...
    def __init__(self, objective:MultiVar):
        if not isinstance(objective, IntVar) and not isinstance(objective, MultiVar):
            raise TypeError("Expected valid expression.")
        self.objective = objective

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.objective.get_expr(True)} >"
    
    def __call__(self, vars_dict:dict) -> int:
        return self.objective(vars_dict)


class Minimize(Optimize):
    @overload
    def __init__(self, objective:IntVar): ...
    def __init__(self, objective:MultiVar):
        super().__init__(objective)

class Maximize(Optimize):
    @overload
    def __init__(self, objective:IntVar): ...
    def __init__(self, objective:MultiVar):
        super().__init__(objective)

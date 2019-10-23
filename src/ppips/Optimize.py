#!/usr/bin/python3

from __future__ import annotations

from typing import overload, Union

from .IntVariable import IntVar
from .MultiVar import MultiVar

class Optimize:
    def __init__(self, objective: Union[IntVar, MultiVar]):
        if not isinstance(objective, IntVar) and not isinstance(objective, MultiVar):
            raise TypeError("Expected valid expression.")
        self.objective = objective

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.objective.get_expr(True)} >"
    
    def __call__(self, vars_dict:dict) -> Number:
        return self.objective(vars_dict)


class Minimize(Optimize):
    def __init__(self, objective: Union[IntVar, MultiVar]):
        super().__init__(objective)

class Maximize(Optimize):
    def __init__(self, objective: Union[IntVar, MultiVar]):
        super().__init__(objective)

Number = Union[int, float]

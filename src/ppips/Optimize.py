#!/usr/bin/python3

from __future__ import annotations

from typing import overload, Dict, Union

from .IntVariable import IntVar
from .MultiVar import MultiVar

Number = Union[int, float]
Element = Union[IntVar, Number]
ElementDict = Dict[Union[IntVar, str], Number]

class Optimize:
    def __init__(self, objective: Union[IntVar, MultiVar]) -> None:
        if not isinstance(objective, (IntVar, MultiVar)):
            raise TypeError("Expected valid expression.")
        self.objective = objective

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.objective.get_expr(True)} >"
    
    def __call__(self, vars_dict: ElementDict) -> Union[Element, MultiVar]:
        if isinstance(self.objective, (IntVar, MultiVar)):
            return self.objective(vars_dict)
        return self.objective
    
    def update(self, vars_dict: ElementDict) -> None:
        if isinstance(self.objective, (IntVar, MultiVar)):
            self.objective = self.objective(vars_dict)



class Minimize(Optimize):
    def __init__(self, objective: Union[IntVar, MultiVar]) -> None:
        super().__init__(objective)

class Maximize(Optimize):
    def __init__(self, objective: Union[IntVar, MultiVar]) -> None:
        super().__init__(objective)

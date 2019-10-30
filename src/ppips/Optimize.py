#!/usr/bin/python3

from __future__ import annotations

from typing import overload, Dict, Union

from .VarsOperations import ArithmeticElement, AbstractVar

Number = Union[int, float]
Element = Union[AbstractVar, Number]
ElementDict = Dict[Union[AbstractVar, str], Number]
ArithElement = Union[ArithmeticElement, Number]

class Optimize:
    def __init__(self, objective: ArithElement, default_optimal: Number) -> None:
        if isinstance(objective, (int, float)):
            raise ValueError("Can't optimize a number, expression needed..")
        if not isinstance(objective, ArithmeticElement):
            raise TypeError("Expected valid expression.")
        self.objective: ArithElement = objective
        self.default_optimal = default_optimal
        self.last_optimal = default_optimal

    def __str__(self) -> str:
        value = f"<{self.__class__.__name__}: "
        if isinstance(self.objective, (int, float)):
            value += f"{self.objective}"
        else:
            value += f"{self.objective.get_expr(True)}"
        value += " >"
        return value
    
    def __call__(self, vars_dict: ElementDict) -> ArithElement:
        if isinstance(self.objective, ArithmeticElement):
            return self.objective(vars_dict)
        return self.objective
    
    def update(self, vars_dict: ElementDict) -> None:
        if isinstance(self.objective, ArithmeticElement):
            self.objective = self.objective(vars_dict)
    
    def reset_optimal(self):
        self.last_optimal = self.default_optimal

    def is_optimal(self, other: Number) -> bool:
        return other == self.last_optimal

    def is_better_than_optimal(self, other: Number) -> bool:
        raise NotImplementedError()


class Minimize(Optimize):
    def __init__(self, objective: ArithElement) -> None:
        super().__init__(objective, float("inf"))

    def is_better_than_optimal(self, other: Number) -> bool:
        if other < self.last_optimal:
            self.last_optimal = other
            return True
        return False

class Maximize(Optimize):
    def __init__(self, objective: ArithElement) -> None:
        super().__init__(objective, -float("inf"))

    def is_better_than_optimal(self, other: Number) -> bool:
        if other > self.last_optimal:
            self.last_optimal = other
            return True
        return False

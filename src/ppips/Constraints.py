#!/usr/bin/python3

from __future__ import annotations

from typing import overload, List, Dict, Union

from .IntVariable import IntVar
from .MultiVar import MultiVar
from .VarsComparison import VarsComparison
from .Optimize import Optimize, Maximize, Minimize

class Constraints:
    def __init__(self) -> None:
        self.constr: List[VarsComparison] = list()

    def __str__(self):
        rest = f"<{self.__class__.__name__}:>"
        for i in self.constr:
            rest += f"\n\t{str(i)}"
        return rest
    
    def __iadd__(self, other: VarsComparison) -> Constraints:
        if isinstance(other, VarsComparison):
            self.constr.append(other)
            return self
        return NotImplemented
    
    def __isub__(self, other: Union[List[VarsComparison], VarsComparison]) -> Constraints:
        if isinstance(other, VarsComparison):
            self.constr.remove(other)
            return self
        elif isinstance(other, list):
            for i in other:
                self.constr.remove(i)
            return self
        return NotImplemented
    
    def evaluate(self, vars_dict) -> bool:
        for i in self.constr:
            evaluation = i(vars_dict)
            if isinstance(evaluation, bool) and not evaluation:
                return False
        return True

    def __call__(self, vars_dict) -> bool:
        return self.evaluate(vars_dict)

    def __iter__(self):
        for i in self.constr:
            yield i

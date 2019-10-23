#!/usr/bin/python3

from typing import overload, Dict

from .IntVariable import IntVar
from .MultiVar import MultiVar
from .VarsComparison import VarsComparison
from .Optimize import Optimize, Maximize, Minimize

class Constraints:
    pass

class Constraints:
    def __init__(self):
        self.constr = list()

    def __str__(self):
        rest = f"<{self.__class__.__name__}:>"
        for i in self.constr:
            rest += f"\n\t{str(i)}"
        return rest
    
    def __iadd__(self, other:VarsComparison) -> Constraints:
        if isinstance(other, VarsComparison):
            self.constr.append(other)
            return self
        return NotImplemented
    
    def evaluate(self, vars_dict) -> bool:
        for i in self.constr:
            evaluation = i(vars_dict)
            # print("\t", evaluation)
            if not evaluation:
                return False
        return True

    def __call__(self, vars_dict) -> bool:
        return self.evaluate(vars_dict)


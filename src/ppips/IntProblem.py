#!/usr/bin/python3

from typing import overload, List, Tuple, Dict, TypeVar

none_int = TypeVar("none_int", None, int)

from .IntVariable import IntVar, IntVarContainer
from .MultiVar import MultiVar
from .VarsComparison import VarsComparison
from .Constraints import Constraints
from .Optimize import Optimize, Maximize, Minimize

class IntProblem:
    def __init__(self, name:str, vars:List[IntVar]):
        self.name = name
        self.vars = list(vars)
        self.constraint = Constraints()
        self.objective = None

    def get_expr(self) -> str:
        return self.name

    def __str__(self):
        obje = f"\n\tObjective: {str(self.objective)}" if self.objective is not None else ""
        rest = str(self.constraint)
        vars_ = "\n\t".join(repr(x) for x in self.vars)

        return f"<{self.__class__.__name__}: {self.get_expr()!r}>{obje}\n\n\t{rest}\n\n\t{vars_}\n"

    def __iadd__(self, other: VarsComparison):
        if isinstance(other, VarsComparison):
            self.constraint += other
            return self
        return NotImplemented

    @overload
    def __ilshift__(self, other: IntVar): ...
    def __ilshift__(self, other: MultiVar):
        if isinstance(other, MultiVar):
            if self.objective is not None:
                print("Warning: this problem already has an objective function. Changing to the new one.")
            self.objective = other
            return self
        elif isinstance(other, IntVar):
            if self.objective is not None:
                print("Warning: this problem already has an objective function. Changing to the new one.")
            self.objective = other
            return self
        return NotImplemented

    def __imatmul__(self, other: Optimize):
        if isinstance(other, Optimize):
            if self.objective is not None:
                print("Warning: this problem already has an objective function. Changing to the new one.")
            self.objective = other
            return self
        return NotImplemented

    @overload
    def evaluate(self, vars_dict:Dict[str, int]) -> Tuple[bool, none_int]: ...
    def evaluate(self, vars_dict:Dict[IntVar, int]) -> Tuple[bool, none_int]:
        valid = self.constraint(vars_dict)
        if not valid:
            return (False, None)
        if self.objective is not None:
            return (True, self.objective(vars_dict))
        return (True, None)

    def solve(self, solutions_type:str="all") -> List[Dict[IntVar, int]]:
        # first
        # optimal
        # all
        solutions = list()
        actual = dict()
        vars_list = [IntVarContainer(x) for x in self.vars]
        i = 0
        maxi = -float("inf")
        mini = float("inf")
        while i >= 0 and i < len(vars_list):
            var = vars_list[i]
            was_instanced = var.instance_next()
            if not was_instanced:
                var.reset_instances()
                i -= 1
                continue
            actual[var.get_var()] = var.get_instanced()
            i += 1
            if self.constraint({}):
                if i == len(vars_list):
                    if solutions_type == "first":
                        solutions.append(actual)
                        break
                    elif solutions_type == "optimal":
                        actual_value = self.evaluate(actual)[1]
                        if isinstance(self.objective, Maximize):
                            if actual_value == maxi:
                                solutions.append(actual)
                            elif actual_value > maxi:
                                solutions = [actual]
                                maxi = actual_value
                        elif isinstance(self.objective, Minimize):
                            if actual_value == mini:
                                solutions.append(actual)
                            elif actual_value < mini:
                                solutions = [actual]
                                mini = actual_value
                    elif solutions_type == "all":
                        solutions.append(actual)
                    actual = dict(actual)
                    var.de_instance()
                    i -= 1
            else:
                i -= 1
                del actual[var.get_var()]

        [x.de_instance() for x in self.vars]

        if solutions_type == "all":
            if isinstance(self.objective, Maximize):
                solutions.sort(key=lambda x:-self.evaluate(x)[1])
            elif isinstance(self.objective, Minimize):
                solutions.sort(key=lambda x:self.evaluate(x)[1])


        return solutions

#!/usr/bin/python3

from __future__ import annotations

from typing import overload, List, Tuple, Dict, Union

from .IntVariable import IntVar, IntVarContainer
from .MultiVar import MultiVar
from .VarsComparison import VarsComparison
from .Constraints import Constraints
from .Optimize import Optimize, Maximize, Minimize

Number = Union[int, float]
Element = Union[IntVar, Number]
ElementDict = Dict[Union[IntVar, str], Number]

class IntProblem:
    def __init__(self, name: str, vars: List[IntVar]) -> None:
        self.name = name
        self.vars = list(vars)
        self.constraints = Constraints()
        self.objective: Union[Optimize, None] = None
        self.removed_vars: Dict[IntVar, Number] = dict()

    def get_expr(self) -> str:
        return self.name

    def __str__(self):
        obje = f"\n\tObjective: {str(self.objective)}" if self.objective is not None else ""
        rest = str(self.constraints)
        # vars_ = "\n\t".join(repr(x) for x in self.vars)
        vars_ = f"Variables: {len(str.vars)}"

        return f"<{self.__class__.__name__}: {self.get_expr()!r}>{obje}\n\n\t{rest}\n\n\t{vars_}\n"

    def __iadd__(self, other: VarsComparison) -> IntProblem:
        if isinstance(other, VarsComparison):
            self.constraints += other
            return self
        return NotImplemented

    def __imatmul__(self, other: Optimize) -> IntProblem:
        if isinstance(other, Optimize):
            if self.objective is not None:
                print("Warning: this problem already has an objective function. Changing to the new one.")
            self.objective = other
            return self
        return NotImplemented

    def evaluate(self, vars_dict: ElementDict) -> Tuple[bool, Union[Element, MultiVar, None]]:
        valid = self.constraints(vars_dict)
        if not valid:
            return (False, None)
        if self.objective is not None:
            return (True, self.objective(vars_dict))
        return (True, None)

    def compute_search_space(self) -> int:
        total = 1
        for i in self.vars:
            total *= len(i.get_domain())
        return total

    def _node_consistency_(self, var: IntVar, constr: VarsComparison) -> bool:
        """Apply node consistency to the var and returns True if just only 1 element is it's domain."""
        for i in set(var.get_domain()):
            if not constr(i):
                var.remove_from_domain(i)
        domain = var.get_domain()
        if len(domain) == 0:
            raise RuntimeError("Variable "+var.get_expr()+" has empty domain after node consistency.")
        elif len(domain) == 1:
            return True
        return False

    def node_consistency(self) -> None:
        removed_constr = list()
        for i in self.constraints:
            constr_vars = i.get_vars()
            if len(constr_vars) == 1:
                var = list(constr_vars)[0]
                if self._node_consistency_(var, i):
                    var_value = list(var.get_domain())[0]
                    if var in self.removed_vars and self.removed_vars[var] != var_value:
                        raise RuntimeError("Da fuck?")
                    self.removed_vars[var] = var_value
                    if var in self.vars: 
                        self.vars.remove(var)
                removed_constr.append(i)
        self.constraints -= removed_constr
        if len(removed_constr) > 0:
            self.constraints.update_constraints(self.removed_vars)
            if self.objective is not None:
                self.objective.update(self.removed_vars)


    def solve(self, solutions_type: str="all") -> List[ElementDict]:
        # first
        # optimal
        # all
        solutions: List[Dict[Union[IntVar, str], Number]] = list()
        actual: Dict[Union[IntVar, str], Number] = dict()
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
            instance = var.get_instanced()
            if isinstance(instance, (int, float)):
                actual[var.get_var()] = instance
            i += 1
            if self.constraints({}):
                if i == len(vars_list):
                    if solutions_type == "first":
                        solutions.append(actual)
                        break
                    elif solutions_type == "optimal":
                        actual_value: Number = self.evaluate(actual)[1]
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
                if var.get_var() in actual:
                    del actual[var.get_var()]

        for x in self.vars:
            x.de_instance()

        if solutions_type == "all":
            if isinstance(self.objective, Maximize):
                solutions.sort(key=lambda x: self.evaluate(x)[1], reverse=True)
            elif isinstance(self.objective, Minimize):
                solutions.sort(key=lambda x: self.evaluate(x)[1])

        solutions = [{**x, **self.removed_vars} for x in solutions]
        return solutions

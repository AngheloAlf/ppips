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
        vars_ = f"Variables: {len(self.vars)}"

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

    def get_constraints_for_var(self, var: IntVar, min_vars: int = 1, max_vars: int = 0) -> Set[VarsComparison]:
        constrs: Set[VarsComparison] = set()
        for i in self.constraints:
            constr_vars = i.get_vars()
            if var in constr_vars:
                if len(constr_vars)>=min_vars and (max_vars == 0 or len(constr_vars) <= max_vars):
                    constrs.add(i)
        return constrs

    def node_consistency(self) -> None:
        removed_constr = list()
        for i in self.constraints:
            constr_vars = i.get_vars()
            if len(constr_vars) == 1:
                var = list(constr_vars)[0]
                if node_consistency(var, i)[0]:
                    var_value = list(var.get_domain())[0]
                    if var in self.removed_vars:
                        if self.removed_vars[var] != var_value:
                            raise RuntimeError("Da fuck?")
                    else:
                        self.removed_vars[var] = var_value
                        if var in self.vars: 
                            self.vars.remove(var)
                removed_constr.append(i)
        self.constraints -= removed_constr
        if len(removed_constr) > 0:
            self.constraints.update_constraints(self.removed_vars)
            if self.objective is not None:
                self.objective.update(self.removed_vars)
    
    def arc_consistency(self) -> None:
        self.node_consistency()
        for i in self.vars:
            removed_constr = list()
            constr_queue: List[VarsComparison] = list(self.get_constraints_for_var(i, 2, 2))
            while len(constr_queue) > 0:
                popped = constr_queue.pop()
                popped_vars = list(popped.get_vars())
                j = popped_vars[0]
                k = popped_vars[1]
                has_solution1, has_solution2, amount1, amount2 = arc_consistency(k, j, popped)

                if has_solution1 and has_solution2:
                    # remove constraint if both has_solution
                    removed_constr.append(popped)

                if has_solution1:
                    # remove variable if has_solution1
                    var_value = list(k.get_domain())[0]
                    if k in self.removed_vars:
                        if self.removed_vars[k] != var_value:
                            raise RuntimeError("Da fuck?")
                    else:
                        self.removed_vars[k] = var_value
                        if k in self.vars: 
                            self.vars.remove(k)
                elif amount1 > 0:
                    constr_queue += list(self.get_constraints_for_var(k, 2, 2))

                if has_solution2:
                    # remove variable if has_solution2
                    var_value = list(j.get_domain())[0]
                    if j in self.removed_vars:
                        if self.removed_vars[j] != var_value:
                            raise RuntimeError("Da fuck?")
                    else:
                        self.removed_vars[j] = var_value
                        if j in self.vars: 
                            self.vars.remove(j)
                elif amount2 > 0:
                    constr_queue += list(self.get_constraints_for_var(j, 2, 2))

            # remove constraints
            self.constraints -= removed_constr
            # update constraints
            self.constraints.update_constraints(self.removed_vars)
            if self.objective is not None:
                # update objective
                self.objective.update(self.removed_vars)
            self.node_consistency()


    def generate_graph(self) -> Dict[IntVar, Set[IntVar]]:
        graph: Dict[IntVar, Set[IntVar]] = dict()
        for i in self.constraints:
            constr_vars = i.get_vars()
            if len(constr_vars) >= 2:
                for j in constr_vars:
                    if j not in graph:
                        graph[j] = set()
                    graph[j] |= constr_vars - {j}
        return graph


    def solve(self, solutions_type: str="first") -> List[ElementDict]:
        # first, optimal, all
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

def node_consistency(var: IntVar, constr: VarsComparison) -> Tuple[bool, int]:
    """Apply node consistency to the var, and returns True if just only 1 element is left in it's domain, and the amount of removed values."""
    assert(len(constr.get_vars()) == 1)
    values_removed = 0
    for i in set(var.get_domain()):
        if not constr(i):
            var.remove_from_domain(i)
            values_removed += 1
    domain = var.get_domain()
    if len(domain) == 0:
        raise RuntimeError("Variable "+var.get_expr()+" has empty domain after node consistency.")
    return (len(domain) == 1, values_removed)

def arc_consistency(var1: IntVar, var2: IntVar, constr: VarsComparison) -> Tuple[bool, bool, int, int]:
    """Apply arc consistency to both vars, and returns True if just only 1 element is left for each of it's domains, and the amount of removed values for each variable."""
    assert(len(constr.get_vars()) == 2)
    values_removed_1 = 0
    for i in set(var1.get_domain()):
        remove = True
        for j in set(var2.get_domain()):
            if constr({var1: i, var2: j}):
                remove = False
                break
        if remove:
            var1.remove_from_domain(i)
            values_removed_1 += 1

    values_removed_2 = 0
    for j in set(var2.get_domain()):
        remove = True
        for i in set(var1.get_domain()):
            if constr({var1: i, var2: j}):
                remove = False
                break
        if remove:
            var2.remove_from_domain(j)
            values_removed_2 += 1
    
    domain1 = var1.get_domain()
    domain2 = var2.get_domain()
    if len(domain1) == 0:
        raise RuntimeError("Variable "+var1.get_expr()+" has empty domain after arc consistency.")
    elif len(domain2) == 0:
        raise RuntimeError("Variable "+var2.get_expr()+" has empty domain after arc consistency.")
    return (len(domain1) == 1, len(domain2) == 1, values_removed_1, values_removed_2)
    
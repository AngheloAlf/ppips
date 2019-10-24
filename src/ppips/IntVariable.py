#!/usr/bin/python3

from __future__ import annotations

from typing import overload, List, Dict, Set, Union, Optional, Iterable

from .VarsComparison import VarsComparison, ComparableElement
from .MultiVar import MultiVar

# https://docs.python.org/3/reference/datamodel.html

class IntVar(ComparableElement):
    def __init__(self, name: str, domain: Iterable[Number]) -> None:
        self.name: str = name
        if len(domain) == 0:
            raise RuntimeError("Domain can't be empty")
        self.domain: Set[Number] = set(domain)
        self.value_instanced: Optional[Number] = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.domain!r})"

    def get_expr(self, *params) -> str:
        return self.name

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.get_expr()!r}>"

    def __hash__(self):
        return hash(self.name)

    def get_domain(self) -> Set[Number]:
        return self.domain
    
    def instance_value(self, value: Number) -> None:
        if not self.is_valid(value):
            raise RuntimeError("Value not in domain")
        self.value_instanced = value
    
    def de_instance(self) -> None:
        self.value_instanced = None

    def __call__(self, value: Union[Number, ElementDict] = None) -> Element:
        if value is None and self.value_instanced is None:
            return self
        elif isinstance(value, (int, float)):
            if not self.is_valid(value):
                raise RuntimeError(f"Value must be part of {self.name}'s domain.")
            return value
        elif isinstance(value, dict) and self in value:
            out = value[self]
            if not self.is_valid(out):
                raise RuntimeError(f"Value must be part of {self.name}'s domain.")
            return out
        elif self.value_instanced is not None:
            if not self.is_valid(self.value_instanced):
                raise RuntimeError(f"Value must be part of {self.name}'s domain.")
            return self.value_instanced
        else:
            return self


    def __add__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=self, second=other)
        return NotImplemented

    def __radd__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=other, second=self)
        return NotImplemented


    def __sub__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=self, second=-other)
        return NotImplemented

    def __rsub__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=other, second=-self)
        return NotImplemented


    def __mul__(self, other: Element) -> IntVarMult:
        if isinstance(other, (IntVar, int, float)):
            return IntVarMult(first=self, second=other)
        return NotImplemented

    def __rmul__(self, other: Element) -> IntVarMult:
        if isinstance(other, (IntVar, int, float)):
            return IntVarMult(first=other, second=self)
        return NotImplemented

    
    def __truediv__(self, other: Element) -> IntVarDiv:
        if isinstance(other, (IntVar, int, float)):
            return IntVarDiv(first=self, second=other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, (IntVar, int, float)):
            return IntVarDiv(first=other, second=self)
        return NotImplemented


    def __neg__(self) -> IntVarMult:
        return IntVarMult(first=-1, second=self)


    def is_valid(self, value: Union[Number, ElementDict]) -> bool:
        return value in self.domain


class IntVarAdds(MultiVar):
    def __init__(self, /, var_list:list=None, first=None, second=None) -> None:
        super().__init__(" + ", var_list=var_list, first=first, second=second)

    def evaluate(self, vars_dict: ElementDict) -> ArithElement:
        result: Number = 0
        for var in self.elements:
            if isinstance(var, (int, float)):
                result += var
            else:
                result += var(vars_dict)
        return result


    def __add__(self, other: ArithElement) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(var_list=self.elements+[other])
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(var_list=self.elements+other.elements)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(var_list=self.elements+[other])
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(var_list=self.elements+[other])
        return NotImplemented


    def __radd__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(var_list=[other]+self.elements)
        return NotImplemented


    def __sub__(self, other: ArithElement) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(var_list=self.elements+[-other])
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(var_list=self.elements+[-other])
        elif isinstance(other, IntVarMult):
            return IntVarAdds(var_list=self.elements+[-other])
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(var_list=self.elements+[-other])
        return NotImplemented

    def __rsub__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=other, second=-self)
        return NotImplemented


    def __mul__(self, other: ArithElement) -> IntVarMult:
        if isinstance(other, (IntVar, int, float)):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarMult(first=self, second=other)
        return NotImplemented

    def __rmul__(self, other: Element) -> IntVarMult:
        if isinstance(other, (IntVar, int, float)):
            return IntVarMult(first=other, second=self)
        return NotImplemented


    def __truediv__(self, other: ArithElement) -> IntVarDiv:
        if isinstance(other, (IntVar, int, float)):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(first=self, second=other)
        return NotImplemented

    def __rtruediv__(self, other: Element) -> IntVarDiv:
        if isinstance(other, (IntVar, int, float)):
            return IntVarDiv(first=other, second=self)
        return NotImplemented


    def __neg__(self) -> IntVarMult:
        return IntVarMult(first=-1, second=self)


class IntVarMult(MultiVar):
    def __init__(self, /, var_list:list=None, first=None, second=None) -> None:
        super().__init__("*", var_list=var_list, first=first, second=second, parenthesis=False)

    def evaluate(self, vars_dict:ElementDict) -> ArithElement:
        result = 1
        for var in self.elements:
            if type(var) == int:
                result *= var
            else:
                result *= var(vars_dict)
        return result


    def __add__(self, other: ArithElement) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=self, second=other)
        return NotImplemented

    def __radd__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=other, second=self)
        return NotImplemented


    def __sub__(self, other: ArithElement) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=self, second=-other)
        return NotImplemented

    def __rsub__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=other, second=-self)
        return NotImplemented


    def __mul__(self, other: ArithElement) -> IntVarMult:
        if isinstance(other, (IntVar, int, float)):
            return IntVarMult(var_list=self.elements+[other])
        elif isinstance(other, IntVarAdds):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarMult(var_list=self.elements+other.elements)
        elif isinstance(other, IntVarDiv):
            return IntVarMult(first=self, second=other)
        return NotImplemented

    def __rmul__(self, other: Element) -> IntVarMult:
        if isinstance(other, (IntVar, int, float)):
            return IntVarMult(var_list=[other]+self.elements)
        return NotImplemented


    def __truediv__(self, other: ArithElement) -> IntVarDiv:
        if isinstance(other, (IntVar, int, float)):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(first=self, second=other)
        return NotImplemented

    def __rtruediv__(self, other: Element) -> IntVarDiv:
        if isinstance(other, (IntVar, int, float)):
            return IntVarDiv(first=other, second=self)
        return NotImplemented


    def __neg__(self) -> IntVarMult:
        self.elements.insert(0, -1)
        return self


class IntVarDiv(MultiVar):
    def __init__(self, /, var_list:list=None, first=None, second=None) -> None:
        super().__init__("/", var_list=var_list, first=first, second=second)

    def evaluate(self, vars_dict:ElementDict) -> ArithElement:
        result: Number = 1
        var = self.elements[0]
        if isinstance(var, (int, float)):
            result *= var
        else:
            result *= var(vars_dict)
        for var in self.elements[1:]:
            if isinstance(var, (int, float)):
                result /= var
            else:
                result /= var(vars_dict)
        return result


    def __add__(self, other: ArithElement) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=self, second=other)
        return NotImplemented

    def __radd__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=other, second=self)
        return NotImplemented


    def __sub__(self, other: ArithElement) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=self, second=-other)
        return NotImplemented

    def __rsub__(self, other: Element) -> IntVarAdds:
        if isinstance(other, (IntVar, int, float)):
            return IntVarAdds(first=other, second=-self)
        return NotImplemented


    def __mul__(self, other: ArithElement) -> IntVarMult:
        if isinstance(other, (IntVar, int, float)):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarMult(first=self, second=other)
        return NotImplemented

    def __rmul__(self, other: Element) -> IntVarMult:
        if isinstance(other, (IntVar, int, float)):
            return IntVarMult(first=other, second=self)
        return NotImplemented


    def __truediv__(self, other: ArithElement) -> IntVarDiv:
        if isinstance(other, (IntVar, int, float)):
            return IntVarDiv(var_list=self.elements+[other])
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(var_list=self.elements+other.elements)
        return NotImplemented

    def __rtruediv__(self, other: Element) -> IntVarDiv:
        if isinstance(other, (IntVar, int, float)):
            return IntVarDiv(first=other, second=self)
        return NotImplemented
    

    def __neg__(self) -> IntVarMult:
        return IntVarMult(first=-1, second=self)


class IntVarContainer:
    def __init__(self, var: IntVar) -> None:
        self.var = var
        self.domain = list(var.domain)
        self.pos = 0
    
    def instance_next(self) -> bool:
        if self.pos >= len(self.domain):
            return False
        self.var.instance_value(self.domain[self.pos])
        self.pos += 1
        return True
    
    def de_instance(self) -> None:
        self.var.de_instance()
        return
    
    def reset_instances(self) -> None:
        self.de_instance()
        self.pos = 0
        return
    
    def get_var(self) -> IntVar:
        return self.var
    
    def get_instanced(self) -> Element:
        return self.var()


Number = Union[int, float]
Element = Union[IntVar, Number]
ArithElement = Union[Element, MultiVar]
ElementDict = Dict[Union[IntVar, str], Number]

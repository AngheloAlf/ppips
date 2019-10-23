#!/usr/bin/python3

from typing import overload, List, Dict, Set

from .VarsComparison import VarsComparison, ComparableElement
from .MultiVar import MultiVar


class IntVar(ComparableElement):
    pass
class IntVarAdds(MultiVar):
    pass
class IntVarMult(MultiVar):
    pass
class IntVarDiv(MultiVar):
    pass

# https://docs.python.org/3/reference/datamodel.html

class IntVar(ComparableElement):
    def __init__(self, name:str, domain:Set[int]):
        self.name = name
        if len(domain) == 0:
            raise RuntimeError("Domain can't be empty")
        self.domain = set(domain)
        self.value_instanced = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.domain!r})"

    def get_expr(self, *params) -> str:
        return self.name

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.get_expr()!r}>"

    def __hash__(self):
        return hash(self.name)

    def get_domain(self) -> Set[int]:
        return self.domain
    
    def instance_value(self, value:int) -> int:
        if not self.is_valid(value):
            raise RuntimeError("Value not in domain")
        self.value_instanced = value
    
    def de_instance(self) -> None:
        self.value_instanced = None
    
    @overload
    def __call__(self, value:int) -> int: ...
    @overload
    def __call__(self, value:Dict[IntVar, int]) -> int: ...
    def __call__(self, value = None):
        if value is None and self.value_instanced is None:
            raise RuntimeError("Value not provided")
        elif type(value)==int:
            if not self.is_valid(value):
                raise RuntimeError(f"Value must be part of {self.name}'s domain.")
            return value
        elif type(value) == dict and self in value:
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

    @overload
    def __add__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __add__(self, other: int) -> IntVarAdds: ...
    def __add__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=self, second=other)
        elif type(other) == int:
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return NotImplemented
        return NotImplemented

    @overload
    def __radd__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __radd__(self, other: int) -> IntVarAdds: ...
    def __radd__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=other, second=self)
        elif type(other) == int:
            return IntVarAdds(first=other, second=self)
        elif isinstance(other, IntVarAdds):
            return NotImplemented
        return NotImplemented


    @overload
    def __sub__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __sub__(self, other: int) -> IntVarAdds: ...
    def __sub__(self, other):
        if isinstance(other, IntVar):
            # second = IntVarMult(first=-1, second=other)
            return IntVarAdds(first=self, second=-other)
        elif type(other) == int:
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarAdds):
            return NotImplemented
        return NotImplemented

    @overload
    def __rsub__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __rsub__(self, other: int) -> IntVarAdds: ...
    def __rsub__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=other, second=-self)
        elif type(other) == int:
            return IntVarAdds(first=other, second=-self)
        elif isinstance(other, IntVarAdds):
            return NotImplemented
        return NotImplemented


    @overload
    def __mul__(self, other: IntVar) -> IntVarMult: ...
    @overload
    def __mul__(self, other: int) -> IntVarMult: ...
    def __mul__(self, other):
        if isinstance(other, IntVar):
            return IntVarMult(first=self, second=other)
        elif type(other) == int:
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return NotImplemented
        return NotImplemented

    @overload
    def __rmul__(self, other: IntVar) -> IntVarMult: ...
    @overload
    def __rmul__(self, other: int) -> IntVarMult: ...
    def __rmul__(self, other):
        if isinstance(other, IntVar):
            return IntVarMult(first=other, second=self)
        elif type(other) == int:
            return IntVarMult(first=other, second=self)
        elif isinstance(other, IntVarMult):
            return NotImplemented
        return NotImplemented

    
    def __truediv__(self, other):
        if isinstance(other, IntVar):
            return IntVarDiv(first=self, second=other)
        elif type(other) == int:
            return IntVarDiv(first=self, second=other)
        elif type(other) == float:
            return IntVarDiv(first=self, second=other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, IntVar):
            return IntVarDiv(first=other, second=self)
        elif type(other) == int:
            return IntVarDiv(first=other, second=self)
        elif type(other) == float:
            return IntVarDiv(first=other, second=self)
        return NotImplemented


    def __neg__(self) -> IntVarMult:
        return IntVarMult(first=-1, second=self)

    def is_valid(self, value:int)->bool:
        return value in self.domain


class IntVarAdds(MultiVar):
    # def __init__(self, /, var_list:List[IntVar]=None, first:IntVar=None, second:IntVar=None):
    def __init__(self, /, var_list:list=None, first=None, second=None):
        super().__init__(" + ", var_list=var_list, first=first, second=second)

    # def evaluate(self, vars_dict:dict) -> int:
    def evaluate(self, vars_dict:Dict[IntVar, int]) -> int:
        result = 0
        for var in self.elements:
            if type(var) == int:
                result += var
            else:
                result += var(vars_dict)
        return result

    @overload
    def __add__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __add__(self, other: IntVarAdds) -> IntVarAdds: ...
    @overload
    def __add__(self, other: IntVarMult) -> IntVarAdds: ...
    @overload
    def __add__(self, other: int) -> IntVarAdds: ...
    def __add__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(var_list=self.elements+[other])
        elif type(other) == int:
            return IntVarAdds(var_list=self.elements+[other])
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(var_list=self.elements+other.elements)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(var_list=self.elements+[other])
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(var_list=self.elements+[other])
        return NotImplemented

    @overload
    def __radd__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __radd__(self, other: IntVarAdds) -> IntVarAdds: ...
    @overload
    def __radd__(self, other: IntVarMult) -> IntVarAdds: ...
    @overload
    def __radd__(self, other: int) -> IntVarAdds: ...
    def __radd__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(var_list=[other]+self.elements)
        elif type(other) == int:
            return IntVarAdds(var_list=[other]+self.elements)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(var_list=other.elements+self.elements)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(var_list=[other]+self.elements)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(var_list=[other]+self.elements)
        return NotImplemented


    @overload
    def __sub__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __sub__(self, other: IntVarAdds) -> IntVarAdds: ...
    @overload
    def __sub__(self, other: IntVarMult) -> IntVarAdds: ...
    @overload
    def __sub__(self, other: int) -> IntVarAdds: ...
    def __sub__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(var_list=self.elements+[-other])
        elif type(other) == int:
            return IntVarAdds(var_list=self.elements+[-other])
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(var_list=self.elements+[-other])
        elif isinstance(other, IntVarMult):
            return IntVarAdds(var_list=self.elements+[-other])
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(var_list=self.elements+[-other])
        return NotImplemented

    @overload
    def __rsub__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __rsub__(self, other: IntVarAdds) -> IntVarAdds: ...
    @overload
    def __rsub__(self, other: IntVarMult) -> IntVarAdds: ...
    @overload
    def __rsub__(self, other: int) -> IntVarAdds: ...
    def __rsub__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=other, second=-self)
        elif type(other) == int:
            return IntVarAdds(first=other, second=-self)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=other, second=-self)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=other, second=-self)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=other, second=-self)
        return NotImplemented


    @overload
    def __mul__(self, other: IntVar) -> IntVarMult: ...
    @overload
    def __mul__(self, other: IntVarMult) -> IntVarMult: ...
    @overload
    def __mul__(self, other: IntVarAdds) -> IntVarMult: ...
    @overload
    def __mul__(self, other: int) -> IntVarMult: ...
    def __mul__(self, other):
        if isinstance(other, IntVar):
            return IntVarMult(first=self, second=other)
        elif type(other) == int:
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarMult(first=self, second=other)
        return NotImplemented

    @overload
    def __rmul__(self, other: IntVar) -> IntVarMult: ...
    @overload
    def __rmul__(self, other: IntVarMult) -> IntVarMult: ...
    @overload
    def __rmul__(self, other: IntVarAdds) -> IntVarMult: ...
    @overload
    def __rmul__(self, other: int) -> IntVarMult: ...
    def __rmul__(self, other):
        if isinstance(other, IntVar):
            return IntVarMult(first=other, second=self)
        elif type(other) == int:
            return IntVarMult(first=other, second=self)
        elif isinstance(other, IntVarAdds):
            return IntVarMult(first=other, second=self)
        elif isinstance(other, IntVarMult):
            return IntVarMult(first=other, second=self)
        elif isinstance(other, IntVarDiv):
            return IntVarMult(first=other, second=self)
        return NotImplemented


    def __truediv__(self, other):
        if isinstance(other, IntVar):
            return IntVarDiv(first=self, second=other)
        elif type(other) == int:
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(first=self, second=other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, IntVar):
            return IntVarDiv(first=other, second=self)
        elif type(other) == int:
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(first=other, second=self)
        return NotImplemented

    def __neg__(self) -> IntVarMult:
        return IntVarMult(first=-1, second=self)


class IntVarMult(MultiVar):
    # def __init__(self, /, var_list:List[IntVar]=None, first:IntVar=None, second:IntVar=None):
    def __init__(self, /, var_list:list=None, first=None, second=None):
        super().__init__("*", var_list=var_list, first=first, second=second, parenthesis=False)

    # def evaluate(self, vars_dict:dict) -> int:
    def evaluate(self, vars_dict:Dict[IntVar, int]) -> int:
        result = 1
        for var in self.elements:
            if type(var) == int:
                result *= var
            else:
                result *= var(vars_dict)
        return result

    @overload
    def __mul__(self, other: IntVar) -> IntVarMult: ...
    @overload
    def __mul__(self, other: IntVarMult) -> IntVarMult: ...
    @overload
    def __mul__(self, other: IntVarAdds) -> IntVarMult: ...
    @overload
    def __mul__(self, other: int) -> IntVarMult: ...
    def __mul__(self, other):
        if isinstance(other, IntVar):
            return IntVarMult(var_list=self.elements+[other])
        elif type(other) == int:
            return IntVarMult(var_list=self.elements+[other])
        elif isinstance(other, IntVarAdds):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarMult(var_list=self.elements+other.elements)
        elif isinstance(other, IntVarDiv):
            return IntVarMult(first=self, second=other)
        return NotImplemented

    @overload
    def __rmul__(self, other: IntVar) -> IntVarMult: ...
    @overload
    def __rmul__(self, other: IntVarMult) -> IntVarMult: ...
    @overload
    def __rmul__(self, other: IntVarAdds) -> IntVarMult: ...
    @overload
    def __rmul__(self, other: int) -> IntVarMult: ...
    def __rmul__(self, other):
        if isinstance(other, IntVar):
            return IntVarMult(var_list=[other]+self.elements)
        elif type(other) == int:
            return IntVarMult(var_list=[other]+self.elements)
        elif isinstance(other, IntVarAdds):
            return IntVarMult(fist=other, second=self.elements)
        elif isinstance(other, IntVarMult):
            return IntVarMult(var_list=other.elements+self.elements)
        elif isinstance(other, IntVarDiv):
            return IntVarMult(first=other, second=self)
        return NotImplemented


    @overload
    def __add__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __add__(self, other: IntVarAdds) -> IntVarAdds: ...
    @overload
    def __add__(self, other: IntVarMult) -> IntVarAdds: ...
    @overload
    def __add__(self, other: int) -> IntVarAdds: ...
    def __add__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=self, second=other)
        elif type(other) == int:
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=self, second=other)
        return NotImplemented

    @overload
    def __radd__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __radd__(self, other: IntVarAdds) -> IntVarAdds: ...
    @overload
    def __radd__(self, other: IntVarMult) -> IntVarAdds: ...
    @overload
    def __radd__(self, other: int) -> IntVarAdds: ...
    def __radd__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=other, second=self)
        elif type(other) == int:
            return IntVarAdds(first=other, second=self)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=other, second=self)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=other, second=self)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=other, second=self)
        return NotImplemented


    @overload
    def __sub__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __sub__(self, other: IntVarAdds) -> IntVarAdds: ...
    @overload
    def __sub__(self, other: IntVarMult) -> IntVarAdds: ...
    @overload
    def __sub__(self, other: int) -> IntVarAdds: ...
    def __sub__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=self, second=-other)
        elif type(other) == int:
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=self, second=-other)
        return NotImplemented

    @overload
    def __rsub__(self, other: IntVar) -> IntVarAdds: ...
    @overload
    def __rsub__(self, other: IntVarAdds) -> IntVarAdds: ...
    @overload
    def __rsub__(self, other: IntVarMult) -> IntVarAdds: ...
    @overload
    def __rsub__(self, other: int) -> IntVarAdds: ...
    def __rsub__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=other, second=-self)
        elif type(other) == int:
            return IntVarAdds(first=other, second=-self)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=other, second=-self)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=other, second=-self)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=other, second=-self)
        return NotImplemented


    def __truediv__(self, other):
        if isinstance(other, IntVar):
            return IntVarDiv(first=self, second=other)
        elif type(other) == int:
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(first=self, second=other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, IntVar):
            return IntVarDiv(first=other, second=self)
        elif type(other) == int:
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(first=other, second=self)
        return NotImplemented


    def __neg__(self) -> IntVarMult:
        self.elements.insert(0, -1)
        return self


class IntVarDiv(MultiVar):
    # def __init__(self, /, var_list:List[IntVar]=None, first:IntVar=None, second:IntVar=None):
    def __init__(self, /, var_list:list=None, first=None, second=None):
        super().__init__("/", var_list=var_list, first=first, second=second, parenthesis=True)

    # def evaluate(self, vars_dict:dict) -> int:
    def evaluate(self, vars_dict:Dict[IntVar, int]) -> int:
        result = 1
        var = self.elements[0]
        if type(var) in (int, float):
            result *= var
        else:
            result *= var(vars_dict)
        for var in self.elements[1:]:
            if type(var) in (int, float):
                result /= var
            else:
                result /= var(vars_dict)
        return result

    def __add__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=self, second=other)
        elif type(other) == int:
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=self, second=other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, IntVar):
            return IntVarAdds(first=self, second=-other)
        elif type(other) == int:
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarDiv):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarMult):
            return IntVarAdds(first=self, second=-other)
        elif isinstance(other, IntVarAdds):
            return IntVarAdds(first=self, second=-other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, IntVar):
            return IntVarMult(first=self, second=other)
        elif type(other) == int:
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarDiv):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarMult):
            return IntVarMult(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarMult(first=self, second=other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, IntVar):
            return IntVarDiv(var_list=self.elements+[other])
        elif type(other) == int:
            return IntVarDiv(var_list=self.elements+[other])
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(var_list=self.elements+other.elements)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=self, second=other)
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=self, second=other)
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, IntVar):
            return IntVarDiv(first=other, second=self)
        elif type(other) == int:
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarDiv):
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarMult):
            return IntVarDiv(first=other, second=self)
        elif isinstance(other, IntVarAdds):
            return IntVarDiv(first=other, second=self)
        return NotImplemented
    

    def __neg__(self) -> IntVarMult:
        return IntVarMult(first=-1, second=self)


class IntVarContainer:
    def __init__(self, var:IntVar):
        self.var = var
        self.domain = list(var.domain)
        self.pos = 0
    
    def instance_next(self) -> bool:
        if self.pos >= len(self.domain):
            return False
        self.var.instance_value(self.domain[self.pos])
        self.pos += 1
        return True
    
    def de_instance(self):
        self.var.de_instance()
    
    def reset_instances(self) -> None:
        self.de_instance()
        self.pos = 0
    
    def get_var(self):
        return self.var
    
    def get_instanced(self):
        return self.var()

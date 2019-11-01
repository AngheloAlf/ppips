#!/usr/bin/python3

from __future__ import annotations

from typing import overload, List, Dict, Set, Union, Optional, Collection, Any

from .VarsComparison import VarsComparison
from .Util import are_equals

# https://docs.python.org/3/reference/datamodel.html

Number = Union[int, float]


class ArithmeticElement:
    def __add__(self, other: ArithElement) -> AddType:
        if other == 0:
            return self
        if isinstance(other, (ArithmeticElement, int, float)):
            return VarAdds(first=self, second=other)
        return NotImplemented
    
    def __radd__(self, other: Element) -> AddType:
        if other == 0:
            return self
        if isinstance(other, (int, float)):
            return VarAdds(first=other, second=self)
        return NotImplemented


    def __sub__(self, other: ArithElement) -> AddType:
        if other == 0:
            return self
        if isinstance(other, (ArithmeticElement, int, float)):
            return VarAdds(first=self, second=-other)
        return NotImplemented

    def __rsub__(self, other: Element) -> AddType:
        if other == 0:
            return -self
        if isinstance(other, (int, float)):
            return VarAdds(first=other, second=-self)
        return NotImplemented


    def __mul__(self, other: ArithElement) -> MultType:
        if other == 0:
            return 0
        if other == 1:
            return self
        if isinstance(other, (ArithmeticElement, int, float)):
            return VarMult(first=self, second=other)
        return NotImplemented

    def __rmul__(self, other: Element) -> MultType:
        if other == 0:
            return 0
        if other == 1:
            return self
        if isinstance(other, (int, float)):
            return VarMult(first=other, second=self)
        return NotImplemented


    def __truediv__(self, other: ArithElement) -> DivType:
        if other == 0:
            raise ZeroDivisionError()
        if other == 1:
            return self
        if isinstance(other, (ArithmeticElement, int, float)):
            return VarDiv(first=self, second=other)
        return NotImplemented

    def __rtruediv__(self, other: Element) -> DivType:
        if other == 0:
            return 0
        if isinstance(other, (int, float)):
            return VarDiv(first=other, second=self)
        return NotImplemented


    def __pow__(self, other: Element) -> PowType:
        if other == 0:
            return 1
        if other == 1:
            return self
        if isinstance(other, (ArithmeticElement, int, float)):
            return VarPow(first=self, second=other)
        return NotImplemented

    def __rpow__(self, other: Element) -> PowType:
        if other == 0:
            return 0
        if other == 1:
            return 1
        if isinstance(other, (int, float)):
            return VarPow(first=other, second=self)
        return NotImplemented


    def __mod__(self, other: Element) -> ModType:
        if other == 0:
            raise ZeroDivisionError()
        if isinstance(other, (ArithmeticElement, int, float)):
            return VarMod(first=self, second=other)
        return NotImplemented

    def __rmod__(self, other: Element) -> ModType:
        if other == 0:
            return 0
        if isinstance(other, (ArithmeticElement, int, float)):
            return VarMod(first=other, second=self)
        return NotImplemented


    def __neg__(self) -> MultType:
        return VarMult(first=-1, second=self)


    def __lt__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, "<")
    def __le__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, "<=")
    def __eq__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, "==")
    def __ne__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, "!=")
    def __gt__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, ">")
    def __ge__(self, other):
        if(isinstance(other, VarsComparison)):
            raise RuntimeError()
        return VarsComparison(self, other, ">=")

    def __bool__(self) -> bool:
        return False

    
    def get_expr(self, disable_last_parenthesis: bool=False) -> str:
        raise NotImplementedError()
    def __call__(self, value) -> ArithElement:
        raise NotImplementedError()


class AbstractVar(ArithmeticElement):
    def __init__(self, name: str) -> None:
        self.name: str = name

    def __repr__(self) -> str:
        return str(self)

    def get_expr(self, disable_last_parenthesis: bool=False) -> str:
        return self.name

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.get_expr()!r}>"

    def __hash__(self):
        return hash(self.name)

    def __call__(self, value: Union[Number, ElementDict] = None) -> Element:
        if value is None:
            return self
        elif isinstance(value, (int, float)):
            self.validate(value)
            return value
        elif isinstance(value, dict) and self in value:
            out = value[self]
            self.validate(out)
            return out
        else:
            return self

    def validate(self, value: Number) -> None:
        raise NotImplementedError()

    def __bool__(self) -> bool:
        return True

    def __iter__(self):
        yield self
    
    def is_equal(self, other: AbstractVar) -> bool:
        if not isinstance(other, AbstractVar):
            return False
        return self.name == other.name


class MultiVar(ArithmeticElement):
    def __init__(self, simbol: str, /, var_list: list=None, first=None, second=None, parenthesis: bool=True) -> None:
        self.simbol = simbol
        self.parenthesis = parenthesis
        if first is not None and second is not None:
            if var_list is not None:
                raise RuntimeError()
            self.elements = [first, second]
        elif var_list is not None:
            if first is not None or second is not None:
                raise RuntimeError()
            self.elements = list(var_list)
        else:
            raise RuntimeError()

    def __repr__(self):
        return f"{self.__class__.__name__}(var_list={self.elements!r})"

    def get_expr(self, disable_last_parenthesis=False) -> str:
        result = []
        for i in self.elements:
            if type(i) in (int, float):
                result.append(str(i))
            else:
                result.append(i.get_expr())
        expression = self.simbol.join(result)
        if self.parenthesis and not disable_last_parenthesis:
            return f"({expression})"
        return expression

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.get_expr(True)}>"
    
    def evaluate(self, vars_dict: ElementDict):
        raise NotImplementedError()
    
    def __call__(self, vars_dict: ElementDict) -> ArithElement:
        return self.evaluate(vars_dict)

    def __iter__(self):
        for i in self.elements:
            if isinstance(i, (int, float)):
                yield i
            else:
                for j in i:
                    yield j
        
    def is_equal(self, other):
        if not isinstance(other, MultiVar):
            return False
        if self.simbol != other.simbol:
            return False
        if len(self.elements) != len(other.elements):
            return False
        for i in range(len(self.elements)):
            a = self.elements[i]
            b = self.elements[i]
            if not are_equals(a, b):
                return False
        return True


class VarAdds(MultiVar):
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


    def __add__(self, other: ArithElement) -> AddType:
        if other == 0:
            return self
        if isinstance(other, VarAdds):
            return VarAdds(var_list=self.elements+other.elements)
        elif isinstance(other, (ArithmeticElement, int, float)):
            return VarAdds(var_list=self.elements+[other])
        return super().__add__(other)

    def __radd__(self, other: Element) -> AddType:
        if other == 0:
            return self
        if isinstance(other, (AbstractVar, int, float)):
            return VarAdds(var_list=[other]+self.elements)
        return NotImplemented


    def __sub__(self, other: ArithElement) -> AddType:
        if other == 0:
            return self
        if isinstance(other, (ArithmeticElement, int, float)):
            return VarAdds(var_list=self.elements+[-other])
        return NotImplemented


class VarMult(MultiVar):
    def __init__(self, /, var_list:list=None, first=None, second=None) -> None:
        super().__init__("*", var_list=var_list, first=first, second=second, parenthesis=False)

    def evaluate(self, vars_dict:ElementDict) -> ArithElement:
        result: Number = 1
        for var in self.elements:
            if isinstance(var, (int, float)):
                result *= var
            else:
                result *= var(vars_dict)
        return result


    def __mul__(self, other: ArithElement) -> MultType:
        if other == 0:
            return 0
        if other == 1:
            return self
        if isinstance(other, (AbstractVar, int, float)):
            return VarMult(var_list=self.elements+[other])
        elif isinstance(other, VarMult):
            return VarMult(var_list=self.elements+other.elements)
        return super().__mul__(other)

    def __rmul__(self, other: Element) -> MultType:
        if other == 0:
            return 0
        if other == 1:
            return self
        if isinstance(other, (AbstractVar, int, float)):
            return VarMult(var_list=[other]+self.elements)
        return NotImplemented


    def __neg__(self) -> MultType:
        self.elements.insert(0, -1)
        return self


class VarDiv(MultiVar):
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


    def __truediv__(self, other: ArithElement) -> DivType:
        if other == 0:
            raise ZeroDivisionError()
        if other == 1:
            return self
        if isinstance(other, (AbstractVar, int, float)):
            return VarDiv(var_list=self.elements+[other])
        elif isinstance(other, VarDiv):
            return VarDiv(var_list=self.elements+other.elements)
        return super().__truediv__(other)


class VarPow(MultiVar):
    def __init__(self, /, var_list:list=None, first=None, second=None) -> None:
        super().__init__("**", var_list=var_list, first=first, second=second)

    def evaluate(self, vars_dict: ElementDict) -> ArithElement:
        result: Number = 1
        var = self.elements[0]
        if isinstance(var, (int, float)):
            result = var
        else:
            result = var(vars_dict)
        for var in self.elements[1:]:
            if isinstance(var, (int, float)):
                result = result ** var
            else:
                result = result ** var(vars_dict)
        return result


class VarMod(MultiVar):
    def __init__(self, /, var_list: list=None, first=None, second=None) -> None:
        super().__init__("%", var_list=var_list, first=first, second=second)

    def evaluate(self, vars_dict: ElementDict) -> ArithElement:
        result: Number = 1
        var = self.elements[0]
        if isinstance(var, (int, float)):
            result = var
        else:
            result = var(vars_dict)
        for var in self.elements[1:]:
            if isinstance(var, (int, float)):
                result = result % var
            else:
                result = result % var(vars_dict)
        return result


Element = Union[AbstractVar, Number]
ArithElement = Union[ArithmeticElement, Number]

ElementDict = Dict[Union[AbstractVar, str], Number]

AddType = Union[ArithmeticElement, Number, VarAdds]
MultType = Union[ArithmeticElement, Number, VarMult]
DivType = Union[ArithmeticElement, Number, VarDiv]
PowType = Union[ArithmeticElement, Number, VarPow]
ModType = Union[ArithmeticElement, Number, VarMod]

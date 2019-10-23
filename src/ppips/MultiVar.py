#!/usr/bin/python3

from .VarsComparison import VarsComparison, ComparableElement

class MultiVar(ComparableElement):
    def __init__(self, simbol:str, /, var_list:list=None, first=None, second=None, parenthesis=True):
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
            if type(i) == int:
                result.append(str(i))
            else:
                result.append(i.get_expr())
        expression = self.simbol.join(result)
        if self.parenthesis and not disable_last_parenthesis:
            return f"({expression})"
        return expression

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.get_expr(True)}>"
    
    def __call__(self, vars_dict:dict) -> int:
        return self.evaluate(vars_dict)

#!/usr/bin/python3

from __future__ import annotations

from typing import List, Dict, Set, Union, Optional, Collection

from .VarsOperations import AbstractVar

# https://docs.python.org/3/reference/datamodel.html

Number = Union[int, float]
ElementDict = Dict[Union[AbstractVar, str], Number]

class IntVar(AbstractVar):
    def __init__(self, name: str, domain: Collection[Number]) -> None:
        super().__init__(name)
        if len(domain) == 0:
            raise RuntimeError("Domain can't be empty")
        self.domain: Set[Number] = set(domain)
        self.value_instanced: Optional[Number] = None

    def __repr__(self) -> str:
        return str(self)
        expr = f"<{self.__class__.__name__}: {self.get_expr()!r}>\n\t\\Domain: {self.domain}/"
        if self.value_instanced is not None:
            expr += f"\n\t\\Instanced: {self.value_instanced}/"
        return expr

    def get_domain(self) -> Set[Number]:
        return self.domain
    
    def remove_from_domain(self, value: Number) -> None:
        self.domain.remove(value)
    
    def instance_value(self, value: Number) -> None:
        self.validate(value)
        self.value_instanced = value
    
    def de_instance(self) -> None:
        self.value_instanced = None

    def __call__(self, value: Union[Number, ElementDict] = None) -> Element:
        if value is None and self.value_instanced is None:
            return self
        elif isinstance(value, (int, float)):
            self.validate(value)
            return value
        elif isinstance(value, dict) and self in value:
            out = value[self]
            self.validate(out)
            return out
        elif self.value_instanced is not None:
            self.validate(self.value_instanced)
            return self.value_instanced
        else:
            return self

    def validate(self, value: Union[Number, ElementDict]) -> None:
        if value not in self.domain:
            raise ValueError(f"Value must be part of {self.name}'s domain.")

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
        inst = self.var()
        assert isinstance(inst, (int, float))
        return inst

Element = Union[IntVar, Number]

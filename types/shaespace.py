#!/bin/python3

#> Imports
import typing
from types import SimpleNamespace
#</Imports

#> Header >/
__all__ = ('SlottedSpaceType', 'SlottedSpace', 'ShaeSpace', 'slotted_ShaeSpace')

class _SlottedSpaceTypeMeta(type):
    def __subclasscheck__(cls, other: type) -> bool:
        assert getattr(other, '__class__', None) is type, 'Use isinstance instead!'
        return hasattr(other, '_slottedspace_attrs_') and hasattr(other, '_slottedspace_name_')
    def __instancecheck__(cls, instance: typing.Any):
        assert getattr(instance, '__class__', None) is not type, 'Use issubclass instead!'
        return hasattr(instance, '_slottedspace_attrs_') and hasattr(instance, '_slottedspace_name_')

class SlottedSpaceType(metaclass=_SlottedSpaceTypeMeta):
    '''Creates a namespace with a preset __slots__ attribute'''
    def __new__(cls, *attrs: str, name: str = 'SlottedSpace') -> type:
        return type(name, (cls,), {'__slots__': attrs, '_slottedspace_attrs_': attrs, '_slottedspace_name_': name})
class SlottedSpace(metaclass=_SlottedSpaceTypeMeta):
    '''Creates and instantiates a namespace with a preset __slots__ attribute'''
    def __new__(cls, *attrs: str, name: str = 'SlottedSpace') -> SlottedSpaceType:
        return SlottedSpaceType(*attrs, name=name)()

def ShaeSpace(cls: type):
    '''A decorator to turn a class('s __dict__) into a SimpleNamespace'''
    ns = SimpleNamespace()
    ns._shaespace_attrs_ = tuple(k for k in cls.__dict__ if not k.startswith('_'))
    for a in ns._shaespace_attrs_: setattr(ns, a, getattr(cls, a))
    return ns
def slotted_ShaeSpace(cls: type):
    '''A decorator to turn a class('s __dict__) into a SlottedSpace'''
    ns = SlottedSpace(*(k for k in cls.__dict__ if not k.startswith('_')), name=cls.__qualname__)
    for a in ns._slottedspace_attrs_: setattr(ns, a, getattr(cls, a))
    return ns

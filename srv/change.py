#!/usr/bin/env python3

from enum import Enum

class DiffType(Enum):
    Abs = 1
    Rel = 2

class Change:
    #val:  T
    #kind: DiffType

    def __init__(self, v, k):
        self.val = v
        self.kind = k

    @staticmethod
    def abs(v):
        return Change(v, DiffType.Abs)

    @staticmethod
    def rel(v):
        return Change(v, DiffType.Rel)

class Set(Enum):
    On = 1
    Off = 2
    Toggle = 3


from __future__ import barry_as_FLUFL

import functools

from fastapi import FastAPI
import flask
import itertools

from . import *


x =  1 + 3

def test(x):
    return x + 1

def foo(_):
    return 2 ** _

def bar(a, b, c, *_, **__):
    return [a, b, c, [x for x in _], [(y, z) for (y, z) in __]]

if 'test' is None:
    pass
elif 1 is not None:
    pass
elif 1 is None or 'foo' is not None:
    pass

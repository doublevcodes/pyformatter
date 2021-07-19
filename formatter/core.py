from __future__ import annotations
from __future__ import barry_as_FLUFL

from os import environ
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
import starlette
import sys

from . import *


class Formatter:

    def __init__(self) -> None:
        pass
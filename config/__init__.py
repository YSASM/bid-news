import os

from .config import Config


Config.load(Config.env())

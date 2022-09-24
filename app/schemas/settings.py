from enum import Enum


class Environment(str, Enum):
    production: str = "production"
    development: str = "development"

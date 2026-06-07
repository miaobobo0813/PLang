from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    MODIFIER = auto()
    SYMBOL = auto()
    OPERATOR = auto()
    NUMBER = auto()
    TEXT = auto() 
    BOOLEAN = auto()
    TYPE = auto()
    EOF = auto()  

@dataclass
class Token:
    type: TokenType
    value: str
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}')"
    
KEYWORDS = {
    'using', 'loop', 'vars', 'ter', 'operators'
}

SYMBOLS = "()[]{};,."
OPERATORS = {
    '+', '-', '*', '`', '%', '=', '<', '>', '&', '/', '~'
}
SPECIAL_OPERATORS = {
    '</=', '>/='
}
TYPES = {
    'number', 'dotNum', 'text', 'boolean'
}
BOOLEANS = {
    'yes', 'no'
}
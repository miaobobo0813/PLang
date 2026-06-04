from dataclasses import dataclass
from enum import Enum, auto
from modules import *

class TokenType(Enum):
    KEYWORD = auto()
    MODIFIER = auto()
    SYMBOL = auto()
    NUMBER = auto()
    TEXT = auto() 
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
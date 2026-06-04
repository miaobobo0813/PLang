from dataclasses import dataclass
from typing import Any, List

@dataclass
class numberNode:
    value: float

@dataclass
class textNode:
    value: str

@dataclass
class boolNode:
    value: bool

@dataclass
class varsNode:
    name: str

@dataclass
class varsNewNode:
    name: str
    value: Any
    type: str

@dataclass
class varsModifyNode:
    name: str
    value: Any

@dataclass
class opNode:
    operator: str
    left: Any
    right: Any

@dataclass
class generalNode:
    keyword: str
    modifier: str
    args: List[Any]

@dataclass
class loopWhileNode:
    condition: Any
    body: List[Any]

@dataclass
class loopForNode:
    var: str
    rangeFrom: Any
    rangeTo: Any
    body: List[Any]

@dataclass
class programNode:
    statements: List[Any]
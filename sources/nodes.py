from dataclasses import dataclass
from typing import Any, List

@dataclass
class numberNode:
    value: float

@dataclass
class textNode:
    value: str

@dataclass
class booleanNode:
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
class terOtptNode:
    text: Any

@dataclass
class terInptNode:
    var: str

@dataclass
class loopWhileNode:
    condition: Any
    body: List[Any]

@dataclass
class loopForNode:
    var: forRangeVarNode
    rangeFrom: Any
    rangeTo: Any
    body: List[Any]

@dataclass
class forRangeVarNode:
    name: str
    value: Any
    newType: str

@dataclass
class loopNode:
    stop: bool
    skip: bool

@dataclass
class loopIfNode:
    condition: Any
    body: List[Any]
    elseBody: List[Any]

@dataclass
class programNode:
    statements: List[Any]

@dataclass
class tipNode:
    text: Any
class compile:
    def __init__(self):
        self.compileCodes = []
        self.typeFormat = {
            'number': 'int',
            'text': 'char*',
            'boolean': 'bool', 
            '': '', 
        }
        self.operatorFormat = {
            '+': '+',
            '-': '-',
            '*': '*',
            '`': '/',
            '%': '%',
            '=': '==',
            '/': '||',
            '&': '&&',
            '</=': '<=',
            '>/=': '>=', 
            '~': '!', 
            '>': '>', 
            '<': '<', 
        }

    def addCode(self, code):
        self.compileCodes.append(code)
    
    def visit(self, node):
        methodName = f'visit_{type(node).__name__}'
        if hasattr(self, methodName):
            return getattr(self, methodName)(node)
        raise ValueError(f"No visit method found for node type: {type(node).__name__}")
    
    def visit_programNode(self, node):
        self.addCode("#include <stdio.h>\n#include <string.h>\nint main() { ")
        for statement in node.statements:
            self.visit(statement)
        self.addCode("return 0; }")
        return "".join(self.compileCodes)
    
    def visit_numberNode(self, node):
        return str(node.value)
    
    def visit_textNode(self, node):
        return f'"{node.value}"'
    
    def visit_booleanNode(self, node):
        return "true" if node.value else "false"

    def visit_varsNewNode(self, node):
        cType = self.typeFormat.get(node.type, 'int')
        valueCode = self.visit(node.value)
        if cType == 'char*':
            self.addCode(f'{cType} {node.name}[] = {valueCode};')
        else:
            self.addCode(f"{cType} {node.name} = {valueCode};")
    
    def visit_varsModifyNode(self, node):
        valueCode = self.visit(node.value)
        self.addCode(f"{node.name} = {valueCode};")
    
    def visit_opNode(self, node):
        leftCode = self.visit(node.left)
        rightCode = self.visit(node.right)
        return f"({leftCode} {self.operatorFormat[node.operator]} {rightCode})"
    
    def visit_generalNode(self, node):
        return 
    
    def visit_loopWhileNode(self, node):
        condition = self.visit(node.condition)
        self.addCode(f"while({condition}) {{")
        for code in node.body:
            self.visit(code)
        self.addCode('}')
    
    def visit_loopForNode(self, node):
        type = self.typeFormat[node.var.newType]
        rangeVar = f"{type} {node.var.name} = {node.rangeFrom}"
        self.addCode(f"for ({rangeVar}; {node.var.name} <= {node.rangeTo}; {node.var.name}++){{")
        for code in node.body:
            self.visit(code)
        self.addCode('}')
    
    def visit_terOtptNode(self, node):
        text = self.visit(node.text)
        self.addCode(f"printf(\"%s\", {text})")

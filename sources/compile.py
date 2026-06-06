class compile:
    def __init__(self):
        self.compileCodes = []
        self.typeFormat = {
            'number': 'int',
            'text': 'char*',
            'boolean': 'bool', 
            'dotNum': 'double', 
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
        self.varsTypeMap = {}

    def addCode(self, code):
        self.compileCodes.append(code)
    
    def visit(self, node):
        methodName = f'visit_{type(node).__name__}'
        if hasattr(self, methodName):
            return getattr(self, methodName)(node)
        raise ValueError(f"No visit method found for node type: {type(node).__name__}")
    
    def visit_programNode(self, node):
        self.addCode("#ifdef _WIN32\n#include <windows.h>\n#endif\n#include <stdio.h>\n#include <string.h>\nint main() { \n #ifdef _WIN32\nSetConsoleOutputCP(CP_UTF8);\n#endif\n")
        for statement in node.statements:
            self.visit(statement)
        self.addCode("return 0; }")
        return "".join(self.compileCodes)
    
    def visit_numberNode(self, node):
        if node.value.is_integer():
            return str(int(node.value))
        return str(node.value)
    
    def visit_textNode(self, node):
        return f'"{node.value}"'
    
    def visit_booleanNode(self, node):
        return "true" if node.value else "false"

    def visit_varsNewNode(self, node):
        cType = self.typeFormat.get(node.type, 'int')
        valueCode = self.visit(node.value)
        self.varsTypeMap[node.name] = node.type
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
        fromNum = self.visit(node.rangeFrom)
        toNum = self.visit(node.rangeTo)
        rangeVar = f"{type} {node.var.name} = {fromNum}"
        self.addCode(f"for ({rangeVar}; {node.var.name} <= {toNum}; {node.var.name}++){{")
        if node.var.newType != '':
            self.varsTypeMap[node.var.name] = node.var.newType
        for code in node.body:
            self.visit(code)
        self.addCode('}')
        del self.varsTypeMap[node.var.name]
    
    def visit_terOtptNode(self, node):
        text = self.visit(node.text)
        if text.startswith('"'):
            self.addCode(f'printf({text});')
        elif text in ['true', 'false']:
            self.addCode(f"printf(\"%d\", {text});")
        elif text.replace('.', '').isdigit() or (text.startswith('-') and text[1:].replace('.', '').isdigit()):
            if '.' in text:
                self.addCode(f'printf(\"%.16g\", {text});')
            else:
                self.addCode(f'printf(\"%d\", {text});')
        else:
            printfCode = None
            if self.varsTypeMap[text] == 'number' or self.varsTypeMap[text] == 'boolean':
                printfCode = '%d'
            elif self.varsTypeMap[text] == 'text':
                printfCode = '%s'
            elif self.varsTypeMap[text] == 'dotNum':
                printfCode = '%.16g'
            self.addCode(f'printf(\"{printfCode}\", {text});')
    
    def visit_varsNode(self, node):
        return node.name

    def visit_tipNode(self, node):
        return 
    
    def visit_loopNode(self, node):
        if node.stop:
            self.addCode('break;')
        elif node.skip:
            self.addCode('continue;')
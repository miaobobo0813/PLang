from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List

# 1. Token 类型枚举（标识符正式升级为修饰符！）
class TokenType(Enum):
    KEYWORD = auto()      # 核心关键字 (vars, loop, ter, number, yes, no...)
    MODIFIER = auto()     # 修饰符 (跟在点号后面的名字，如 vars.xxx 中的 xxx)
    SYMBOL = auto()       # 符号 (.,;(){}[]`+-*/%&~<>=!)
    NUMBER = auto()       # 数字字面量 (整数和小数)
    TEXT = auto()         # 字符串字面量
    EOF = auto()          # 文件结束标志

@dataclass
class Token:
    type: TokenType
    value: str
    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}')"

# 2. PLang 核心关键字全家桶
KEYWORDS = {
    "using", "vars", "loop", "ter", "operators", 
    "document", "tips", "use", "sub",
    "new", "modify", "type", "func", "return", "args", "var", "modify", 
    "while", "for", "range", "from", "to", "when", "codes", "stop", "skip",
    "otpt", "inpt", "if", "in",
    "number", "dotNum", "text", "boolean",
    "yes", "no"
}

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.pos = 0
    
    def get_next_token(self) -> Token:
        # 跳过空格和换行
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            self.pos += 1
        
        if self.pos >= len(self.source):
            return Token(TokenType.EOF, "")
        
        char = self.source[self.pos]
        
        # 识别符号
        if char in ".,;(){}[]+*`%/&~<>-=":
            self.pos += 1
            return Token(TokenType.SYMBOL, char)
        
        # 识别字符串
        if char == '"':
            start = self.pos
            self.pos += 1
            while self.pos < len(self.source) and self.source[self.pos] != '"':
                self.pos += 1
            self.pos += 1
            return Token(TokenType.TEXT, self.source[start:self.pos])
        
        # 识别关键字 或 修饰符 (MODIFIER)
        if char.isalpha() or char == '_':
            start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self.pos += 1
            word = self.source[start:self.pos]
            
            # 核心判断逻辑：是核心关键字，还是修饰符？
            if word in KEYWORDS:
                return Token(TokenType.KEYWORD, word)
            else:
                return Token(TokenType.MODIFIER, word)
        
        # 识别数字 (支持 dotNum)
        if char.isdigit() or (char == '.' and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit()):
            start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
                self.pos += 1
            return Token(TokenType.NUMBER, self.source[start:self.pos])
        
        raise SyntaxError(f"Unknown character: '{char}'")

    def scan_all(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

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
    vType: str
    value: Any

@dataclass
class varModifyNode:
    name: str
    newValue: Any

@dataclass
class opNode:
    op: str
    left: Any
    right: Any

@dataclass
class callNode:
    keyword: str
    modifier: str
    args: List[Any]

@dataclass
class loopNode:
    condition: Any
    body: List[Any]

@dataclass
class programNode:
    statements: List[Any]

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.currentModifyTarget = None
    
    def currentToken(self):
        return self.tokens[self.pos]
    
    def eat(self, tokenType):
        if self.currentToken().type == tokenType:
            self.pos += 1
        else:
            raise SyntaxError(f"Syntax error: need a {tokenType} but found a {self.currentToken().type}")
    
    def parseProgram(self):
        statements = []
        while self.currentToken().type != TokenType.EOF:
            statements.append(self.parseStatement())
        return programNode(statements)
    
    def parseStatement(self):
        token = self.currentToken()
        
        if token.type == TokenType.KEYWORD and token.value == 'vars':
            return self.parseVarsStatement() # 解析 vars 相关的语句
        elif token.type == TokenType.KEYWORD and token.value == 'loop':
            return self.parseLoopStatement() # 解析 loop 相关的语句
        elif token.type == TokenType.KEYWORD and token.value == 'ter':
            return self.parseTerStatement()  # 解析 ter 相关的语句
        elif token.type == TokenType.KEYWORD and token.value == 'using':
            return self.parseUsingStatement()  # 解析 using 相关的语句
        elif token.type == TokenType.KEYWORD and token.value == 'operators':
            return self.parseOperatorsStatement()  # 解析 operators 相关的语句
        else:
            raise SyntaxError(f"Unknown keyword: {token.value}")
    
    def parseVarsStatement(self):
        self.eat(TokenType.KEYWORD) # 吃掉 'vars'
        self.eat(TokenType.SYMBOL)  # 吃掉 '.'
        
        methodToken = self.currentToken().value
        
        if methodToken == 'new':
            self.eat(TokenType.KEYWORD) # 吃掉方法名 ('new')
            self.eat(TokenType.SYMBOL)  # 吃掉 '('
            # 解析 vars.new(i, number, 0)
            name = self.currentToken().value # 获取变量名
            self.eat(TokenType.MODIFIER)
            self.eat(TokenType.SYMBOL)        # 吃掉 ','
            
            varType = self.currentToken().value # 获取类型
            self.eat(TokenType.KEYWORD)
            self.eat(TokenType.SYMBOL)        # 吃掉 ','
            
            value = self.parseExpression()   # 递归解析初始值表达式
            self.eat(TokenType.SYMBOL)        # 吃掉 ')'
            self.eat(TokenType.SYMBOL)        # 吃掉 ';'
            
            return varsNewNode(name, varType, value)
        else:
            self.eat(TokenType.MODIFIER) # 吃掉变量名
            # 走到这里说明是 vars.xxx 开头的语句（比如 vars.xxx.modify(...)）
            self.eat(TokenType.SYMBOL)  # 在这里吃掉 '.'

            name = self.currentToken().value # 获取修饰符(.modify)
            self.eat(TokenType.KEYWORD)
            self.eat(TokenType.SYMBOL)  # 吃掉 '('

            if name == "modify":
                # 💡 核心操作：临时记录当前正在被修改的变量名！
                self.currentModifyTarget = methodToken  # methodToken 就是 vars.xxx 中的 xxx 
                
                value = self.parseExpression() # 递归解析括号里的表达式
                
                self.eat(TokenType.SYMBOL)  # 吃掉 ')'
                self.eat(TokenType.SYMBOL)  # 吃掉 ';'
                
                # 别忘了把临时记录清空
                self.currentModifyTarget = None 
                
                return varModifyNode(methodToken, value)
            else:
                raise SyntaxError(f"Unknown modifier: {name}")
    
    # 补全 ter 语句解析 (例如: ter.otpt("xxx"); )
    def parseTerStatement(self):
        self.eat(TokenType.KEYWORD) # 吃掉 'ter'
        self.eat(TokenType.SYMBOL)  # 吃掉 '.'
        
        method = self.currentToken().value
        self.eat(TokenType.KEYWORD) # 吃掉方法名 (如 'otpt')
        
        self.eat(TokenType.SYMBOL)  # 吃掉 '('
        args = []
        # 如果括号里不是直接闭合，就解析参数
        if self.currentToken().type != TokenType.SYMBOL or self.currentToken().value != ')':
            args.append(self.parseExpression())
            
        self.eat(TokenType.SYMBOL)  # 吃掉 ')'
        self.eat(TokenType.SYMBOL)  # 吃掉 ';'
        
        return callNode(keyword='ter', modifier=method, args=args)

    # 补全 loop 语句解析 (例如: loop.while.when(...).codes({...}); )
    def parseLoopStatement(self):
        self.eat(TokenType.KEYWORD) # 吃掉 'loop'
        self.eat(TokenType.SYMBOL)  # 吃掉 '.'
        
        loopType = self.currentToken().value # 获取 'while' 或 'for'
        self.eat(TokenType.KEYWORD)
        
        if loopType == 'stop':
            self.eat(TokenType.SYMBOL)  # 吃掉 '('
            self.eat(TokenType.SYMBOL)  # 吃掉 ')'
            self.eat(TokenType.SYMBOL)  # 吃掉 ';'
            return callNode(keyword='loop', modifier='stop', args=[])
        elif loopType == 'skip':
            self.eat(TokenType.SYMBOL)  # 吃掉 '('
            self.eat(TokenType.SYMBOL)  # 吃掉 ')'
            self.eat(TokenType.SYMBOL)  # 吃掉 ';'
            return callNode(keyword='loop', modifier='skip', args=[])
        # 目前先实现 while 的逻辑
        elif loopType == 'while':
            self.eat(TokenType.SYMBOL)  # 吃掉 '.'
            self.eat(TokenType.KEYWORD) # 吃掉 'when'
            self.eat(TokenType.SYMBOL)  # 吃掉 '('
            condition = self.parseExpression() # 解析循环条件
            self.eat(TokenType.SYMBOL)  # 吃掉 ')'
            
            self.eat(TokenType.SYMBOL)  # 吃掉 '.'
            self.eat(TokenType.KEYWORD) # 吃掉 'codes'
            self.eat(TokenType.SYMBOL)  # 吃掉 '('
            self.eat(TokenType.SYMBOL)  # 吃掉 '{'
            
            body = []
            # 循环解析大括号里的语句，直到遇到右大括号
            while self.currentToken().value != '}':
                body.append(self.parseStatement())
                
            self.eat(TokenType.SYMBOL)  # 吃掉 '}'
            self.eat(TokenType.SYMBOL)  # 吃掉 ')'
            self.eat(TokenType.SYMBOL)  # 吃掉 ';'
            
            return loopNode(condition=condition, body=body)
        
        # for 循环的逻辑可以后续在这里用 elif 继续扩展
        else:
            raise SyntaxError(f"Unknown loop: {loopType}")

    # 补全 using 语句解析 (例如: using.tips("xxx"); )
    def parseUsingStatement(self):
        self.eat(TokenType.KEYWORD) # 吃掉 'using'
        self.eat(TokenType.SYMBOL)  # 吃掉 '.'
        
        method = self.currentToken().value
        self.eat(TokenType.KEYWORD)
        
        self.eat(TokenType.SYMBOL)  # 吃掉 '('
        arg = self.parseExpression()
        self.eat(TokenType.SYMBOL)  # 吃掉 ')'
        self.eat(TokenType.SYMBOL)  # 吃掉 ';'
        
        return callNode(keyword='using', modifier=method, args=[arg])

    # 补全最基础的元素解析（数字、字符串、vars.xxx 变量获取）
    def parsePrimary(self):
        token = self.currentToken()
        
        # 解析数字
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return numberNode(value=float(token.value))
        
        # 解析字符串
        if token.type == TokenType.TEXT:
            self.eat(TokenType.TEXT)
            return textNode(value=token.value)
        
        if token.type == TokenType.KEYWORD and token.value in {"yes", "no"}:    
            self.eat(TokenType.KEYWORD)
            return boolNode(value=token.value == "yes")

        if token.type == TokenType.KEYWORD and token.value == 'operators':
            return self.parseOperatorsStatement()  # 直接调用 operators 语句解析函数
        
        # 解析 var 变量
        if token.type == TokenType.KEYWORD and token.value == 'var':
            self.eat(TokenType.KEYWORD) # 吃掉 'var'
            if self.currentModifyTarget:
                return varsNode(name=self.currentModifyTarget)
            else:
                raise SyntaxError("Syntax error: 'var' used outside of a modify context.")

        # 解析 vars.xxx 这种变量获取
        if token.type == TokenType.KEYWORD and token.value == 'vars':
            self.eat(TokenType.KEYWORD)
            self.eat(TokenType.SYMBOL) # 吃掉 '.'
            var_name = self.currentToken().value
            self.eat(TokenType.MODIFIER)
            return varsNode(name=var_name)
            
        raise SyntaxError(f"Unknown value: {token.value}")

    def parseExpression(self):
        if self.currentToken().type == TokenType.SYMBOL:
            return self.parseOperatorsStatement()  # 如果是符号，说明可能是运算表达式，直接调用 operators 语句解析函数
        elif self.currentToken().type == TokenType.KEYWORD:
            token_val = self.currentToken().value
            if token_val == 'var' and self.currentModifyTarget:
                self.eat(TokenType.KEYWORD)
                return varsNode(name=self.currentModifyTarget)
            return self.parsePrimary() 
        else:
            return self.parsePrimary()
    
    # 补全 operators 语句解析 (例如: operators.<(vars.a, vars.b); )
    def parseOperatorsStatement(self):
        token = self.currentToken()
        if token.type == TokenType.KEYWORD and token.value == 'operators':
            self.eat(TokenType.KEYWORD) # 吃掉 'operators'
            self.eat(TokenType.SYMBOL)  # 吃掉 '.'
        
        # 获取真实的运算符符号 (比如 <, +, = 等)
        op_token = self.currentToken()
        self.eat(TokenType.SYMBOL) 

        if self.currentToken().type == TokenType.SYMBOL and self.currentToken().value in {'/'}:
            # 处理</=, >/=
            op_token.value += self.currentToken().value
            self.eat(TokenType.SYMBOL) # 吃掉 '/'
            op_token.value += self.currentToken().value
            self.eat(TokenType.SYMBOL) # 吃掉 '='

        self.eat(TokenType.SYMBOL)  # 吃掉 '('
        
        # 递归解析运算符左边的参数
        left = self.parseExpression()
        self.eat(TokenType.SYMBOL)  # 吃掉 ','
        # 递归解析运算符右边的参数
        right = self.parseExpression()
        
        self.eat(TokenType.SYMBOL)  # 吃掉 ')'
        
        # 直接返回一个标准的二元运算节点！
        # 这样 operators.<(a, b) 就和 <(a, b) 完全等价了
        return opNode(op=op_token.value, left=left, right=right)

class Interpreter:
    def __init__(self):
        # 用来存放 PLang 里的变量，比如 {"i": 0, "pi": 3.14}
        self.variables = {}
        self.isStop = False  # 用来控制 loop.stop() 的执行
        self.isSkip = False  # 用来控制 loop.skip() 的执行

    # 核心分发器：根据节点类型，自动调用对应的 visit_xxx 方法
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"Syntax Error: Unknown statement {type(node).__name__}")

    # 1. 处理整个程序入口
    def visit_programNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    # 2. 处理变量声明 (vars.new)
    def visit_varsNewNode(self, node):
        value = self.visit(node.value)  # 算出初始值
        self.variables[node.name] = value
        # print(f"Define variable: {node.name} -> {value}")

    # 3. 处理基础字面量 (数字、字符串)
    def visit_numberNode(self, node):
        return node.value
    
    def visit_textNode(self, node):
        return node.value.strip('"')  # 去掉两边的引号

    # 4. 处理获取变量 (比如 vars.i 里的 i)
    def visit_varsNode(self, node):
        if node.name not in self.variables:
            raise Exception(f"Runtime error: '{node.name}' has not defined.")
        return self.variables[node.name]

    # 5. 处理输出 (ter.otpt)
    def visit_callNode(self, node):
        if node.keyword == 'ter' and node.modifier == 'otpt':
            for arg in node.args:
                print(self.visit(arg), end="") 
        elif node.keyword == 'using' and node.modifier == 'tips':
            # 处理 using.tips
            # print(f"Comments: {self.visit(node.args[0])}")
            return
        elif node.keyword == 'loop' and node.modifier == 'stop':
            self.isStop = True  # 设置停止标志，在 loopNode 里检查这个标志来决定是否跳出循环
        elif node.keyword == 'loop' and node.modifier == 'skip':
            self.isSkip = True  # 设置跳过标志，在 loopNode 里检查这个标志来决定是否跳过当前迭代
        else:
            raise Exception(f"Syntax Error: Unknown call: {node.keyword}.{node.modifier}")

    # 6. 处理数学和逻辑运算 (+, < 等)
    def visit_opNode(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        
        if node.op == '+':
            return left_val + right_val
        elif node.op == '<':
            return left_val < right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '`':
            return left_val / right_val
        elif node.op == '%':
            return left_val % right_val
        elif node.op == '&':    
            return left_val and right_val
        elif node.op == '/':
            return left_val or right_val
        elif node.op == '>':
            return left_val > right_val
        elif node.op == '=':
            return left_val == right_val
        elif node.op == '</=':
            return left_val <= right_val
        elif node.op == '>/=':
            return left_val >= right_val
        else:
            raise Exception(f"Syntax Error: Unknown operator: {node.op}")

    # 7. 处理变量修改 (vars.i.modify(...))
    def visit_varModifyNode(self, node):
        new_value = self.visit(node.newValue)  # 算出新的值
        self.variables[node.name] = new_value  # 更新字典里的变量
        # print(f"Modify: {node.name} -> {new_value}")

    # 8. 处理循环 (loop.while.when(...).codes({...}))
    def visit_loopNode(self, node):
        # 只要条件为 True，就反复执行 body 里的语句
        while self.visit(node.condition):
            for statement in node.body:
                self.visit(statement)
                if self.isStop:  # 如果 loop.stop() 被调用了，就跳出循环
                    self.isStop = False  # 重置停止标志，以便下次循环使用
                    return
                if self.isSkip:  # 如果 loop.skip() 被调用了，就跳过当前迭代
                    self.isSkip = False  # 重置跳过标志，以便下次循环使用
                    break  # 跳出当前迭代，继续下一轮循环
    
# ================= 最终测试运行 =================
if __name__ == '__main__':
    test_plang_code = """
    using.tips("PLang 编译器终极测试");
    vars.new(i, number, 1);
    vars.new(pi, dotNum, 3.14);
    loop.while.when(>/=(vars.i, 8)).codes({
        ter.otpt("当前 i 的值是：");
        vars.i.modify(*(var, 2));
        ter.otpt(vars.i);
        ter.otpt("\n");
    });
    ter.otpt("测试结束！");
    """
    lexer = Lexer(test_plang_code)
    tokens = lexer.scan_all()
    
    parser = Parser(tokens)
    ast = parser.parseProgram()
    
    # print("AST Tree: ")
    # print(ast)

    interpreter = Interpreter()
    interpreter.visit(ast)

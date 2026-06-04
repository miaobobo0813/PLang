from tokens import *
from nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.currentModifyTarget = None
    
    def nowToken(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, "")
    
    def nextToken(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return Token(TokenType.EOF, "")
    
    def parseProgram(self):
        statement = []
        while self.nowToken().type != TokenType.EOF:
            statement.append(self.parseStatement())
        return programNode(statements=statement)
    
    def parseStatement(self):
        token = self.nowToken()
        if token.type == TokenType.KEYWORD:
            if token.value == 'vars':
                return self.parseVars()
            elif token.value == 'loop':
                return self.parseLoop()
            elif token.value == 'ter':
                return self.parseTerminal()
            elif token.value == 'using':
                return self.parseUsing()
            else:
                raise ValueError(f"Unexpected keyword: {token.value}")
        elif token.type == TokenType.SYMBOL:
            raise ValueError(f"Unexpected symbol: {token.value}")
        else:
            raise ValueError(f"Unexpected keyword: {token.value}")
    
    def parseVars(self):
        self.nextToken()  # Skip 'vars'
        self.nextToken()  # Skip '.'
        modifier = self.nextToken()
        if modifier.type != TokenType.MODIFIER:
            raise ValueError(f"Expected modifier \"{modifier.value}\"")
        if modifier.value == 'new':
            self.nextToken()  # Skip '('
            name = self.nextToken()
            self.nextToken()  # Skip ','
            typeToken = self.nextToken()
            self.nextToken()  # Skip ','
            value = self.parseExpression()
            self.nextToken()  # Skip ')'
            self.nextToken()  # Skip ';'
            return varsNewNode(name=name.value, value=value, type=typeToken.value)
        else:
            self.nextToken()  # Skip '.'
            check = self.nextToken()
            if check.value == 'modify':
                self.currentModifyTarget = modifier.value
                self.nextToken()  # Skip '('
                value = self.parseExpression()
                self.nextToken()  # Skip ')'
                self.nextToken()  # Skip ';'
                self.currentModifyTarget = None
                return varsModifyNode(name=modifier.value, value=value)
            else:
                raise SyntaxError("Need modify.")
    
    def parseExpression(self):
        token = self.nowToken()
        if token.type == TokenType.NUMBER:
            return numberNode(value=float(token.value))
        elif token.type == TokenType.TEXT:
            return textNode(value=token.value)
        elif token.type == TokenType.MODIFIER:
            return varsNode(name=token.value)
        elif token.type == TokenType.OPERATOR:
            return self.parseOperator()
        elif token.type == TokenType.KEYWORD and token.value == 'operators':
            self.nextToken()  # Skip 'operators'
            self.nextToken()  # Skip '.'
            return self.parseOperator()
        elif token.type == TokenType.KEYWORD and token.value == 'vars':
            self.nextToken()  # Skip 'vars'
            self.nextToken()  # Skip '.'
            return varsNode(name=self.nowToken().value)
        elif token.value == 'var':
            if self.currentModifyTarget is None:
                raise ValueError("Unexpected 'var' without modifying a variable.")
            return varsNode(name=self.currentModifyTarget)
        else:
            raise ValueError(f"Unexpected token in expression: {token.value}")
    
    def parseOperator(self):
        operator = self.nowToken()
        if operator.type != TokenType.OPERATOR:
            raise ValueError(f"Expected operator, got: {operator.value}")
        self.nextToken()  # Skip operator
        self.nextToken()  # Skip '('
        left = self.parseExpression()
        self.nextToken()  # Skip ','
        right = self.parseExpression()
        self.nextToken()  # Skip ')'
        return opNode(operator=operator.value, left=left, right=right)

    def parseLoop(self):
        self.nextToken()  # Skip 'loop'
        self.nextToken()  # Skip '.'
        modifier = self.nextToken()
        if modifier.value == 'while':
            condition = None
            statements = []
            self.nextToken()  # Skip '.'
            modifier1 = self.nextToken()
            if modifier1.value == 'when':
                self.nextToken()  # Skip '('
                condition = self.parseExpression()
                self.nextToken()  # Skip ')'
            elif modifier1.value == 'codes':
                self.nextToken()  # Skip '('
                self.nextToken()  # Skip '{'
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.nextToken()  # Skip '}'
                self.nextToken()  # Skip ')'
            else:
                raise ValueError(f"Expected loop modifier: {self.nowToken().value}.")
            
            self.nextToken()  # Skip '.'
            modifier2 = self.nextToken()
            if modifier2.value == 'when':
                self.nextToken()  # Skip '('
                condition = self.parseExpression()
                self.nextToken()  # Skip ')'
            elif modifier2.value == 'codes':
                self.nextToken()  # Skip '('
                self.nextToken()  # Skip '{'
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.nextToken()  # Skip '}'
                self.nextToken()  # Skip ')'
            else:
                raise ValueError(f"Expected loop modifier: {self.nowToken().value}.")
            
            if condition is None:
                raise ValueError("Missing condition for while loop")
            if not statements:
                raise ValueError("Missing body for while loop")

            self.nextToken() # Skip ';'

            return loopWhileNode(condition=condition, body=statements)
        elif modifier.value == 'for':
            var = None
            statements = []
            rangeFrom = None
            rangeTo = None
            self.nextToken() # Skip '.'
            modifier1 = self.nextToken()
            if modifier1.value == 'range':
                self.nextToken() # Skip '('
                rangeFrom = self.parseExpression()
                self.nextToken() # Skip ','
                rangeTo = self.parseExpression()
                self.nextToken() # Skip ','
                if self.nowToken().value != 'vars':
                    raise ValueError(f"Expected variable for for loop: {self.nowToken().value}")
                self.nextToken() # Skip 'vars'
                self.nextToken() # Skip '.'
                type = self.nowToken()
                if type.value == 'new':
                    self.nextToken() # Skip 'new'
                    self.nextToken() # Skip '('
                    varName = self.nowToken()
                    self.nextToken() # Skip variable name
                    varType = self.nextToken()
                    self.nextToken() # Skip ','
                    value = self.parseExpression()
                    self.nextToken() # Skip ')'
                    var = forRangeVarNode(name=varName.value, value=value, newType=varType.value)
                else:
                    varName = self.nowToken()
                    var = forRangeVarNode(name=varName.value, value=None, newType='')
                self.nextToken() # Skip ')'
            elif modifier1.value == 'codes':
                self.nextToken() # Skip '('
                self.nextToken() # Skip '{'
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.nextToken() # Skip '}'
                self.nextToken() # Skip ')'
            else:
                raise ValueError(f"Expected loop modifier: {self.nowToken().value}.")
            
            self.nextToken() # Skip '.'
            modifier1 = self.nextToken()
            if modifier1.value == 'range':
                self.nextToken() # Skip '('
                rangeFrom = self.parseExpression()
                self.nextToken() # Skip ','
                rangeTo = self.parseExpression()
                self.nextToken() # Skip ','
                if self.nowToken().value != 'vars':
                    raise ValueError(f"Expected variable for for loop: {self.nowToken().value}")
                self.nextToken() # Skip 'vars'
                self.nextToken() # Skip '.'
                type = self.nowToken()
                if type.value == 'new':
                    self.nextToken() # Skip 'new'
                    self.nextToken() # Skip '('
                    varName = self.nowToken()
                    self.nextToken() # Skip variable name
                    varType = self.nextToken()
                    self.nextToken() # Skip ','
                    value = self.parseExpression()
                    self.nextToken() # Skip ')'
                    var = forRangeVarNode(name=varName.value, value=value, newType=varType.value)
                else:
                    varName = self.nowToken()
                    var = forRangeVarNode(name=varName.value, value=None, newType='')
                self.nextToken() # Skip ')'
            elif modifier1.value == 'codes':
                self.nextToken() # Skip '('
                self.nextToken() # Skip '{'
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.nextToken() # Skip '}'
                self.nextToken() # Skip ')'
            else:
                raise ValueError(f"Expected loop modifier: {self.nowToken().value}.")

            if var is None:
                raise ValueError("Missing variable for for loop")
            if rangeFrom is None:
                raise ValueError("Missing start value for for loop")
            if rangeTo is None:
                raise ValueError("Missing end value for for loop")
            if statements == []:
                raise ValueError("Missing body for for loop")

            self.nextToken() # Skip ';'

            return loopForNode(var=var, rangeFrom=rangeFrom, rangeTo=rangeTo, body=statements)
        elif modifier.value == 'stop':
            self.nextToken() # Skip '('
            self.nextToken() # Skip ')'
            self.nextToken() # Skip ';'
            return loopNode(stop=True, skip=False)
        elif modifier.value == 'skip':
            self.nextToken() # Skip '('
            self.nextToken() # Skip ')'
            self.nextToken() # Skip ';'
            return loopNode(stop=False, skip=True)
        else:
            raise ValueError(f"Expected loop modifier: {self.nowToken().value}. ('if' is developing...)")
    
    def parseTerminal(self):
        self.nextToken()  # Skip 'ter'
        self.nextToken()  # Skip '.'
        modifier = self.nextToken()
        if modifier.value == 'otpt':
            self.nextToken()  # Skip '('
            value = self.parseExpression()
            self.nextToken()  # Skip ')'
            self.nextToken()  # Skip ';'
            return terOtptNode(text=value)
        else:
            raise ValueError(f"Expected terminal modifier: {self.nowToken().value}. (inpt is in development...)")
    
    def parseUsing(self):
        self.nextToken()  # Skip 'using'
        self.nextToken()  # Skip '.'
        modifier = self.nextToken()
        if modifier.value == 'tips':
            self.nextToken()  # Skip '('
            self.parseExpression()
            self.nextToken()  # Skip ')'
            self.nextToken()  # Skip ';'
            return None
        else:
            raise ValueError(f"Expected using modifier: {self.nowToken().value}. (use is in development...)")

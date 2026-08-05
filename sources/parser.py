from tokens import *
from nodes import *
from typing import Optional

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.currentModifyTarget = None
        self.errors = []
        self.notSupportVarName = ['int', 'char', 'bool', 'struct', 'double', 'long', 'float']
        self.notSupportVarNameIncludes = {"(", ')', '[', ']', '{', '}', ';', ',', '.'}.union(OPERATORS, SPECIAL_OPERATORS)
        self.definedVarName = []
        self.definedVarTypes = {}
    
    def nowToken(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        token = self.tokens[len(self.tokens)-1]
        return Token(TokenType.EOF, "", fromPos=token.fromPos, toPos=token.toPos)
    
    def nextToken(self, needs: Optional[str] = None, message: Optional[str] = None):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if needs != None:
                if token.value != needs:
                    errorToken = self.tokens[self.pos-1]
                    if message != None:
                        self.errors.append(f"Line: {errorToken.fromPos[0]}~{errorToken.toPos[0]}, Column: {errorToken.fromPos[1]}~{errorToken.toPos[1]}: {message}")
                    else:
                        self.errors.append(f"Line: {errorToken.fromPos[0]}~{errorToken.toPos[0]}, Column: {errorToken.fromPos[1]}~{errorToken.toPos[1]}: Missing {needs}")
                    return token
            self.pos += 1
            return token
        token = self.tokens[len(self.tokens)-1]
        return Token(TokenType.EOF, "", fromPos=token.fromPos, toPos=token.toPos)
    
    def _getExpressionType(self, node):
        if isinstance(node, numberNode):
            return 'number'
        if isinstance(node, dotNumNode):
            return 'dotNum'
        if isinstance(node, textNode):
            return 'text'
        if isinstance(node, booleanNode):
            return 'boolean'
        if isinstance(node, varsNode):
            return self.definedVarTypes.get(node.name)
        if isinstance(node, opNode):
            leftType = self._getExpressionType(node.left)
            rightType = self._getExpressionType(node.right)
            if leftType in {'number', 'dotNum'} and rightType in {'number', 'dotNum'}:
                return 'dotNum' if 'dotNum' in {leftType, rightType} else 'number'
            if leftType == rightType:
                return leftType
        return None

    def _isCompatibleType(self, targetType, valueType):
        if targetType is None or valueType is None:
            return False
        if targetType == valueType:
            return True
        if targetType in {'number', 'dotNum'} and valueType in {'number', 'dotNum'}:
            return True
        return False

    def _isComparable(self, leftType, rightType):
        if leftType is None or rightType is None:
            return False
        if leftType == rightType and (not leftType in {'text', 'boolean'}) and (not rightType in {'text', 'boolean'}):
            return True
        if leftType in {'number', 'dotNum'} and rightType in {'number', 'dotNum'}:
            return True
        return False
    
    def _isComputable(self, leftType, rightType):
        if leftType is None or rightType is None:
            return False
        if leftType == rightType and leftType != 'text' and rightType != 'text':
            return True
        if leftType in {'number', 'dotNum'} and rightType in {'number', 'dotNum'}:
            return True
        return False
    
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
                self.errors.append(f"Line: {token.fromPos[0]}~{token.toPos[0]}, Column: {token.fromPos[1]}~{token.toPos[1]}: Unknown keyword: {token.value}")
        elif token.type == TokenType.SYMBOL:
            self.nextToken()
            self.errors.append(f"Line: {token.fromPos[0]}~{token.toPos[0]}, Column: {token.fromPos[1]}~{token.toPos[1]}: Unexpected symbol: {token.value} (No extra ; allow)")
            return tipNode(text=token.value)
        else:
            self.nextToken()
            self.errors.append(f"Line: {token.fromPos[0]}~{token.toPos[0]}, Column: {token.fromPos[1]}~{token.toPos[1]}: Unknown keyword: {token.value}")
            return tipNode(text=token.value)
    
    def parseVars(self):
        self.nextToken('vars', "Missing 'vars' keyword")
        self.nextToken('.', "Missing '.' between keyword and modifier")
        modifier = self.nextToken()
        if modifier.type != TokenType.MODIFIER:
            self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Unknown modifier '{modifier.value}'")
        if modifier.value == 'new':
            self.nextToken('(', "Missing '(' after modifier")
            name = self.nextToken()
            self.nextToken(',', "Missing ',' between args")
            typeToken = self.nextToken()
            self.nextToken(',', "Missing ',' between args")
            value = self.parseExpression()
            self.nextToken(')', "Missing ')' after args")
            self.nextToken(';', "Missing ';' after vars statement")
            if name.value in self.notSupportVarName or any(keyword in name.value for keyword in self.notSupportVarNameIncludes):
                self.errors.append(f"Line: {name.fromPos[0]}~{name.toPos[0]}, Column: {name.fromPos[1]}~{name.toPos[1]}: Variable name '{name.value}' contains invalid character(s)")
            if name.value in self.definedVarName:
                self.errors.append(f"Line: {name.fromPos[0]}~{name.toPos[0]}, Column: {name.fromPos[1]}~{name.toPos[1]}: Variable name '{name.value}' has been defined")
            else:
                self.definedVarName.append(name.value)
                self.definedVarTypes[name.value] = typeToken.value
            return varsNewNode(name=name.value, value=value, type=typeToken.value)
        else:
            if not modifier.value in self.definedVarName:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Variable '{modifier.value}' hasn't been defined")
            self.nextToken('.', "Missing '.' between modifiers")
            check = self.nextToken()
            if check.value == 'modify':
                self.currentModifyTarget = modifier.value
                self.nextToken('(', "Missing '(' after modifier")
                value = self.parseExpression()
                self.nextToken(')', "Missing ')' after args")
                self.nextToken(';', "Missing ';' after vars statement")
                self.currentModifyTarget = None
                declaredType = self.definedVarTypes.get(modifier.value)
                expressionType = self._getExpressionType(value)
                if declaredType is not None and expressionType is not None and not self._isCompatibleType(declaredType, expressionType):
                    self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Variable '{modifier.value}' cannot be modified with a value of type '{expressionType}'")
                return varsModifyNode(name=modifier.value, value=value)
            else:
                self.errors.append(f"Line: {check.fromPos[0]}~{check.toPos[0]}, Column: {check.fromPos[1]}~{check.toPos[1]}: Unknown modifier: {check.value}")
    
    def parseExpression(self):
        token = self.nowToken()
        if token.type == TokenType.NUMBER:
            self.nextToken()
            return numberNode(value=token.value)
        elif token.type == TokenType.DOTNUM:
            self.nextToken()
            return dotNumNode(value=token.value)
        elif token.type == TokenType.TEXT:
            self.nextToken()
            return textNode(value=token.value)
        elif token.type == TokenType.BOOLEAN:
            self.nextToken()
            return booleanNode(value=token.value=='yes')
        elif token.type == TokenType.OPERATOR:
            return self.parseOperator()
        elif token.type == TokenType.KEYWORD and token.value == 'operators':
            self.nextToken()
            self.nextToken('.', "Missing '.' between keyword and modifier")
            return self.parseOperator()
        elif token.type == TokenType.KEYWORD and token.value == 'vars':
            self.nextToken()
            self.nextToken('.', "Missing '.' between keyword and modifier")
            name = self.nextToken()
            if not name.value in self.definedVarName:
                self.errors.append(f"Line: {name.fromPos[0]}~{name.toPos[0]}, Column: {name.fromPos[1]}~{name.toPos[1]}: Variable '{name.value}' hasn't been defined.")
            return varsNode(name=name.value)
        elif token.value == 'var':
            self.nextToken()
            if self.currentModifyTarget is None:
                self.errors.append(f"Line: {token.fromPos[0]}~{token.toPos[0]}, Column: {token.fromPos[1]}~{token.toPos[1]}: Unexpected 'var' without modifying a variable")
                return numberNode(value='0')
            return varsNode(name=self.currentModifyTarget)
        else:
            self.nextToken()
            self.errors.append(f"Line: {token.fromPos[0]}~{token.toPos[0]}, Column: {token.fromPos[1]}~{token.toPos[1]}: Unknown expression: {token.value}")
    
    def parseOperator(self):
        operator = self.nextToken()
        if operator.type != TokenType.OPERATOR:
            self.errors.append(f"Line: {operator.fromPos[0]}~{operator.toPos[0]}, Column: {operator.fromPos[1]}~{operator.toPos[1]}: Unknown operator: {operator.value}")
        self.nextToken('(', "Missing '(' after operator")
        left = self.parseExpression()
        leftType = self._getExpressionType(left)
        if operator.value != '~':
            self.nextToken(',', "Missing ',' between operator args")
            right = self.parseExpression()
            self.nextToken(')', "Missing ')' after operator args")
            rightType = self._getExpressionType(right)
            if operator.value in {'+', '-', '*', '`'}:
                if not self._isComputable(leftType, rightType):
                    self.errors.append(f"Line: {operator.fromPos[0]}~{operator.toPos[0]}, Column: {operator.fromPos[1]}~{operator.toPos[1]}: Operator '{operator.value}' cannot be applied to types '{leftType}' and '{rightType}'")
            if operator.value in {'/'} and (leftType != 'boolean' or rightType != 'boolean'):
                self.errors.append(f"Line: {operator.fromPos[0]}~{operator.toPos[0]}, Column: {operator.fromPos[1]}~{operator.toPos[1]}: Operator '{operator.value}' can only be applied to boolean types, but got '{leftType}' and '{rightType}'")
            if operator.value in {'='}:
                if not self._isCompatibleType(leftType, rightType):
                    self.errors.append(f"Line: {operator.fromPos[0]}~{operator.toPos[0]}, Column: {operator.fromPos[1]}~{operator.toPos[1]}: Operator '{operator.value}' cannot be applied to types '{leftType}' and '{rightType}'")
            if operator.value in {'<', '>', '</=', '>/='}:
                if not self._isComparable(leftType, rightType):
                    self.errors.append(f"Line: {operator.fromPos[0]}~{operator.toPos[0]}, Column: {operator.fromPos[1]}~{operator.toPos[1]}: Operator '{operator.value}' cannot be applied to types '{leftType}' and '{rightType}'")
            return opNode(operator=operator.value, left=left, right=right)
        self.nextToken(')', "Missing ')' after operator args")
        if leftType != 'boolean':
            self.errors.append(f"Line: {operator.fromPos[0]}~{operator.toPos[0]}, Column: {operator.fromPos[1]}~{operator.toPos[1]}: Operator '{operator.value}' can only be applied to boolean types, but got '{leftType}'")
        return opNode(operator=operator.value, left=left, right=None)

    def parseLoop(self):
        self.nextToken('loop', "Missing 'loop' keyword")
        self.nextToken('.', "Missing '.' between keyword and modifier")
        modifier = self.nextToken()
        if modifier.value == 'while':
            condition = None
            statements = []
            self.nextToken('.', "Missing '.' after while modifier")
            modifier1 = self.nextToken()
            if modifier1.value == 'when':
                self.nextToken('(', "Missing '(' after modifier")
                condition = self.parseExpression()
                self.nextToken(')', "Missing ')' after condition")
            elif modifier1.value == 'codes':
                self.nextToken('(', "Missing '(' after codes modifier")
                self.nextToken('{', "Missing '{' after codes modifier")
                beforeDefinedVarNames = self.definedVarName
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.definedVarName = beforeDefinedVarNames
                self.nextToken('}', "Missing '}' after codes body")
                self.nextToken(')', "Missing ')' after codes body")
            else:
                self.errors.append(f"Line: {modifier1.fromPos[0]}~{modifier1.toPos[0]}, Column: {modifier1.fromPos[1]}~{modifier1.toPos[1]}: Unknown loop modifier: {self.nowToken().value}")
            
            self.nextToken('.', "Missing '.' between while modifiers")
            modifier2 = self.nextToken()
            if modifier2.value == 'when':
                self.nextToken('(', "Missing '(' after when modifier")
                condition = self.parseExpression()
                self.nextToken(')', "Missing ')' after when condition")
            elif modifier2.value == 'codes':
                self.nextToken('(', "Missing '(' after codes modifier")
                self.nextToken('{', "Missing '{' after codes modifier")
                beforeDefinedVarNames = self.definedVarName
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.definedVarName = beforeDefinedVarNames
                self.nextToken('}', "Missing '}' after codes body")
                self.nextToken(')', "Missing ')' after codes body")
            else:
                self.errors.append(f"Line: {modifier2.fromPos[0]}~{modifier2.toPos[0]}, Column: {modifier2.fromPos[1]}~{modifier2.toPos[1]}: Unknown loop modifier: {self.nowToken().value}")
            
            if condition is None:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Missing condition for while loop")
            if not statements:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Missing body for while loop")

            self.nextToken(';', "Missing ';' after while loop")

            return loopWhileNode(condition=condition, body=statements)
        elif modifier.value == 'for':
            var = None
            statements = []
            rangeFrom = None
            rangeTo = None
            self.nextToken('.', "Missing '.' after for modifier")
            modifier1 = self.nextToken()
            if modifier1.value == 'range':
                self.nextToken('(', "Missing '(' after range modifier")
                rangeFrom = self.parseExpression()
                self.nextToken(',', "Missing ',' between range values")
                rangeTo = self.parseExpression()
                self.nextToken(',', "Missing ',' between range value and variable")
                if self.nowToken().value != 'vars':
                    self.errors.append(f"Line: {modifier1.fromPos[0]}~{modifier1.toPos[0]}, Column: {modifier1.fromPos[1]}~{modifier1.toPos[1]}: Missing variable for for loop: {self.nowToken().value}")
                self.nextToken('vars', "Missing 'vars' keyword in for loop range")
                self.nextToken('.', "Missing '.' between vars and declaration")
                type = self.nowToken()
                if type.value == 'new':
                    self.nextToken('new', "Missing 'new' modifier for variable declaration")
                    self.nextToken('(', "Missing '(' after new modifier")
                    varName = self.nextToken()
                    self.nextToken(',', "Missing ',' between variable args")
                    varType = self.nextToken()
                    self.nextToken(',', "Missing ',' between variable args")
                    value = self.parseExpression()
                    self.nextToken(')', "Missing ')' after variable declaration")
                    if varName.value in self.notSupportVarName or any(keyword in varName.value for keyword in self.notSupportVarNameIncludes):
                        self.errors.append(f"Line: {varName.fromPos[0]}~{varName.toPos[0]}, Column: {varName.fromPos[1]}~{varName.toPos[1]}: Variable name '{varName.value}' contains invalid character(s)")
                    if varName.value in self.definedVarName:
                        self.errors.append(f"Line: {varName.fromPos[0]}~{varName.toPos[0]}, Column: {varName.fromPos[1]}~{varName.toPos[1]}: Variable name '{varName.value}' has been defined")
                    self.definedVarName.append(varName.value)
                    self.definedVarTypes[varName.value] = varType.value
                    var = forRangeVarNode(name=varName.value, value=value, newType=varType.value)
                else:
                    varName = self.nextToken()
                    if not varName.value in self.definedVarName:
                        self.errors.append(f"Line: {varName.fromPos[0]}~{varName.toPos[0]}, Column: {varName.fromPos[1]}~{varName.toPos[1]}: Variable '{varName.value}' hasn't been defined")
                    var = forRangeVarNode(name=varName.value, value=None, newType='')
                self.nextToken(')', "Missing ')' after range declaration")
            elif modifier1.value == 'codes':
                self.nextToken('(', "Missing '(' after codes modifier")
                self.nextToken('{', "Missing '{' after codes modifier")
                beforeDefinedVarNames = self.definedVarName
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.definedVarName = beforeDefinedVarNames
                if var != None and var.value != None:
                    self.definedVarName.remove(var.name)
                self.nextToken('}', "Missing '}' after codes body")
                self.nextToken(')', "Missing ')' after codes body")
            else:
                self.errors.append(f"Line: {modifier1.fromPos[0]}~{modifier1.toPos[0]}, Column: {modifier1.fromPos[1]}~{modifier1.toPos[1]}: Unknown loop modifier: {self.nowToken().value}.")
            
            self.nextToken('.', "Missing '.' between for modifiers")
            modifier2 = self.nextToken()
            if modifier2.value == 'range':
                self.nextToken('(', "Missing '(' after range modifier")
                rangeFrom = self.parseExpression()
                self.nextToken(',', "Missing ',' between range values")
                rangeTo = self.parseExpression()
                self.nextToken(',', "Missing ',' between range value and variable")
                if self.nowToken().value != 'vars':
                    self.errors.append(f"Line: {modifier2.fromPos[0]}~{modifier2.toPos[0]}, Column: {modifier2.fromPos[1]}~{modifier2.toPos[1]}: Missing variable for for loop: {self.nowToken().value}")
                self.nextToken('vars', "Missing 'vars' keyword in for loop range")
                self.nextToken('.', "Missing '.' between vars and declaration")
                type = self.nowToken()
                if type.value == 'new':
                    self.nextToken('new', "Missing 'new' modifier for variable declaration")
                    self.nextToken('(', "Missing '(' after new modifier")
                    varName = self.nextToken()
                    self.nextToken(',', "Missing ',' between variable args")
                    varType = self.nextToken()
                    self.nextToken(',', "Missing ',' between variable args")
                    value = self.parseExpression()
                    self.nextToken(')', "Missing ')' after variable declaration")
                    if varName.value in self.notSupportVarName or any(keyword in varName.value for keyword in self.notSupportVarNameIncludes):
                        self.errors.append(f"Line: {varName.fromPos[0]}~{varName.toPos[0]}, Column: {varName.fromPos[1]}~{varName.toPos[1]}: Variable name '{varName.value}' contains invalid character(s)")
                    if varName.value in self.definedVarName:
                        self.errors.append(f"Line: {varName.fromPos[0]}~{varName.toPos[0]}, Column: {varName.fromPos[1]}~{varName.toPos[1]}: Variable name '{varName.value}' has been defined.")
                    self.definedVarName.append(varName.value)
                    self.definedVarTypes[varName.value] = varType.value
                    var = forRangeVarNode(name=varName.value, value=value, newType=varType.value)
                else:
                    varName = self.nextToken()
                    if not varName.value in self.definedVarName:
                        self.errors.append(f"Line: {varName.fromPos[0]}~{varName.toPos[0]}, Column: {varName.fromPos[1]}~{varName.toPos[1]}: Variable '{varName.value}' hasn't been defined")
                    var = forRangeVarNode(name=varName.value, value=None, newType='')
                self.nextToken(')', "Missing ')' after range declaration")
            elif modifier2.value == 'codes':
                self.nextToken('(', "Missing '(' after codes modifier")
                self.nextToken('{', "Missing '{' after codes modifier")
                beforeDefinedVarNames = self.definedVarName
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.definedVarName = beforeDefinedVarNames
                if var != None and var.value != None:
                    self.definedVarName.remove(var.name)
                self.nextToken('}', "Missing '}' after codes body")
                self.nextToken(')', "Missing ')' after codes body")
            else:
                self.errors.append(f"Line: {modifier2.fromPos[0]}~{modifier2.toPos[0]}, Column: {modifier2.fromPos[1]}~{modifier2.toPos[1]}: Unknown loop modifier: {self.nowToken().value}.")

            if var is None:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Missing variable for for loop")
                var = forRangeVarNode(name="", value=None, newType='')
            if rangeFrom is None:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Missing start value for for loop")
            if rangeTo is None:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Missing end value for for loop")
            if statements == []:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Missing body for for loop")

            self.nextToken(';', "Missing ';' after for loop")

            return loopForNode(var=var, rangeFrom=rangeFrom, rangeTo=rangeTo, body=statements)
        elif modifier.value == 'stop':
            self.nextToken('(', "Missing '(' after stop modifier")
            self.nextToken(')', "Missing ')' after stop modifier")
            self.nextToken(';', "Missing ';' after stop loop")
            return loopNode(stop=True, skip=False)
        elif modifier.value == 'skip':
            self.nextToken('(', "Missing '(' after skip modifier")
            self.nextToken(')', "Missing ')' after skip modifier")
            self.nextToken(';', "Missing ';' after skip loop")
            return loopNode(stop=False, skip=True)
        elif modifier.value == 'if':
            condition = None
            statements = []
            elseStatements = []
            self.nextToken('.', "Missing '.' after if modifier")
            modifier1 = self.nextToken()
            if modifier1.value == 'when':
                self.nextToken('(', "Missing '(' after when modifier")
                condition = self.parseExpression()
                self.nextToken(')', "Missing ')' after when condition")
            elif modifier1.value == 'codes':
                self.nextToken('(', "Missing '(' after codes modifier")
                self.nextToken('{', "Missing '{' after codes modifier")
                beforeDefinedVarNames = self.definedVarName
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.definedVarName = beforeDefinedVarNames
                self.nextToken('}', "Missing '}' after codes body")
                self.nextToken(')', "Missing ')' after codes body")
            elif modifier1.value == 'else':
                self.nextToken('(', "Missing '(' after else modifier")
                self.nextToken('{', "Missing '{' after else modifier")
                beforeDefinedVarNames = self.definedVarName
                while self.nowToken().value != '}':
                    elseStatements.append(self.parseStatement())
                self.definedVarName = beforeDefinedVarNames
                self.nextToken('}', "Missing '}' after else body")
                self.nextToken(')', "Missing ')' after else body")
            else:
                self.errors.append(f"Line: {modifier1.fromPos[0]}~{modifier1.toPos[0]}, Column: {modifier1.fromPos[1]}~{modifier1.toPos[1]}: Unknown loop modifier: {modifier1.value}")

            self.nextToken('.', "Missing '.' between if modifiers")
            modifier2 = self.nextToken()
            if modifier2.value == 'when':
                self.nextToken('(', "Missing '(' after when modifier")
                condition = self.parseExpression()
                self.nextToken(')', "Missing ')' after when condition")
            elif modifier2.value == 'codes':
                self.nextToken('(', "Missing '(' after codes modifier")
                self.nextToken('{', "Missing '{' after codes modifier")
                beforeDefinedVarNames = self.definedVarName
                while self.nowToken().value != '}':
                    statements.append(self.parseStatement())
                self.definedVarName = beforeDefinedVarNames
                self.nextToken('}', "Missing '}' after codes body")
                self.nextToken(')', "Missing ')' after codes body")
            elif modifier2.value == 'else':
                self.nextToken('(', "Missing '(' after else modifier")
                self.nextToken('{', "Missing '{' after else modifier")
                beforeDefinedVarNames = self.definedVarName
                while self.nowToken().value != '}':
                    elseStatements.append(self.parseStatement())
                self.definedVarName = beforeDefinedVarNames
                self.nextToken('}', "Missing '}' after else body")
                self.nextToken(')', "Missing ')' after else body")
            else:
                self.errors.append(f"Line: {modifier2.fromPos[0]}~{modifier2.toPos[0]}, Column: {modifier2.fromPos[1]}~{modifier2.toPos[1]}: Unknown loop modifier: {modifier2.value}")

            if (self.nowToken().value != ';'):
                self.nextToken('.', "Missing '.' between if modifiers")
                modifier3 = self.nextToken()
                if modifier3.value == 'when':
                    self.nextToken('(', "Missing '(' after when modifier")
                    condition = self.parseExpression()
                    self.nextToken(')', "Missing ')' after when condition")
                elif modifier3.value == 'codes':
                    self.nextToken('(', "Missing '(' after codes modifier")
                    self.nextToken('{', "Missing '{' after codes modifier")
                    beforeDefinedVarNames = self.definedVarName
                    while self.nowToken().value != '}':
                        statements.append(self.parseStatement())
                    self.definedVarName = beforeDefinedVarNames
                    self.nextToken('}', "Missing '}' after codes body")
                    self.nextToken(')', "Missing ')' after codes body")
                elif modifier3.value == 'else':
                    self.nextToken('(', "Missing '(' after else modifier")
                    self.nextToken('{', "Missing '{' after else modifier")
                    beforeDefinedVarNames = self.definedVarName
                    while self.nowToken().value != '}':
                        elseStatements.append(self.parseStatement())
                    self.definedVarName = beforeDefinedVarNames
                    self.nextToken('}', "Missing '}' after else body")
                    self.nextToken(')', "Missing ')' after else body")
                else:
                    self.errors.append(f"Line: {modifier3.fromPos[0]}~{modifier3.toPos[0]}, Column: {modifier3.fromPos[1]}~{modifier3.toPos[1]}: Unknown loop modifier: {modifier3.value}")

            self.nextToken(';', "Missing ';' after if loop")

            if condition is None:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Missing condition for if loop.")
            if statements == []:
                self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Missing body for if loop.")

            return loopIfNode(condition=condition, body=statements,elseBody=elseStatements)
        else:
            self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Unknown loop modifier: {self.nowToken().value}")
    
    def parseTerminal(self):
        self.nextToken('ter', "Missing 'ter' keyword")
        self.nextToken('.', "Missing '.' after ter keyword")
        modifier = self.nextToken()
        if modifier.value == 'otpt':
            self.nextToken('(', "Missing '(' after otpt modifier")
            value = self.parseExpression()
            self.nextToken(')', "Missing ')' after otpt expression")
            self.nextToken(';', "Missing ';' after otpt statement")
            return terOtptNode(text=value)
        elif modifier.value == 'inpt':
            self.nextToken('(', "Missing '(' after inpt modifier")
            self.nextToken('vars', "Missing 'vars' keyword in input statement")
            self.nextToken('.', "Missing '.' after vars keyword")
            value = self.nextToken()
            self.nextToken(')', "Missing ')' after inpt statement")
            self.nextToken(';', "Missing ';' after inpt statement")
            if not value.value in self.definedVarName:
                self.errors.append(f"Line: {value.fromPos[0]}~{value.toPos[0]}, Column: {value.fromPos[1]}~{value.toPos[1]}: Variable '{value.value}' hasn't been defined")
            return terInptNode(var=value.value)
        else:
            self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Unknown terminal modifier: {self.nowToken().value}")
    
    def parseUsing(self):
        self.nextToken('using', "Missing 'using' keyword")
        self.nextToken('.', "Missing '.' after using keyword")
        modifier = self.nextToken()
        if modifier.value == 'tips':
            self.nextToken('(', "Missing '(' after tips modifier")
            text = self.parseExpression()
            self.nextToken(')', "Missing ')' after tips expression")
            self.nextToken(';', "Missing ';' after tips statement")
            return tipNode(text=text)
        else:
            self.errors.append(f"Line: {modifier.fromPos[0]}~{modifier.toPos[0]}, Column: {modifier.fromPos[1]}~{modifier.toPos[1]}: Unknown using modifier: {self.nowToken().value}. (use is in development...)")

from .tokens import *

class Lexer:
    def __init__(self, sourceCode: str):
        self.source = sourceCode
        self.pos = 0
        self.errors = []
    
    def _getPositionInfo(self, pos: int):
        line = self.source[:pos].count('\n') + 1
        lastNewline = self.source.rfind('\n', 0, pos)
        if lastNewline == -1:
            col = pos
        else:
            col = pos - lastNewline
        return (line, col)
    
    def nextToken(self) -> Token:
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            self.pos += 1
        if self.pos >= len(self.source):
            return Token(TokenType.EOF, "", fromPos=self._getPositionInfo(self.pos), toPos=self._getPositionInfo(self.pos))
        
        char = self.source[self.pos]

        if char.isdigit() or (char == '.' and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit()):
            start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
                self.pos += 1
            return Token(TokenType.NUMBER, self.source[start:self.pos], fromPos=self._getPositionInfo(start), toPos=self._getPositionInfo(self.pos-1))
        if char in SYMBOLS:
            self.pos += 1
            return Token(TokenType.SYMBOL, char, fromPos=self._getPositionInfo(self.pos-1), toPos=self._getPositionInfo(self.pos-1))
        if char in OPERATORS:
            firstChar = char
            startPos = self.pos
            endPos = self.pos
            self.pos += 1
            if self.source[self.pos] == '/':
                firstChar += self.source[self.pos]
                self.pos += 1
                firstChar += self.source[self.pos]
                endPos=self.pos
                self.pos += 1
            return Token(TokenType.OPERATOR, firstChar, fromPos=self._getPositionInfo(startPos), toPos=self._getPositionInfo(endPos))
        if char == '"':
            self.pos += 1
            start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos] != '"' or (self.source[self.pos] == '"' and self.source[self.pos-1] == '\\')):
                self.pos += 1
            value = self.source[start:self.pos]
            self.pos += 1
            return Token(TokenType.TEXT, value, fromPos=self._getPositionInfo(start), toPos=self._getPositionInfo(self.pos-1))
        if char.isalpha() or char == '_':
            start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self.pos += 1
            value = self.source[start:self.pos]
            fromPos = self._getPositionInfo(start)
            toPos = self._getPositionInfo(self.pos-1)
            if value in KEYWORDS:
                return Token(TokenType.KEYWORD, value, fromPos=fromPos, toPos=toPos)
            elif value in TYPES:
                return Token(TokenType.TYPE, value, fromPos=fromPos, toPos=toPos)
            elif value in BOOLEANS:
                return Token(TokenType.BOOLEAN, value, fromPos=fromPos, toPos=toPos)
            else:
                return Token(TokenType.MODIFIER, value, fromPos=fromPos, toPos=toPos)

        pos = self._getPositionInfo(self.pos)
        self.errors.append(f"Line: {pos[0]}, Column: {pos[1]}: Unknown character: {char}")
        return Token(TokenType.UNKNOWN, "", fromPos=pos, toPos=pos)
    
    def scan_all(self):
        tokens = []
        while True:
            token = self.nextToken()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

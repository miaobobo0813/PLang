from .tokens import *

class Lexer:
    def __init__(self, sourceCode: str):
        self.source = sourceCode
        self.pos = 0
    
    def nextToken(self) -> Token:
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            self.pos += 1
        if self.pos >= len(self.source):
            return Token(TokenType.EOF, "")
        
        char = self.source[self.pos]

        if char.isdigit() or (char == '.' and self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit()):
            start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '.'):
                self.pos += 1
            return Token(TokenType.NUMBER, self.source[start:self.pos])
        if char in SYMBOLS:
            self.pos += 1
            return Token(TokenType.SYMBOL, char)
        if char in OPERATORS:
            firstChar = char
            self.pos += 1
            if self.source[self.pos] == '/':
                firstChar += self.source[self.pos]
                self.pos += 1
                firstChar += self.source[self.pos]
                self.pos += 1
            return Token(TokenType.OPERATOR, firstChar)
        if char == '"':
            self.pos += 1
            start = self.pos
            while self.pos < len(self.source) and self.source[self.pos] != '"':
                self.pos += 1
            value = self.source[start:self.pos]
            self.pos += 1
            return Token(TokenType.TEXT, value)
        if char.isalpha() or char == '_':
            start = self.pos
            while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                self.pos += 1
            value = self.source[start:self.pos]
            if value in KEYWORDS:
                return Token(TokenType.KEYWORD, value)
            elif value in TYPES:
                return Token(TokenType.TYPE, value)
            elif value in BOOLEANS:
                return Token(TokenType.BOOLEAN, value)
            else:
                return Token(TokenType.MODIFIER, value)

        raise ValueError(f"Unexpected character: {char}")
    
    def scan_all(self):
        tokens = []
        while True:
            token = self.nextToken()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens

test_plang_code = """
using.tips("PLang 编译器测试");
vars.new(i, number, 1);
vars.new(pi, dotNum, 3.14);
loop.while.when(>/=(vars.i, 8)).codes({
    ter.otpt("当前 i 的值是：");
    vars.i.modify(*(var, 2));
    ter.otpt(vars.i);
    ter.otpt("\\n");
});
ter.otpt(vars.pi);
ter.otpt("测试结束！");
"""

from lexer import Lexer
from parser import Parser
from compile import compile

lexer = Lexer(test_plang_code)
tokens = lexer.scan_all()
parser = Parser(tokens)
ast = parser.parseProgram()
compiler = compile()
c_code = compiler.visit(ast)
print(c_code)
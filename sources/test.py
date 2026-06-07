test_plang_code = """
using.tips("This is a comment and not be compile.");
vars.new(i, number, 1);
vars.new(pi, dotNum, 3.1415926);
loop.for.range(1, 8, vars.new(j, number, 1)).codes({
    ter.otpt("当前 i 的值是：");
    using.tips("vars.i.modify(*(var, 2));");
    ter.otpt(vars.i);
    loop.skip();
    ter.otpt("\\n");
});
ter.otpt(vars.pi);
vars.pi.modify(+(var, 1));
ter.otpt("\\n");
ter.otpt(vars.pi);
ter.otpt("\\n");
vars.new(bool, boolean, yes);
ter.otpt("测试结束！");
"""

from lexer import Lexer
from parser import Parser
from compile import compile
import subprocess
import os

lexer = Lexer(test_plang_code)
tokens = lexer.scan_all()
parser = Parser(tokens)
print("Syntax errors:")
ast = parser.parseProgram()
print("None")
print(ast)
compiler = compile()
c_code = compiler.visit(ast)
print(c_code)

filename = f"{__name__}.c"
with open(filename, 'w', encoding='utf-8') as f:
    f.write(c_code)
cmd = ['gcc', filename, '-o', f"{__name__}.exe"]
errors = subprocess.run(cmd, capture_output=True, text=True)
print("Logic errors:")
if errors.stderr == '':
    print("None")
else:
    print(errors.stderr)
os.remove(filename)

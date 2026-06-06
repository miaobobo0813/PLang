from .lexer import Lexer
from .parser import Parser
from .compile import compile
from pathlib import Path
from .__init__ import __version__
import subprocess
import os
import sys
import tempfile
import argparse

def compiler(inputFile, outputFile=None, verbose=None, run=False):
    if sys.platform != 'win32':
        print('Error: PLang only support for Windows.')
        return False
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            codes = f.read()
    except FileNotFoundError:
        print(f'Error: file \"{inputFile}\" do not exist.')
        return False
    except Exception as e:
        print(f'Error: {e}')
        return False

    if outputFile:
        exeFile = outputFile
    else:
        exeFile = Path(inputFile).stem+'.exe'

    try:
        lexer = Lexer(codes)
        tokens = lexer.scan_all()
        parser = Parser(tokens)
        ast = parser.parseProgram()
        if verbose:
            print("AST Tree:")
            print(ast)

        compiler = compile()
        cCode = compiler.visit(ast)
        if verbose:
            print("C Code:")
            print(cCode)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write(cCode)
            cFile = f.name

        cmd = ['gcc', cFile, '-o', exeFile]
        result = subprocess.run(cmd, capture_output=True, text=True)
        os.remove(cFile)

        if result.returncode != 0:
            print("Logic error:")
            print(result.stderr)
            return False

        if run:
            result = subprocess.run([exeFile], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', help='Path to your source code.')
    parser.add_argument('-o', '--output', help='')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show more details about the compile.')
    parser.add_argument('-r', '--run', action='store_true', help='Run the .exe after compile.')
    parser.add_argument('--version', action='version', version=f'PLang Compiler {__version__}')

    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        return 1

    if not os.path.exists(args.file):
        print(f'Error: {args.file} do not exists. Check the spell and try again.')

    return compiler(args.file, args.output, verbose=args.verbose, run=args.run)

if __name__ == "__main__":
    sys.exit(main())
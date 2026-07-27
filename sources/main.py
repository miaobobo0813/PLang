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
import re

def formatGPPOutput(output: str, compiler: compile):
    lines = output.split('\n')
    formatted = []
    for line in lines:
        if '.cpp:' in line and 'error:' in line:
            if "In function 'int main()':" in line:
                continue
            else:
                pattern = r"error:\s*(.+?)(?:\n|$)"
                match = re.search(pattern, line)
                if match:
                    errorLine = match.group(1)
                    errorLine = re.sub(r'\s*\[-[a-zA-Z0-9-]+\]\s*$', '', errorLine)
                    for (old, new) in compiler.typeFormat.items():
                        errorLine = errorLine.replace(new, old)
                    errorLine = errorLine.replace('const char*', 'text')
                    errorLine = re.sub(r'const\schar\s\[\d+\]', 'text', errorLine)
                    errorLine = f"Line: ?, Column: ?: {errorLine}"
                    formatted.append(errorLine)
    return formatted

def compiler(inputFile=None, outputFile=None, verbose=None, run=False, noOutput=False, codes=None):
    if sys.platform != 'win32':
        print('PLang only support for Windows.', file=sys.stderr)
        return 1

    if codes == None and inputFile != None:
        try:
            with open(inputFile, 'r', encoding='utf-8') as f:
                codes = f.read()
        except FileNotFoundError:
            print(f'File \"{inputFile}\" do not exist.', file=sys.stderr)
            return 1
        except Exception as e:
            print(f'{e}', file=sys.stderr)
            return -1

    if outputFile:
        exeFile = outputFile
    elif inputFile != None:
        exeFile = Path(inputFile).stem+'.exe'
    else:
        exeFile = "PLang Code Output.exe"

    try:
        if codes == None:
            lexer = Lexer("")
        else:
            lexer = Lexer(codes)
        tokens = lexer.scan_all()
        if lexer.errors != []:
            for error in lexer.errors:
                print(error, file=sys.stderr)
            return 1
        parser = Parser(tokens)
        ast = parser.parseProgram()
        if parser.errors != []:
            for error in parser.errors:
                print(error, file=sys.stderr)
            return 1
        if verbose:
            print("AST Tree:")
            print(ast)

        compiler = compile()
        cCode = compiler.visit(ast)
        if verbose:
            print("C++ Code:")
            print(cCode)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(cCode)
            cFile = f.name

        cmd = ['g++', cFile]
        if noOutput:
            cmd.append('-fsyntax-only')
        else:
            cmd.append('-o')
            cmd.append(exeFile)
        result = subprocess.run(cmd, capture_output=True, text=True)
        os.remove(cFile)

        if result.returncode != 0:
            errors = formatGPPOutput(result.stderr, compiler=compiler)
            for error in errors:
                print(error, file=sys.stderr)
            return 1

        print("Build success!")

        if noOutput:
            return 0

        if run:
            result = subprocess.run([exeFile], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr, file=sys.stderr)

        return 0
    except KeyError as e:
        print(f"Unknown variable {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(e, file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(prog="plang")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('file', nargs='?', help='Path to your source code.')
    group.add_argument('--code', type=str, help='Execute code passed as string.')
    parser.add_argument('-o', '--output', help='')
    parser.add_argument('-v', '--verbose', action='store_true', help='Show more details about the compile.')
    parser.add_argument('-r', '--run', action='store_true', help='Run the .exe after compile.')
    parser.add_argument('--no-output', action='store_true', help='DO NOT compile .exe file.')
    parser.add_argument('--version', action='version', version=f'PLang Compiler {__version__}')

    args = parser.parse_args()

    if args.code:
        return compiler(outputFile=args.output, verbose=args.verbose, run=args.run, noOutput=args.no_output, codes=args.code)

    if not args.file:
        parser.print_help()
        return 1

    if not os.path.exists(args.file):
        print(f'{args.file} do not exists. Check the spell and try again.')
        return 1

    return compiler(args.file, args.output, verbose=args.verbose, run=args.run, noOutput=args.no_output)

if __name__ == "__main__":
    sys.exit(main())
# PLang Compiler

> **NOTICE**: This project is under active development. Some features may not be final.

A simple, readable programming language that compiles to C++.

## Features

- **Simple syntax** - Keyword-modifier chains make code easy to read and write
- **Cross-platform** - Works on Windows, macOS, and Linux
- **Compiles to C++** - Leverages G++ for native performance
- **Less dependencies** - Only requires Python and G++

## Quick Start

### Build

#### Windows
```Powershell
git clone https://github.com/miaobobo0813/PLang.git
Set-Location PLang\sources
pip install pyinstaller
PyInstaller --onefile main.py --path=. 
```

#### macOS 
```zsh
git clone https://github.com/miaobobo0813/PLang.git
cd PLang/sources
python3 -m pip install pyinstaller
python3 -m PyInstaller --onefile main.py
```

#### Linux
```bash
git clone https://github.com/miaobobo0813/PLang.git
cd PLang
# You also can use yum/pacman for other Linuxs.
sudo apt update
sudo apt install python3.12-venv python3-pip
python3 -m venv venv
source venv/bin/activate
pip install pyinstaller
cd sources
pyinstaller --path=. --onefile main.py
```

### Install

1. Download release from [release page](https://github.com/miaobobo0813/PLang/releases).
2. Follow the steps written in release note to install the compiler.

### Command Line Options

| Option | Description |
|--------|-------------|
| `file` | Path to your `.plang` source file |
| `--code CODE` | Execute code directly from string |
| `-o, --output FILE` | Specify output executable name |
| `-v, --verbose` | Show AST and generated C++ code |
| `-r, --run` | Run the compiled program after building |
| `--no-output` | Check syntax without generating executable |
| `--version` | Display compiler version |

## Example

Here's a PLang program that calculates factorial:

```plang
using.tips("Factorial Calculator");

vars.new(n, number, 5);
vars.new(result, number, 1);
vars.new(i, number, 1);

loop.for.range(1, vars.n, vars.i).codes({
    vars.result.modify(*(var, vars.i));
});

ter.otpt("Factorial of ");
ter.otpt(vars.n);
ter.otpt(" is ");
ter.otpt(vars.result);
ter.otpt("\n");
```

Save as `factorial.plang` and run:
```bash
python -m sources.main factorial.plang -r
# Output: Factorial of 5 is 120
```

## How It Works

```
PLang Source → Lexer → Parser → C++ Generator → G++ → Executable
```

1. **Lexer** - Tokenizes PLang source code
2. **Parser** - Builds an Abstract Syntax Tree (AST)
3. **Compiler** - Generates C++ code from AST
4. **G++** - Compiles to native executable

## Dependencies

- **Python 3.6+** - To run the compiler
- **G++ (GCC)** - To compile generated C++ code

  | Platform | Install Command |
  |----------|-----------------|
  | Windows | Install [MinGW-w64](https://www.mingw-w64.org/) |
  | macOS | `xcode-select --install` |
  | Linux | `sudo apt install g++` (Ubuntu/Debian) |

## Project Structure

```
PLang/
├── sources/
│   ├── __init__.py      # Package version
│   ├── compile.py       # C++ code generator
│   ├── lexer.py         # Lexical analyzer
│   ├── main.py          # CLI entry point
│   ├── nodes.py         # AST node definitions
│   ├── parser.py        # Syntax analyzer
│   └── tokens.py        # Token definitions
├── plang.bat            # Windows launcher
├── setup.ps1            # Windows installation script
├── Language_Guide.md    # Complete language documentation
└── README.md            # This file
```

## Documentation

- [Language Guide](Language_Guide.md) - Complete PLang syntax reference
- [Report Issues](https://github.com/miaobobo0813/PLang/issues)

## License

[MIT](LICENSE)
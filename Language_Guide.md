# PLang Language Guide

## Basic Syntax

**Every statement follows this pattern:**
```
keyword.modifier().modifier()...;
```

**Example:**
```plang
vars.new(i, number, 0);
using.tips("TODO: Fix this later");
```

Comments are written using `using.tips()`.

---

## Keywords

### 1. `using` - Utilities

| Modifier | Description | Example |
|----------|-------------|---------|
| `tips(text)` | Add a comment to your code | `using.tips("TODO: Fix this later");` |

> **Note**: `using.use()` for importing files is currently under development.

---

### 2. `vars` - Variables

| Modifier | Description | Example |
|----------|-------------|---------|
| `new(name, type, value)` | Create a new variable | `vars.new(age, number, 18);` |
| `[name]` | Reference a variable | `vars.age` |
| `modify(value)` | Change a variable's value (you can use `var` to reference the old value) | `vars.age.modify(+(var, 1));` |

#### Types

| Type | Description | Example Value |
|------|-------------|---------------|
| `number` | Integer | `42`, `-5`, `0` |
| `dotNum` | Floating point | `3.14`, `-0.5` |
| `text` | String | `"Hello"`, `"PLang"` |
| `boolean` | True/False | `yes`, `no` |

#### Examples

```plang
using.tips("Variable declaration");
vars.new(x, number, 5);
vars.new(pi, dotNum, 3.14159);
vars.new(name, text, "John");
vars.new(isReady, boolean, yes);

using.tips("Variable modification");
vars.x.modify(+(var, 10));  using.tips("x becomes 15");
vars.name.modify("Jane");   using.tips("name becomes Jane");
```

---

### 3. `ter` - Terminal I/O

| Modifier | Description | Example |
|----------|-------------|---------|
| `otpt(text)` | Print to console | `ter.otpt("Hello, World!");` |
| `inpt(variable)` | Read user input | `ter.inpt(vars.age);` |

#### Examples

```plang
using.tips("Basic output");
ter.otpt("Hello, World!");

using.tips("User input");
vars.new(name, text, "");
ter.otpt("What's your name? ");
ter.inpt(vars.name);
ter.otpt("Hello, ");
ter.otpt(vars.name);
ter.otpt("!\n");

using.tips("Number input");
vars.new(age, number, 0);
ter.otpt("Enter your age: ");
ter.inpt(vars.age);
ter.otpt("You are ");
ter.otpt(vars.age);
ter.otpt(" years old.\n");
```

---

### 4. `loop` - Control Flow

#### while Loop

```plang
loop.while.when(condition).codes({
    using.tips("Code to execute");
});
```

**Example:**
```plang
using.tips("While loop - count to 5");
vars.new(count, number, 1);
loop.while.when(</=(vars.count, 5)).codes({
    ter.otpt(vars.count);
    ter.otpt(" ");
    vars.count.modify(+(var, 1));
});
using.tips("Output: 1 2 3 4 5");
```

---

#### for Loop

```plang
loop.for.range(start, end, variable).codes({
    using.tips("Code to execute");
});
```

**Example:**
```plang
using.tips("For loop - print 1 to 10");
vars.new(i, number, 0);
loop.for.range(1, 10, vars.i).codes({
    ter.otpt(vars.i);
    ter.otpt(" ");
});
using.tips("Output: 1 2 3 4 5 6 7 8 9 10");
```

**Example with variable:**
```plang
using.tips("For loop with custom range");
vars.new(n, number, 5);
vars.new(i, number, 0);
loop.for.range(1, vars.n, vars.i).codes({
    ter.otpt(vars.i);
    ter.otpt(" ");
});
using.tips("Output: 1 2 3 4 5");
```

---

#### if Statement

```plang
loop.if.when(condition).codes({
    using.tips("Code when true");
}).else({
    using.tips("Code when false (optional)");
});
```

**Example:**
```plang
using.tips("If statement");
vars.new(score, number, 85);
loop.if.when(>/=(vars.score, 60)).codes({
    ter.otpt("Pass!");
}).else({
    ter.otpt("Fail!");
});
using.tips("Output: Pass!");
```

**Example without else:**
```plang
using.tips("If without else");
vars.new(age, number, 18);
loop.if.when(>/=(vars.age, 18)).codes({
    ter.otpt("You can vote!");
});
```

---

#### Loop Control

| Modifier | Description | Example |
|----------|-------------|---------|
| `stop()` | Exit the loop immediately | `loop.stop();` |
| `skip()` | Skip to next iteration | `loop.skip();` |

**Example:**
```plang
using.tips("Loop control example");
vars.new(i, number, 0);
loop.while.when(yes).codes({
    vars.i.modify(+(var, 1));
    
    loop.if.when(=(vars.i, 5)).codes({
        loop.stop();  using.tips("Exit when i reaches 5.");
    });
    
    loop.if.when(=(vars.i, 3)).codes({
        loop.skip();  using.tips("Skip printing 3");
    });
    
    ter.otpt(vars.i);
    ter.otpt(" ");
});
using.tips("Output: 1 2 4");
```

---

### 5. `operators` - Operations

Operators can be used in two ways:
1. With `operators.` prefix: `operators.+(left, right)`
2. Directly: `+(left, right)`

#### Arithmetic Operators

| Operator | Operation | Syntax | Returns |
|----------|-----------|--------|---------|
| `+` | Addition | `+(left, right)` | number/dotNum |
| `-` | Subtraction | `-(left, right)` | number/dotNum |
| `*` | Multiplication | `*(left, right)` | number/dotNum |
| `` ` `` | Division | `` `(left, right) `` | dotNum |
| `%` | Modulo | `%(left, right)` | number |

**Examples:**
```plang
using.tips("Arithmetic operators");
vars.new(a, number, 10);
vars.new(b, number, 3);

vars.new(sum, number, +(vars.a, vars.b));         using.tips("13");
vars.new(diff, number, -(vars.a, vars.b));        using.tips("7");
vars.new(product, number, *(vars.a, vars.b));     using.tips("30");
vars.new(quotient, dotNum, `(vars.a, vars.b));    using.tips("3.333...");
vars.new(remainder, number, %(vars.a, vars.b));   using.tips("1");
```

#### Comparison Operators

| Operator | Operation | Syntax | Returns |
|----------|-----------|--------|---------|
| `=` | Equality | `=(left, right)` | boolean |
| `<` | Less than | `<(left, right)` | boolean |
| `>` | Greater than | `>(left, right)` | boolean |
| `</=` | Less/equal | `</=(left, right)` | boolean |
| `>/=` | Greater/equal | `>/=(left, right)` | boolean |

**Examples:**
```plang
using.tips("Comparison operators");
vars.new(a, number, 10);
vars.new(b, number, 3);

vars.new(isEqual, boolean, =(vars.a, vars.b));     using.tips("no");
vars.new(isGreater, boolean, >(vars.a, vars.b));   using.tips("yes");
vars.new(isLess, boolean, <(vars.a, vars.b));      using.tips("no");
vars.new(isGE, boolean, >/=(vars.a, vars.b));      using.tips("yes");
```

#### Logical Operators

| Operator | Operation | Syntax | Returns |
|----------|-----------|--------|---------|
| `/` | OR | `/(left, right)` | boolean |
| `&` | AND | `&(left, right)` | boolean |
| `~` | NOT | `~(value)` | boolean |

**Examples:**
```plang
using.tips("Logical operators");
vars.new(a, boolean, yes);
vars.new(b, boolean, no);

vars.new(orResult, boolean, /(vars.a, vars.b));     using.tips("yes");
vars.new(andResult, boolean, &(vars.a, vars.b));    using.tips("no");
vars.new(notResult, boolean, ~(vars.a));            using.tips("no");
```

---

## Complete Examples

### Factorial Calculator

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
using.tips("Output: Factorial of 5 is 120");
```

### Fibonacci Sequence

```plang
using.tips("Fibonacci Sequence");
vars.new(a, number, 0);
vars.new(b, number, 1);
vars.new(i, number, 0);

loop.for.range(1, 10, vars.i).codes({
    vars.new(fib, number, +(vars.a, vars.b));
    ter.otpt(vars.fib);
    ter.otpt(" ");
    vars.a.modify(vars.b);
    vars.b.modify(vars.fib);
});
using.tips("Output: 1 2 3 5 8 13 21 34 55 89");
```

### Guess the Number Game

```plang
using.tips("Guess the Number Game");
vars.new(target, number, 7);
vars.new(guess, number, 0);
vars.new(tries, number, 0);

ter.otpt("Guess a number between 1 and 10!\n");

loop.while.when(yes).codes({
    vars.tries.modify(+(var, 1));
    ter.otpt("Your guess: ");
    ter.inpt(vars.guess);
    
    loop.if.when(=(vars.guess, vars.target)).codes({
        ter.otpt("Correct! You took ");
        ter.otpt(vars.tries);
        ter.otpt(" tries.\n");
        loop.stop();
    }).else({
        ter.otpt("Wrong! Try again.\n");
    });
});
```

### Temperature Converter

```plang
using.tips("Temperature Converter");
vars.new(celsius, dotNum, 0);
vars.new(fahrenheit, dotNum, 0);

ter.otpt("Enter temperature in Celsius: ");
ter.inpt(vars.celsius);

vars.fahrenheit.modify(+(*(`(vars.celsius, 5), 9), 32));

ter.otpt(vars.celsius);
ter.otpt("°C = ");
ter.otpt(vars.fahrenheit);
ter.otpt("°F\n");
```

---

## Error Messages

PLang compiler provides clear error messages with line and column numbers:

```
Line: 5~5, Column: 10~15: Variable 'x' hasn't been defined
Line: 3~3, Column: 5~5: Missing ';' after statement
```

Common errors:
- **Undefined variable** - Using a variable before declaring it
- **Type mismatch** - Assigning wrong type to a variable
- **Missing semicolon** - Forgetting `;` at end of statement
- **Unknown keyword** - Using an undefined keyword

---

## Tips & Best Practices

1. **Use comments**: Document your code with `using.tips()`
2. **Initialize variables**: Always give variables an initial value
3. **Use meaningful names**: `vars.new(age, number, 0)` is better than `vars.new(a, number, 0)`
4. **Check loop conditions**: Ensure loops will terminate
5. **Test incrementally**: Test small pieces before building larger programs
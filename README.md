# PLang & PLang compiler

NOTICE: This project is in development. Some of the code in this file is not final.

### PLang

#### **Basic usage**
`keyword.modifier().modifier()...;`
e.g. `vars.new(i, number, 0)`

#### **Keywords**

1.`using`

**modifiers**
- `use(fileName)`: use the source from `fileName` in your code.
  e.g. `using.use(student);`
- `tips(text)`: add a comment to the line.
  e.g. `using.tips("TODO: Here's something to do.");`
- `sub(oldCode, newCode)`: replace `oldCode` with `newCode`.
  e.g. `using.sub(dotNum, dn);`

2.`vars`

**modifiers**
- `new(name, type, value)`: create a new variable in the code.
    e.g. `vars.new(n, number, 0);`
- `[variable name]`: returns the variable value.
    e.g. `vars.n`

- modifiers
- - `modify(value)`: modify the variable to `value`. You can use `var` in this modifier to refer to the variable.
    e.g. `vars.n.modify(+(var, 1));`

3.`ter`

**modifiers**
- `otpt(text)`: print text in the terminal.
    e.g. `ter.otpt("Hello world!");`
- `inpt(variable)`: input a value and save it to the `variable`.
    e.g. `ter.inpt(vars.n);`

4.`loop`

**modifiers**
- `while`: when the condition is true, run the code in `codes`. Use `when` to write the condition.
    e.g. 
  ```PLang
  loop.while.when(</=(vars.n, vars.k)).codes({
      ter.otpt(vars.n);
      vars.n.modify(+(var, 1));
  });
  ```
- `for`: run the code while the variable is in the specified range. use `.range(from: number, to: number, in: variable)` to write a range.
    e.g.
  ```PLang
  vars.new(i, number, 0);
  loop.for.range(from: 1, to: 5, in: vars.i).codes({
      ter.otpt(vars.i);
  });
  ```

- `stop()`: terminate the loop.
    e.g.
    ```PLang
    loop.while.when(yes).codes({
        ter.otpt("This while only run for once.");
        loop.stop();
    });
    ```

- `skip()`: skips the current iteration and proceeds to the next one.
    e.g.
    ```PLang
    loop.while.when(yes).codes({
        ter.otpt("This code will run.");
        loop.skip();
        ter.otpt("This code will be skipped.");
    });
    ```

5.`operators`

`operators.<(left, right)` and `<(left, right)` are both available. (Just like using using.sub(operators., ) to omit the prefix.)

**modifiers**
1. `+`
    - `+(number, number)` returns `number` (also can use `dotNum`)
2. `-`
    - `-(number, number)` returns `number` (also can use `dotNum`)
3. `*`
    - `*(number, number)` returns `number` (also can use `dotNum`)
4. `` ` `` : division
    - `` `(number, number)`` returns `dotNum`
5. `%`
    - `%(number, number)` returns `number`
6. `/`: or
    - `/(boolean, boolean)` returns `boolean`
7. `&`: and
    - `&(boolean, boolean)` returns `boolean`
8. `=`: equal
    - `=(number, number)` returns `boolean`
9. `~`: opposite
    - `~(boolean)` returns `boolean`
10. `<`: less than
    - `<(number, number)` returns  `boolean` (also can use `dotNum`)
11. `>`: greater than
    - `>(number, number)` returns  `boolean` (also can use `dotNum`)
12. `</=`: less than or equal
    - `</=(number, number)` returns  `boolean` (also can use `dotNum`)
13. `>/=`: greater than or equal
    - `>/=(number, number)` returns  `boolean` (also can use `dotNum`)

#### **Types**
1. `number`: a number.
2. `dotNum`: a decimal number (float/double).
3. `text`: a text (string).
4. `boolean`: a bool value. it has 2 values: `yes` and `no`.

---
### PLang compiler

##### Dependencies

1. `gcc`: We need it to compile c code.
2. `python`: Compiler write by python.
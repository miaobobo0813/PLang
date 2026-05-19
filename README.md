# PLang & PLang compiler

NOTICE: This project is in development. Some of the code in this file is not final.

### PLang

- **Basic usage**
`keyword.modifier().modifier()...;`
e.g. `vars.new(i, number, 0)`

- **Keywords**

1. `using`

**modifiers**
- `use(fileName)`: using `fileName` source in your code.
  e.g. `using.use(student);`
- `tips(text)`: add a comment in the line.
  e.g. `using.tips("TODO: Here's something to do.");`
- `sub(oldCode, newCode)`: replace `oldCode` with `newCode`.
  e.g. `using.sub(dotNum, dn);`

2. `vars`

**modifiers**
- `new(name, type, value)`: create a new variable in the code.
  e.g. `vars.new(n, number, 0);`
- `[variable name]`: return the variable value.
  e.g. `vars.n`

**modifiers**
- `modify(value)`: modify the variable to `value`. you can use `var` in this modifier to refer to the variable.
  e.g. `vars.n.modify(+(var, 1));`

3. `ter`

**modifiers**
- `otpt(text)`: print text in the terminal.
  e.g. `ter.otpt("Hello world!");`
- `inpt(variable)`: input value and save in the `variable`.
  e.g. `ter.inpt(vars.n);`

4. `loop`

**modifiers**
- `while`: when the condition is true, run the code in `codes`. Use `when` to write the condition.
  e.g. 
  ```PLang
  loop.while.when(</=(vars.n, vars.k)).codes({
      ter.otpt(vars.n);
      vars.n.modify(+(var, 1));
  });
  ```
- `for`: when the variable in range, run the code. use `.range(from: number, to: number, in: variable)` to write a range.
  e.g.
  ```PLang
  vars.new(i, number, 0);
  loop.for.range(from: 1, to: 5, in: vars.i).codes({
      ter.otpt(vars.i);
  });
  ```

5. `operators`

`operators.<(left, right)` and `<(left, right)` all available. (Just like used `using.sub(operators., )` before.)

**modifiers**
1. `+`
2. `-`
3. `*`
4. `\`` : division
5. `%`
6. `/`: or
7. `&`: and
8. `=`: equal
9. `~`: opposite

- **Types**
1. `number`: a number.
2. `dotNum`: a dot number (float/double).
3. `text`: a text (string).
4. `boolean`: a bool value. it has `yes` and `no` 2 values.
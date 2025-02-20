# MayhemMonkey

MayhemMonkey is a testing tool designed to simulate how your program might react to unexpected errors that can occur when executing basic built-in functions in Python. It helps ensure that your code is robust enough to handle a variety of errors gracefully.

## Goal

The main goal of MayhemMonkey is to simulate errors in basic built-in functions to test how your program responds to unexpected failures. With mayhemmonkey, you can introduce different types of errors in critical Python functions like `open`, `print`, `eval`, etc., and ensure your application remains stable under these conditions.

## Installation

Install MayhemMonkey easily using pip:

```bash
pip3 install mayhemmonkey
```

## Usage

Here is a simple example of how to use MayhemMonkey in a Python project:

```
from mayhemmonkey import MayhemMonkey

mayhemmonkey = MayhemMonkey()

print(mayhemmonkey.get_function_categories())
print(mayhemmonkey.get_function_categories_as_list())

mayhemmonkey.set_function_error_rate("open", 0.5)
mayhemmonkey.set_function_group_error_rate("io", 0.3)
mayhemmonkey.set_global_error_rate(0.2)

with open("test.txt", "w") as f:  # 50% Chance that it'll fail
    f.write("Hello world!")

print("This should be printed.")  # 30% it'll fail because it's in the group "io"
```

### Error Configuration

MayhemMonkey allows you to configure the error probability for various functions, function groups, or globally. The error probability is given as a decimal number between `0` and `1`, where `0` means no errors and `1` guarantees an error.

#### Configuring Error Probabilities

| Function/Group         | Description                                                                  | Error Probability | Example                                   |
|------------------------|------------------------------------------------------------------------------|-------------------|-------------------------------------------|
| **Individual Functions**| Set error probability for a specific function.                               | Float 0 to 1            | `mayhemmonkey.set_function_error_rate("open", 0.5)` |
| **Function Groups**     | Set error probability for a group of functions.                              | Float 0 to 1            | `mayhemmonkey.set_function_group_error_rate("io", 0.3)` |
| **Global**              | Set global error probability for all functions.                              | Float 0 to 1            | `mayhemmonkey.set_global_error_rate(0.2)`  |

#### Function Groups and Their Functions

| Category | Functions |
| --- | --- |
| attributes | `delattr`, `getattr`, `hasattr`, `property`, `setattr` |
| collections | `dict`, `frozenset`, `list`, `set`, `tuple` |
| conversion | `ascii`, `bin`, `bool`, `bytearray`, `bytes`, `chr`, `complex`, `float`, `format`, `hex`, `int`, `oct`, `ord`, `repr`, `str` |
| evaluation | `compile`, `eval`, `exec` |
| exceptions | `compile`, `eval`, `exec` |
| functional | `breakpoint`, `classmethod`, `staticmethod`, `super` |
| hashing | `hash` |
| io | `input`, `open`, `print` |
| iteration | `all`, `any`, `enumerate`, `filter`, `iter`, `len`, `map`, `next`, `range`, `reversed`, `sorted`, `zip` |
| math | `abs`, `divmod`, `max`, `min`, `pow`, `round`, `sum` |
| reflection | `__import__`, `callable`, `globals`, `id`, `isinstance`, `issubclass`, `locals`, `type`, `vars` |
| slicing | `slice` |

#### Error Types for Functions

MayhemMonkey can generate specific types of errors for each function. Here’s a list of the possible errors and their meanings:

| Function | Error Type         | Description                                      |
|----------|--------------------|--------------------------------------------------|
| `open`   | `FileNotFoundError` | File not found                                  |
|          | `PermissionError`   | No permission for the file                      |
|          | `OSError`           | Too many open files                             |
| `input`  | `EOFError`          | End of file reached                             |
|          | `KeyboardInterrupt` | Input was interrupted                           |
| `print`  | `OSError`           | Error during printing                           |
| `eval`   | `SyntaxError`       | Invalid syntax                                  |
|          | `TypeError`         | Invalid expression                              |
|          | `RuntimeError`      | Unexpected runtime error                        |
| `exec`   | `SyntaxError`       | Invalid syntax                                  |
|          | `RuntimeError`      | Unexpected runtime error                        |
| `compile`| `SyntaxError`       | Error during compilation                        |
| `max`    | `ValueError`        | Empty sequence                                  |
|          | `TypeError`         | Incompatible types for comparison               |
| `min`    | `ValueError`        | Empty sequence                                  |
|          | `TypeError`         | Incompatible types for comparison               |
| `divmod` | `ZeroDivisionError` | Division by zero                                |
|          | `TypeError`         | Invalid operand                                 |
| `pow`    | `ZeroDivisionError` | 0.0 cannot be raised to a negative exponent     |
|          | `TypeError`         | Invalid operand                                 |
| `round`  | `TypeError`         | Second argument must be an integer              |

## Frequently Asked Questions
How can I use MayhemMonkey in my application?

MayhemMonkey is easy to use to simulate errors in basic Python functions. You can install mayhemmonkey in your project and then configure error probabilities for specific functions, function groups, or globally. This helps ensure that your application is robust enough to handle different error conditions.

## What happens if an error occurs?

When an error occurs due to the configured error probability, an exception will be raised that you can handle with a try-except block. You can ensure that your application is prepared for these errors by adding appropriate error handling.

## Contributing

If you want to contribute to the development of MayhemMonkey, you can open a pull request or file an issue on GitHub.

# Caveats

Load this as last module, as currently, all imports will fail when this module is loaded.

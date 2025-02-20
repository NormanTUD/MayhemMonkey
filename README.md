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

mayhemmonkey.set_function_error_rate("open", 0.5)
mayhemmonkey.set_function_group_error_rate("io", 0.3)

mayhemmonkey.install_faulty()

with open("test.txt", "w") as f:  # 50% Chance that it'll fail
    f.write("Hello world!")

print("This should be printed.")  # 30% it'll fail because it's in the group "io"
```

You can also set specific functions to fail after a certain amount of calls:

```
from mayhemmonkey import MayhemMonkey

mayhemmonkey = MayhemMonkey()

mayhemmonkey.set_function_fail_after_count("print", 3)

mayhemmonkey.install_faulty()

print("This should be printed.")
print("This should be printed.")
try:
    print("This shouldn't be printed.")
except Exception as e:
    print(f"Error: {e}")

print("This should be printed.")
```

Here, the 3rd print fails with some random error that print can give in real life.

### Error Configuration

MayhemMonkey allows you to configure the error probability for various functions, function groups, or globally. The error probability is given as a decimal number between `0` and `1`, where `0` means no errors and `1` guarantees an error.

#### Methods of the MayhemMonkey-object

| Function                          | Description                                                                                                   | Parameters                                                                                 |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| `get_function_categories`         | Returns a dictionary of all function categories and their respective functions.                               | No parameters.                                                                             |
| `get_function_categories_as_list` | Returns a list of tuples where each tuple contains the category name and its associated functions.            | No parameters.                                                                             |
| `install_faulty`                  | Patches built-in functions to introduce errors. Can only be called once.                                      | No parameters.                                                                             |
| `set_function_error_rate`         | Sets the error probability for an individual function.                                                        | `name` (str): The function name.<br>`rate` (float): The error rate between 0 and 1.        |
| `set_function_group_error_rate`   | Sets the error probability for a group of functions.                                                          | `group` (str): The function group.<br>`rate` (float): The error rate between 0 and 1.      |
| `is_valid_exception_tuple_list`   | Checks if the provided object is a valid list of tuples with exception types and messages.                    | `obj` (list): A list of tuples of the form (ExceptionType, String).                        |
| `add_exception_to_function`       | Adds a list of exceptions (tuples) to a function to simulate specific errors.                                 | `name` (str): The function name.<br>`list_of_tuples_of_exceptions` (list): List of tuples (ExceptionType, String). |
| `set_function_fail_after_count`   | Sets the count after which a function will start failing with errors.                                         | `name` (str): The function name.<br>`cnt` (int): The count after which it will fail.       |
| `generate_function_categories_markdown_table` | Generates a markdown table for function categories and their functions.                                      | No parameters.                                                                             |
| `generate_function_errors_markdown_table`      | Generates a markdown table for functions and their associated errors.                                         | No parameters.                                                                             |


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

| Function | Errors |
| --- | --- |
| `__import__` | `ImportError: Module not found`<br>`TypeError: Invalid module name` |
| `abs` | `TypeError: Bad operand type for abs()` |
| `all` | `TypeError: Argument must be iterable` |
| `any` | `TypeError: Argument must be iterable` |
| `ascii` | `None` |
| `bin` | `TypeError: Object cannot be interpreted as an integer` |
| `bool` | `None` |
| `breakpoint` | `RuntimeError: Cannot start debugger` |
| `bytearray` | `TypeError: Invalid argument type`<br>`ValueError: Negative size not allowed` |
| `bytes` | `TypeError: Invalid argument type`<br>`ValueError: Negative size not allowed` |
| `callable` | `None` |
| `chr` | `ValueError: Argument out of range`<br>`TypeError: Integer argument required` |
| `classmethod` | `TypeError: Invalid method reference` |
| `compile` | `SyntaxError: Compilation error`<br>`TypeError: Invalid code object` |
| `complex` | `ValueError: Could not convert string to complex`<br>`TypeError: Invalid type for complex()` |
| `delattr` | `AttributeError: Object has no such attribute`<br>`TypeError: Invalid attribute name` |
| `dict` | `TypeError: Invalid dictionary construction` |
| `dir` | `TypeError: Invalid argument type` |
| `divmod` | `ZeroDivisionError: division by zero`<br>`TypeError: Unsupported operand type` |
| `enumerate` | `TypeError: Object is not iterable` |
| `eval` | `SyntaxError: Invalid syntax`<br>`TypeError: Expression not allowed`<br>`RuntimeError: Unexpected runtime error` |
| `exec` | `SyntaxError: Invalid syntax`<br>`RuntimeError: Unexpected runtime error` |
| `filter` | `TypeError: Function must be callable` |
| `float` | `ValueError: Could not convert string to float`<br>`TypeError: Invalid type for float()` |
| `format` | `ValueError: Invalid format string` |
| `frozenset` | `TypeError: Invalid argument type` |
| `getattr` | `AttributeError: Object has no such attribute`<br>`TypeError: Invalid attribute name` |
| `globals` | `None` |
| `hasattr` | `None` |
| `hash` | `TypeError: Unhashable type` |
| `hex` | `TypeError: Object cannot be interpreted as an integer` |
| `id` | `None` |
| `input` | `EOFError: End of file reached`<br>`KeyboardInterrupt: Input interrupted` |
| `int` | `ValueError: Invalid literal for int()`<br>`TypeError: Invalid type for int()` |
| `isinstance` | `TypeError: Second argument must be a type or tuple of types` |
| `issubclass` | `TypeError: Second argument must be a type or tuple of types` |
| `iter` | `TypeError: Object is not iterable` |
| `len` | `TypeError: Object has no len()` |
| `list` | `TypeError: Invalid argument for list()` |
| `locals` | `None` |
| `map` | `TypeError: Function must be callable` |
| `max` | `ValueError: Empty sequence`<br>`TypeError: Cannot compare different types` |
| `memoryview` | `TypeError: Invalid memory buffer` |
| `min` | `ValueError: Empty sequence`<br>`TypeError: Cannot compare different types` |
| `next` | `StopIteration: Iterator exhausted`<br>`TypeError: Object is not an iterator` |
| `object` | `None` |
| `oct` | `TypeError: Object cannot be interpreted as an integer` |
| `open` | `FileNotFoundError: No such file or directory`<br>`PermissionError: Permission denied`<br>`IsADirectoryError: Is a directory`<br>`OSError: Too many open files` |
| `ord` | `TypeError: Argument must be a character`<br>`ValueError: Character out of range` |
| `pow` | `ZeroDivisionError: 0.0 cannot be raised to a negative power`<br>`TypeError: Unsupported operand type` |
| `print` | `OSError: Output error` |
| `property` | `None` |
| `range` | `TypeError: Invalid argument type`<br>`ValueError: Step argument must not be zero` |
| `repr` | `None` |
| `reversed` | `TypeError: Object is not reversible` |
| `round` | `TypeError: Second argument must be an integer` |
| `set` | `TypeError: Invalid argument for set()` |
| `setattr` | `AttributeError: Cannot set attribute`<br>`TypeError: Invalid attribute name` |
| `slice` | `TypeError: Invalid slice indices` |
| `sorted` | `TypeError: Invalid key function` |
| `staticmethod` | `None` |
| `str` | `TypeError: Invalid type for str()` |
| `sum` | `TypeError: Object in iterable is not summable` |
| `super` | `TypeError: Invalid superclass reference` |
| `tuple` | `TypeError: Invalid argument for tuple()` |
| `type` | `TypeError: Invalid arguments for type()` |
| `vars` | `TypeError: Object must have __dict__ attribute` |
| `zip` | `None` |

## What happens if an error occurs?

When an error occurs due to the configured error probability, an exception will be raised that you can handle with a try-except block. You can ensure that your application is prepared for these errors by adding appropriate error handling.

## Contributing

If you want to contribute to the development of MayhemMonkey, you can open a pull request or file an issue on GitHub.

# Caveats

Load this as last module, as currently, all imports will fail when this module is loaded.

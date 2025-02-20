import builtins
import random
import functools
import types

class MayhemMonkey:
    FUNCTION_CATEGORIES = {
        "io": {
            "open", "input", "print"
        },
        "math": {
            "abs", "divmod", "max", "min", "pow", "round", 
            "sum"
        },
        "evaluation": {
            "eval", "exec", "compile"
        },
        "conversion": {
            "ascii", "bin", "bool", "bytearray", "bytes", 
            "chr", "complex", "float", "format", "hex", 
            "int", "oct", "ord", "repr", "str"
        },
        "collections": {
            "dict", "frozenset", "list", "set", "tuple"
        },
        "iteration": {
            "all", "any", "enumerate", "filter", "iter", 
            "len", "map", "next", "range", "reversed", 
            "sorted", "zip"
        },
        "attributes": {
            "delattr", "getattr", "hasattr", "setattr", 
            "property"
        },
        "reflection": {
            "callable", "globals", "id", "isinstance", 
            "issubclass", "locals", "type", "vars", 
            "__import__"
        },
        "functional": {
            "breakpoint", "classmethod", "staticmethod", 
            "super"
        },
        "hashing": {
            "hash"
        },
        "slicing": {
            "slice"
        },
        "exceptions": {
            "compile", "eval", "exec"
        }
    }


    DEFAULT_INDIVIDUAL_ERROR_RATES = {}
    DEFAULT_GROUP_ERROR_RATES = {}

    FUNCTION_ERRORS = {
        "abs": [(TypeError, "Bad operand type for abs()")],
        "all": [(TypeError, "Argument must be iterable")],
        "any": [(TypeError, "Argument must be iterable")],
        "ascii": [],
        "bin": [(TypeError, "Object cannot be interpreted as an integer")],
        "bool": [],
        "breakpoint": [(RuntimeError, "Cannot start debugger")],
        "bytearray": [(TypeError, "Invalid argument type"),
                      (ValueError, "Negative size not allowed")],
        "bytes": [(TypeError, "Invalid argument type"),
                  (ValueError, "Negative size not allowed")],
        "callable": [],
        "chr": [(ValueError, "Argument out of range"),
                (TypeError, "Integer argument required")],
        "classmethod": [(TypeError, "Invalid method reference")],
        "compile": [(SyntaxError, "Compilation error"),
                    (TypeError, "Invalid code object")],
        "complex": [(ValueError, "Could not convert string to complex"),
                    (TypeError, "Invalid type for complex()")],
        "delattr": [(AttributeError, "Object has no such attribute"),
                    (TypeError, "Invalid attribute name")],
        "dict": [(TypeError, "Invalid dictionary construction")],
        "dir": [(TypeError, "Invalid argument type")],
        "divmod": [(ZeroDivisionError, "division by zero"),
                   (TypeError, "Unsupported operand type")],
        "enumerate": [(TypeError, "Object is not iterable")],
        "eval": [(SyntaxError, "Invalid syntax"),
                 (TypeError, "Expression not allowed"),
                 (RuntimeError, "Unexpected runtime error")],
        "exec": [(SyntaxError, "Invalid syntax"),
                 (RuntimeError, "Unexpected runtime error")],
        "filter": [(TypeError, "Function must be callable")],
        "float": [(ValueError, "Could not convert string to float"),
                  (TypeError, "Invalid type for float()")],
        "format": [(ValueError, "Invalid format string")],
        "frozenset": [(TypeError, "Invalid argument type")],
        "getattr": [(AttributeError, "Object has no such attribute"),
                    (TypeError, "Invalid attribute name")],
        "globals": [],
        "hasattr": [],
        "hash": [(TypeError, "Unhashable type")],
        "hex": [(TypeError, "Object cannot be interpreted as an integer")],
        "id": [],
        "input": [(EOFError, "End of file reached"),
                  (KeyboardInterrupt, "Input interrupted")],
        "int": [(ValueError, "Invalid literal for int()"),
                (TypeError, "Invalid type for int()")],
        "isinstance": [(TypeError, "Second argument must be a type or tuple of types")],
        "issubclass": [(TypeError, "Second argument must be a type or tuple of types")],
        "iter": [(TypeError, "Object is not iterable")],
        "len": [(TypeError, "Object has no len()")],
        "list": [(TypeError, "Invalid argument for list()")],
        "locals": [],
        "map": [(TypeError, "Function must be callable")],
        "max": [(ValueError, "Empty sequence"),
                (TypeError, "Cannot compare different types")],
        "memoryview": [(TypeError, "Invalid memory buffer")],
        "min": [(ValueError, "Empty sequence"),
                (TypeError, "Cannot compare different types")],
        "next": [(StopIteration, "Iterator exhausted"),
                 (TypeError, "Object is not an iterator")],
        "object": [],
        "oct": [(TypeError, "Object cannot be interpreted as an integer")],
        "open": [(FileNotFoundError, "No such file or directory"),
                 (PermissionError, "Permission denied"),
                 (IsADirectoryError, "Is a directory"),
                 (OSError, "Too many open files")],
        "ord": [(TypeError, "Argument must be a character"),
                (ValueError, "Character out of range")],
        "pow": [(ZeroDivisionError, "0.0 cannot be raised to a negative power"),
                (TypeError, "Unsupported operand type")],
        "print": [(OSError, "Output error")],
        "property": [],
        "range": [(TypeError, "Invalid argument type"),
                  (ValueError, "Step argument must not be zero")],
        "repr": [],
        "reversed": [(TypeError, "Object is not reversible")],
        "round": [(TypeError, "Second argument must be an integer")],
        "set": [(TypeError, "Invalid argument for set()")],
        "setattr": [(AttributeError, "Cannot set attribute"),
                    (TypeError, "Invalid attribute name")],
        "slice": [(TypeError, "Invalid slice indices")],
        "sorted": [(TypeError, "Invalid key function")],
        "staticmethod": [],
        "str": [(TypeError, "Invalid type for str()")],
        "sum": [(TypeError, "Object in iterable is not summable")],
        "super": [(TypeError, "Invalid superclass reference")],
        "tuple": [(TypeError, "Invalid argument for tuple()")],
        "type": [(TypeError, "Invalid arguments for type()")],
        "vars": [(TypeError, "Object must have __dict__ attribute")],
        "zip": [],
        "__import__": [(ImportError, "Module not found"),
                       (TypeError, "Invalid module name")]
    }

    FUNCTION_CALL_COUNTER = {}

    FAIL_AT_COUNT = {}

    INSTALLED_FAULTY = False

    def __init__(self):
        self.individual_error_rates = self.DEFAULT_INDIVIDUAL_ERROR_RATES.copy()
        self.group_error_rates = self.DEFAULT_GROUP_ERROR_RATES.copy()
        self.function_list = [func for funcs in self.FUNCTION_CATEGORIES.values() for func in funcs]

        self.originals = {
            name: getattr(builtins, name)
            for name in dir(builtins)
            if callable(getattr(builtins, name))
            and isinstance(getattr(builtins, name), (types.BuiltinFunctionType, types.FunctionType))
            and name in self.function_list
        }

    def is_builtin_function(self, func_name):
        """ Check if a function is a builtin """
        return hasattr(builtins, func_name) and callable(getattr(builtins, func_name))

    def install_faulty(self):
        if self.INSTALLED_FAULTY:
            raise Exception("Can only call install_faulty once.")

        self._patch_functions()
        self.INSTALLED_FAULTY = True

    def get_function_categories(self):
        """Returns a dictionary with all FUNCTION_CATEGORIES and their functions."""
        return list({category: list(functions) for category, functions in self.FUNCTION_CATEGORIES.items()}.keys())

    def get_function_categories_as_list(self):
        """Returns a list of tuples, where each tuple contains (category, [functions])."""
        return [(category, list(functions)) for category, functions in self.FUNCTION_CATEGORIES.items()]

    def _patch_functions(self):
        """Overrides built-in functions with faulty versions."""
        for name, func in self.originals.items():
            setattr(builtins, name, self._faulty_wrapper(func, name))

    def _faulty_wrapper(self, func, name):
        """Creates a faulty version of a function."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.FUNCTION_CALL_COUNTER[name] = self.FUNCTION_CALL_COUNTER.get(name, 0) + 1

            error_rate = self.get_error_rate(name)

            try_to_fail = False

            if name in self.FAIL_AT_COUNT and name in self.FUNCTION_CALL_COUNTER and self.FAIL_AT_COUNT[name] == self.FUNCTION_CALL_COUNTER[name]:
                try_to_fail = True

            elif random.random() < error_rate:
                try_to_fail = True

            if try_to_fail:
                errors = self.FUNCTION_ERRORS.get(name, [(RuntimeError, "Unexpected runtime error")])

                if errors:
                    len_errors = 0
                    for _ in errors:
                        len_errors = len_errors + 1
                    max_index = len_errors - 1
                    index = random.randint(0, max_index)
                    err_type, err_msg = errors[index]

                    print(err_msg)

                    raise err_type(f"{err_msg}")
            return func(*args, **kwargs)
        return wrapper

    def set_function_error_rate(self, name, rate):
        """Sets the error probability for an individual function."""
        if name not in self.originals:
            raise ValueError(f"Unknown function: {name}")
        if not (0 <= rate <= 1):
            raise ValueError("Error probability must be between 0 and 1")
        self.individual_error_rates[name] = rate

    def set_function_group_error_rate(self, group, rate):
        """Sets the error probability for a function group."""
        if group not in self.FUNCTION_CATEGORIES:
            raise ValueError(f"Unknown function group: {group}")
        if not (0 <= rate <= 1):
            raise ValueError("Error probability must be between 0 and 1")
        self.group_error_rates[group] = rate

    def is_valid_exception_tuple_list(self, obj):
        """
        Checks if the given object is a list of tuples of the form (ExceptionType, String).
        Raises a TypeError if the object is not valid.
        """
        if not isinstance(obj, list):
            raise TypeError(f"Expected a list, but got {type(obj).__name__}")

        for i, item in enumerate(obj):
            if not isinstance(item, tuple) or len(item) != 2:
                raise TypeError(f"Item {i} is not a tuple of length 2: {item}")

            exc_type, msg = item

            if not (isinstance(exc_type, type) and issubclass(exc_type, BaseException)):
                raise TypeError(f"Item {i} first element is not an Exception type: {exc_type}")

            if not isinstance(msg, str):
                raise TypeError(f"Item {i} second element is not a string: {msg}")

        return True

    def add_exception_to_function(self, name, list_of_tuples_of_exceptions):
        if isinstance(name, str):
            if self.is_builtin_function(name):
                if self.is_valid_exception_tuple_list(list_of_tuples_of_exceptions):
                    if name in self.FUNCTION_ERRORS:
                        print(f"Warning: {name} already exists in self.FUNCTION_ERRORS. Old value will be overwritten.")

                    self.FUNCTION_ERRORS[name] = list_of_tuples_of_exceptions
                else:
                    raise ValueError(f"2nd parameter list_of_tuples_of_exceptions must be a list of tuples")
            else:
                raise ValueError(f"{name} is not a builtin function")
        else:
            raise ValueError(f"1st parameter name must be a string, is {type(name)}")

    def set_function_fail_after_count(self, name, cnt):
        if isinstance(name, str):
            if self.is_builtin_function(name):
                if isinstance(cnt, int):
                    if name in self.FUNCTION_ERRORS:
                        self.FAIL_AT_COUNT[name] = cnt
                    else:
                        raise ValueError(f"Function has no known exceptions. Call 'mayhemmonkey.add_exception_to_function(\"{name}\", [(OSError, 'Output Error')])' with a list of tuples of exceptions and their corresponding names BEFORE calling set_function_fail_after_count.")
                else:
                    raise ValueError(f"2nd parameter cnt must be a string, is {type(cnt)}")
            else:
                raise ValueError(f"{name} is not a builtin function")
        else:
            raise ValueError(f"1st parameter name must be a string, is {type(name)}")

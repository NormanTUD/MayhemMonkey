# TODO:
# Alle fkts die ersetzt werden sollen als Param übergeben
# Param welche Error gemacht werden
# Nicht beim laden ersetzen sondern per install_faulty
# Nicht nur wahrscheinlichkeit sondern auch Counter erlauben bis zur Failure, auch Modulo Counter

import builtins
import random
import functools
import types

class MayhemMonkey:
    FUNCTION_CATEGORIES = {
        "io": {"open", "input", "print"},
        "math": {"divmod", "max", "min", "pow", "round"},
        "evaluation": {"eval", "exec", "compile"}
    }

    DEFAULT_GLOBAL_ERROR_RATE = 0
    DEFAULT_INDIVIDUAL_ERROR_RATES = {}
    DEFAULT_GROUP_ERROR_RATES = {}

    FUNCTION_ERRORS = {
        "open": [(FileNotFoundError, "No such file or directory"),
                 (PermissionError, "Permission denied"),
                 (IsADirectoryError, "Is a directory"),
                 (OSError, "Too many open files")],
        "input": [(EOFError, "End of file reached"),
                  (KeyboardInterrupt, "Input interrupted")],
        "print": [(OSError, "Output error")],
        "eval": [(SyntaxError, "Invalid syntax"),
                 (TypeError, "Expression not allowed"),
                 (RuntimeError, "Unexpected runtime error")],
        "exec": [(SyntaxError, "Invalid syntax"),
                 (RuntimeError, "Unexpected runtime error")],
        "compile": [(SyntaxError, "Compilation error")],
        "hash": [(TypeError, "Unhashable type")],
        "max": [(ValueError, "Empty sequence"),
                (TypeError, "Cannot compare different types")],
        "min": [(ValueError, "Empty sequence"),
                (TypeError, "Cannot compare different types")],
        "divmod": [(ZeroDivisionError, "division by zero"),
                   (TypeError, "Unsupported operand type")],
        "pow": [(ZeroDivisionError, "0.0 cannot be raised to a negative power"),
                (TypeError, "Unsupported operand type")],
        "round": [(TypeError, "Second argument must be an integer")],
    }

    FUNCTION_CALL_COUNTER = {}

    FAIL_AT_COUNT = {}

    def __init__(self):
        self.global_error_rate = self.DEFAULT_GLOBAL_ERROR_RATE
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

        self._patch_functions()

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

                    raise err_type(f"{err_msg}")
            return func(*args, **kwargs)
        return wrapper

    def get_error_rate(self, name):
        """Determines the error probability for a function."""
        if name in self.individual_error_rates:
            return self.individual_error_rates[name]
        for category, functions in self.FUNCTION_CATEGORIES.items():
            if name in functions:
                return self.group_error_rates.get(category, self.global_error_rate)
        return self.global_error_rate

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

    def set_global_error_rate(self, rate):
        """Sets the global error probability."""
        if not (0 <= rate <= 1):
            raise ValueError("Error probability must be between 0 and 1")
        self.global_error_rate = rate

    def set_function_fail_after_count(self, name, cnt):
        if isinstance(name, str):
            if isinstance(cnt, int):
                self.FAIL_AT_COUNT[name] = cnt
            else:
                raise ValueError(f"2nd parameter cnt must be a string, is {type(cnt)}")
        else:
            raise ValueError(f"1st parameter name must be a string, is {type(name)}")

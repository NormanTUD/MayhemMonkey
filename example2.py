from mayhemmonkey import MayhemMonkey

mayhemmonkey = MayhemMonkey()

mayhemmonkey.set_function_fail_after_count("print", 3)

mayhemmonkey.add_exception_to_function("print_ASDF", [(OSError, 'Output Error')])

mayhemmonkey.set_function_fail_after_count("print_ASDF", 3)

mayhemmonkey.install_faulty()

print("This should be printed.")
print("This should be printed.")
try:
    print("This shouldn't be printed.")
except Exception as e:
    print(f"Error: {e}")

print("This should be printed.")

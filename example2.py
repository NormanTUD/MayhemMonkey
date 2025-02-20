from mayhemmonkey import MayhemMonkey

mayhemmonkey = MayhemMonkey()

mayhemmonkey.set_function_fail_after_count("print", 3)

mayhemmonkey.install_faulty()
mayhemmonkey.install_faulty()

print("This should be printed.")
print("This should be printed.")
print("This should be printed.")

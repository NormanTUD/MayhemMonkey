from mayhemmonkey import MayhemMonkey

mayhemmonkey = MayhemMonkey()

mayhemmonkey.set_function_fail_after_count("print", 3)

with open("test.txt", "w") as f:
    f.write("Hello world!")

print("This should be printed.")
print("This should be printed.")
print("This should be printed.")

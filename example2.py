from mayhemmonkey import MayhemMonkey

mayhemmonkey = MayhemMonkey()

mayhemmonkey.set_function_fail_after_count("print", 3)

mayhemmonkey.install_faulty()

with open("test.txt", "w") as f:
    f.write("Hello world!")

print("This should be printed.")
print("This should be printed.")
print("This should be printed.")

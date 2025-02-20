from mayhemmonkey import MayhemMonkey

mayhemmonkey = MayhemMonkey()

mayhemmonkey.set_function_error_rate("open", 0.5)
mayhemmonkey.set_function_group_error_rate("io", 0.3)
mayhemmonkey.set_function_group_error_rate(["math", "conversion"], 0.8)

mayhemmonkey.install_faulty()

with open("test.txt", "w") as f:  # 50% Chance that it'll fail
    f.write("Hello world!")

print("This should be printed.")  # 30% it'll fail because it's in the group "io"

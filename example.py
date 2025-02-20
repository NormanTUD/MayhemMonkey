from mayhemmonkey import MayhemMonkey

mayhemmonkey = MayhemMonkey()

print(mayhemmonkey.get_function_categories())
print(mayhemmonkey.get_function_categories_as_list())

mayhemmonkey.set_function_error_rate("open", 0.5)
mayhemmonkey.set_function_group_error_rate("io", 0.3)

mayhemmonkey.install_faulty()

#print(mayhemmonkey.generate_function_categories_markdown_table())
print(mayhemmonkey.generate_function_errors_markdown_table())

with open("test.txt", "w") as f:  # 50% Chance that it'll fail
    f.write("Hello world!")

print("This should be printed.")  # 30% it'll fail because it's in the group "io"

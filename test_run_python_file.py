from functions.run_python_file import run_python_file

str_1 = run_python_file("calculator", "main.py")
str_2 = run_python_file("calculator", "main.py", ["3 + 5"])
str_3 = run_python_file("calculator", "tests.py")
str_4 = run_python_file("calculator", "../main.py")
str_5 = run_python_file("calculator", "nonexistent.py")
str_6 = run_python_file("calculator", "lorem.txt")

print(f'{str_1}\n{str_2}\n{str_3}\n{str_4}\n{str_5}\n{str_6}')
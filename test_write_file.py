from functions.write_file import write_file

x = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
y = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
c = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")

print(f'{x}\n{y}\n{c}')
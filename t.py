import os
path = "/www/index.html"

if path[0] == "/":
    path = path[1:]

print(path)

if os.path.isfile(path):
    with open(path, 'rb') as file:
        print("ehre")
else:
    print('not')
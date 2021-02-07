def decode(filename):
    f = open(filename)
    d = {}
    name = ""
    message = ''
    isname = True
    for char in f.read():
        print(char)
        if isname:
            if char == ' ':
                isname = False
            else:
                name = name + char
        else:
            if char == '~':
                d[name] = message
                name = ""
                message = ''
                isname = True
            else:
                message = message + char
    d[name] = message
    return d

def add(name, message, filename):
    f = open(filename, "a")
    f.write(name+" "+message+'~')

def delete(filename):
    f = open(filename, "w")
    f.write("")
        
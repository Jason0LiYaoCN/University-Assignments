from stack import Stack

def base_converter(input,base):
    digits = "0123456789ABCDEF"
    remem = Stack()
    while input > 0:
        top = input % base
        remem.push(top)
        input = input // base
    outputstring = ""
    while not remem.is_empty():
        outputstring = outputstring + digits[remem.pop()]
    return outputstring

print(base_converter(16,2))
print(base_converter(32,26))
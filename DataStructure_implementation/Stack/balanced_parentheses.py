from stack import Stack # As previously defined
# Completed extended for "{,[,(,),],}"

def par_check(symbol_string):
    s = Stack()
    balanced = True
    index = 0
    while index < len(symbol_string) and balanced:
        symbol = symbol_string[index]
        if symbol in "{[(":
            s.push(symbol)
        else:
            if s.is_empty():
                balanced = False
            else:
                top = s.pop()
                if not matched(top,symbol):
                    balanced = False
        index = index + 1
    
    if balanced and s.is_empty():
        return True
    else:
        return False
def matched(open, close):
    opens = "{[("
    closes = "}])"
    return opens.index(open) == closes.index(close)

print(par_check('[{[]'))
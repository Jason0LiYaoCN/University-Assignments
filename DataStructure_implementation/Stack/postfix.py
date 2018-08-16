from stack import Stack

def postfix_eval(postfix_expression):
    operand_stack = Stack()
    token_list = postfix_expression.split()

    for token in token_list:
        if token in "0123456789":
            operand_stack.push(int(token))
        else:
            operand2 = operand_stack.pop()
            operand1 = operand_stack.pop()
            result = do_math(token, operand1, operand2)
            operand_stack.push(result)
    return operand_stack.pop()
def do_math(op, op1, op2):
    if op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else :
        return op1 - op2

def infix_to_postfix(infix_expression):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    op_stack = Stack()
    postfix_expr = []
    token_list = infix_expression.split()

    for token in token_list:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" \
        or token in "0123456789":
            postfix_expr.append(token)
        elif token == '(':
            op_stack.push(token)
        elif token == ')':
            token_top = op_stack.pop()
            while token_top != '(':
                postfix_expr.append(token_top)
                token_top = op_stack.pop()
        else:
            while (not op_stack.is_empty()) \
            and (prec[op_stack.peek()] >= prec[token]):
                postfix_expr.append(op_stack.pop())
            op_stack.push(token)

    while not op_stack.is_empty():
        postfix_expr.append(op_stack.pop())
    return " ".join(postfix_expr)

print(infix_to_postfix("A * B + C * D"))    
print(postfix_eval('7 8 + 3 2 + /'))

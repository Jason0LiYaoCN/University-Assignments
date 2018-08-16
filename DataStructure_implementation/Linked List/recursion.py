import turtle

# my_turtle = turtle.Turtle()
# my_win = turtle.Screen()

# def draw_spiral(my_turtle, line_len):
#     if line_len > 0 :
#         my_turtle.forward(line_len)
#         my_turtle.right(90)
#         draw_spiral(my_turtle, line_len - 5)

# draw_spiral(my_turtle, 14)
# my_win.exitonclick()

def tree(branch_len, t):
    if branch_len > 5 :
        t.forward(branch_len)
        t.right(20)
        tree(branch_len - 15, t)
        t.left(40)
        tree(branch_len - 10, t)
        t.right(20)
        t.backward(branch_len)

def main():
    t = turtle.Turtle()
    my_win = turtle.Screen()
    t.left(90)
    t.up()
    t.backward(100)
    t.down()
    t.color("green")
    tree(75, t)
    my_win.exitonclick()

main()    


def list_sum(num_list):
    if len(num_list) == 1:
        return num_list[0]
    else:
        return num_list[0] + list_sum(num_list[1:])

# print(list_sum([1,2,3,4,5]))

def num_tostr(n, base):
    conver_string = "0123456789ABCDEF"
    if n < base :
        return conver_string[n]
    else:
        return num_tostr(n // base, base) + conver_string[n % base]

# print(num_tostr(36,16))

# Visualising Recursion

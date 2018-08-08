def binary_search(sorted_list, item):
    if len(sorted_list) == 0:
        return False
    mid_index = len(sorted_list)//2
    if sorted_list[mid_index] == item:
        return True
    elif sorted_list[mid_index] < item :
        return binary_search(sorted_list[mid_index + 1:],item)
    else:
        return binary_search(sorted_list[0:mid_index],item)

test_list = [32, 42]
# print(binary_search(test_list, 50))
# print(binary_search(test_list, 13))
print(test_list[3:])
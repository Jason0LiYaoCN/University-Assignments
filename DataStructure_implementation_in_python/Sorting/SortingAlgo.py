def bubble_sort(input_list):
    for comp_num in range(len(input_list)-1, 0, -1):
        for index in range(comp_num):
            if input_list[index] > input_list[index + 1]:
                tmp = input_list[index]
                input_list[index] = input_list[index + 1]
                input_list[index + 1] = tmp

# if subset is already sorted, then saved time for sorting
def short_bubble_sort(input_list):
    pass_num = len(input_list) - 1
    exchanges = True
    while pass_num > 0 and exchanges:
        exchanges = False
        for index in range(pass_num):
            if input_list[index] > input_list[index + 1]:
                exchanges = True
                tmp = input_list[index]
                input_list[index] = input_list[index + 1]
                input_list[index + 1] = tmp
        pass_num = pass_num - 1

# improves because in each pass only do the swapping once
def selection_sort(input_list):
    for pass_num in range(len(input_list)-1, 0, -1):
        pos_of_max = 0
        for location in range(1, pass_num + 1):
            if input_list[location] > input_list[pos_of_max]:
                pos_of_max = location
        tmp = input_list[pos_of_max]
        input_list[pos_of_max] = input_list[pass_num]
        input_list[pass_num] = tmp

def insertion_sort(a_list):
    for index in range(1, len(a_list)):
        position = index
        current_value = a_list[index]

        while position > 0 and a_list[position - 1] > current_value:
            a_list[position] = a_list[position - 1]
            position = position - 1
        
        a_list[position] = current_value
# the time consumption is nlog(n)
def merge_sort(a_list):
    print("Spliting", a_list)
    if len(a_list) > 1:
        mid = len(a_list) // 2
        left_half = a_list[0:mid]
        right_half = a_list[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = 0
        j = 0
        k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                a_list[k] = left_half[i]
                i = i + 1
            else:
                a_list[k] = right_half[j]
                j = j + 1
            k = k + 1
        while i < len(left_half):
            a_list[k] = left_half[i]
            i = i + 1
            k = k + 1
        while j < len(right_half):
            a_list[k] = right_half[j]
            j = j + 1
            k = k + 1
    print("merging", a_list)

# don't need addtional space compared to the merge sort
def quick_sort(a_list):
    quick_sort_helper(a_list, 0, len(a_list) - 1)

def quick_sort_helper(a_list, first, last):
    if first < last:
        split_index = partition(a_list, first, last)
        print(split_index, a_list[split_index])
        quick_sort_helper(a_list, first, split_index - 1)
        quick_sort_helper(a_list, split_index + 1, last)

def partition(a_list, first, last):
    privot_value = a_list[first]
    left_mark = first + 1
    right_mark = last

    done = False

    while not done:

        while a_list[left_mark] <= privot_value and\
        left_mark <= right_mark:
            left_mark = left_mark + 1
        while a_list[right_mark] >= privot_value and\
        right_mark >= left_mark:
            right_mark = right_mark - 1
        if right_mark < left_mark:
            done = True
        else:
            tmp = a_list[left_mark]
            a_list[left_mark] = a_list[right_mark]
            a_list[right_mark] = tmp
        
    tmp = a_list[first]
    a_list[first] = a_list[right_mark]
    a_list[right_mark] = tmp

    return right_mark
    


test_list = [54, 26, 93, 17, 77, 31, 44, 55, 20]
quick_sort(test_list)
print(test_list)

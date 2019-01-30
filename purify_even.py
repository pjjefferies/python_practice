def purify(list_of_numbers):
    new_list_of_numbers = []
    for a_number in list_of_numbers:
        if int(float(a_number)/2) == (float(a_number)/2):
            new_list_of_numbers.append(a_number)
    return new_list_of_numbers
print purify([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
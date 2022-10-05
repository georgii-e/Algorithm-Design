import os
import math
import time


def write_to_file(arr, handler, add_enter=False):
    """function to write to a file: a number, a list, or just a newline"""
    str_arr = ""
    if add_enter:
        handler.write("\n")
        return
    if type(arr) == list:
        for i in arr:
            str_arr += str(i) + "\n"
        handler.write(str_arr + "\n")
    else:
        handler.write(str(arr) + "\n")


def divide_in_files(path, number_of_files=5):
    """function for dividing the initial file into series and writing them into new files"""
    tmp_lst = []
    file_handler = []
    current_index = 0
    current_file = 0
    for file in range(number_of_files):
        file_handler.append(open(str(file) + ".txt", "w"))
    with open(path, "r") as input_file:
        for line in input_file:
            if current_index != 0 and tmp_lst[current_index - 1] >= int(line):
                write_to_file(tmp_lst, file_handler[current_file % number_of_files])
                current_file += 1
                current_index = 0
                tmp_lst.clear()
            current_index += 1
            tmp_lst.append(int(line))
        write_to_file(tmp_lst, file_handler[current_file % number_of_files])
    for file in file_handler:
        file.close()
    print("Divided successful")


def merge_files(previous_names):
    """function for merging small series into larger series"""
    num_of_files = len(previous_names)
    curr_elements = []
    new_file_handler = []
    file_handler = []
    sizes_of_files = [0] * num_of_files
    new_names = []
    current_new_file = 0
    real_length = num_of_files
    for i, name in enumerate(previous_names):
        # opening and calculating file sizes to track their end
        sizes_of_files[i] = os.path.getsize(previous_names[i] + ".txt")
        new_file_handler.append(open(str(int(name) + num_of_files) + ".txt", "w"))
        file_handler.append(open(name + ".txt", "r"))
        symbol = file_handler[i].readline()
        sizes_of_files[i] -= len(symbol) + 1
        # reading the first characters of each file and adding them to the list
        if symbol != "\n" and symbol != "":
            curr_elements.append(int(symbol))
        else:  # if the file runs out of numbers, decrease the number of files with characters
            sizes_of_files[i] = 0
            curr_elements.append(float('inf'))
            real_length -= 1
    while any(x > 1 for x in sizes_of_files):  # outer loop running until all numbers in all files have been processed
        while real_length > 0:  # internal loop that works as long as at least one file contains numbers related to the current series
            min_element = min(curr_elements)
            min_index = curr_elements.index(min_element)
            # writing the smallest number from the list of first numbers in each file to the output file
            write_to_file(min_element, new_file_handler[current_new_file % num_of_files])
            curr_elements.pop(min_index)
            # replacing this number with the next one from the same file
            symbol = file_handler[min_index].readline()
            sizes_of_files[min_index] -= len(symbol) + 1
            if symbol != "\n" and symbol != "":
                curr_elements.insert(min_index, int(symbol))
            else:
                curr_elements.insert(min_index, float('inf'))
                real_length -= 1
        write_to_file(None, new_file_handler[current_new_file % num_of_files], True)
        current_new_file += 1
        curr_elements.clear()
        real_length = num_of_files
        # repeating the procedure for the next series and the next output file
        for i in range(num_of_files):
            symbol = file_handler[i].readline()
            sizes_of_files[i] -= len(symbol) + 1
            if symbol != "\n" and symbol != "":
                curr_elements.append(int(symbol))
            else:
                sizes_of_files[i] = 0
                curr_elements.append(float('inf'))
                real_length -= 1
    for file in new_file_handler:
        file.close()
    for i, file in enumerate(file_handler):
        if current_new_file - 1 >= i:
            new_names.append(str(int(file.name[:-4]) + num_of_files))
        file.close()
        os.remove(file.name)
    if len(new_names) < num_of_files:
        for i in range(num_of_files - len(new_names)):
            os.remove(str(int(new_names[-1]) + i + 1) + ".txt")
    print(new_names)
    return new_names


try:
    os.remove("Result.txt")
except FileNotFoundError:
    pass
input_file_path = "input_medium.txt"
amount_of_files = 8 + int(math.log2(os.path.getsize(input_file_path) / 1000000)) if math.log2(
    os.path.getsize(input_file_path) / 1000000) > 0 else 5
divide_in_files(input_file_path, amount_of_files)
start = time.time()
file_names = merge_files([str(i) for i in range(amount_of_files)])
while len(file_names) > 1:
    file_names = merge_files(file_names)
os.rename(str(file_names[0]) + ".txt", "Result.txt")
end = time.time()
print("Time taken: ", str(end - start), "seconds / ", str((end - start) / 60), "minutes")

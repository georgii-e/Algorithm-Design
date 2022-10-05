import os
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


def divide_input_file(path, chunk):
    with open(path, "r") as numbers_from_file:
        num_line = 0
        num_file = 0
        tmp_lst = []
        line = numbers_from_file.readline()
        while line != "":
            tmp_lst.append(int(line))
            num_line += 1
            line = numbers_from_file.readline()
            if num_line == chunk:
                with open(f"{num_file}.txt", "w") as numbers_to_file:
                    tmp_lst.sort()
                    write_to_file(tmp_lst, numbers_to_file)
                    num_file += 1
                    tmp_lst.clear()
                    num_line = 0
                    print("Created file number:", num_file)
    return [f"{i}" for i in range(num_file)]


def merge_files(previous_names):
    """function for merging small series into larger series"""
    print("Merging started")
    num_of_files = len(previous_names)
    output_file = open("Result.txt", "w")
    curr_elements = []
    file_handler = []
    real_length = num_of_files
    for i, name in enumerate(previous_names):
        # opening files
        file_handler.append(open(name + ".txt", "r"))
        symbol = file_handler[i].readline()
        # reading the first characters of each file and adding them to the list
        if symbol != "\n" and symbol != "":
            curr_elements.append(int(symbol))
        else:  # if the file runs out of numbers, decrease the number of files with characters
            curr_elements.append(float('inf'))
            real_length -= 1
    while real_length > 0:  # internal loop that works as long as at least one file contains numbers related to the current series
        min_element = min(curr_elements)
        min_index = curr_elements.index(min_element)
        # writing the smallest number from the list of first numbers in each file to the output file
        write_to_file(min_element, output_file)
        curr_elements.pop(min_index)
        # replacing this number with the next one from the same file
        symbol = file_handler[min_index].readline()
        if symbol != "\n" and symbol != "":
            curr_elements.insert(min_index, int(symbol))
        else:
            curr_elements.insert(min_index, float('inf'))
            real_length -= 1
    write_to_file(None, output_file, True)
    curr_elements.clear()
    real_length = num_of_files
    # repeating the procedure for the next series
    for i in range(num_of_files):
        symbol = file_handler[i].readline()
        if symbol != "\n" and symbol != "":
            curr_elements.append(int(symbol))
        else:
            curr_elements.append(float('inf'))
            real_length -= 1
    output_file.close()
    for file in file_handler:
        file.close()
        os.remove(file.name)


MAX_SIZE_OF_CHUNK = 1171875
start = time.time()
names = divide_input_file("input_large.txt", MAX_SIZE_OF_CHUNK)
merge_files(names)
end = time.time()
print("Time taken: ", str(end - start), "seconds / ", str((end - start) / 60), "minutes")

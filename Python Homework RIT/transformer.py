__author__ = 'BR'
__author__ = 'TB'

"""
Author: BIKASH ROY (Username - br8376)
Author: TANAY BHARDWAJ (Username - tb7315)

File name: transformer.py
"""

import sys


def shift(message, instruction, decrypt):
    """
        Method to shift the character at given index (i) by (k) times. If k is not defined, default is 1.
        - Works on negative operations
        :parameter: message - the string which is to be encrypted.
        :parameter: instruction - instruction to shift the characters.
        :parameter: decrypt - flag for decryption
        :return: the new string after transformation
    """
    index_to_shifted = int(instruction[1])
    by_times_forward = 1
    if decrypt:
        by_times_forward = -1
    condition_for_k_forward = "," in instruction and instruction.split(",")[1] != ""
    if condition_for_k_forward:
        split_message = instruction.split(",")
        by_times_forward = int(split_message[1])
        if decrypt:
            by_times_forward = -by_times_forward
    char_acsii_value = ord(message[index_to_shifted])
    if char_acsii_value in range(65, 91):
        if char_acsii_value == 90:
            if by_times_forward < 0:
                char_acsii_value += by_times_forward
            else:
                char_acsii_value = 65 + by_times_forward - 1
        else:
            char_acsii_value += by_times_forward
    new_message = list(message)
    new_message[index_to_shifted] = chr(char_acsii_value)
    new_message = "".join(new_message)
    return new_message


def rotate(message, instruction, decrypt):
    """
        Method to rotate the string one position to the right, also can be operated with exponents, which dictates the
        number of characters to be rotated.
        - Works on negative operations
        :parameter: message - the string which is to be encrypted.
        :parameter: instruction - instruction to rotate the characters.
        :parameter: decrypt - flag for decryption
        :return: the new string after transformation
    """
    if len(instruction) == 1:
        number_of_characters_to_rotates = 1
    else:
        check_minus = instruction[1]
        if check_minus == "-":
            number_of_characters_to_rotates = int(instruction[2])
            if number_of_characters_to_rotates > len(message):
                return "Not enough string to rotate."
        else:
            number_of_characters_to_rotates = int(instruction[1])
    if decrypt:
        for i in range(0, number_of_characters_to_rotates):
            message = message[1:] + message[0]
        return message
    else:
        for i in range(0, number_of_characters_to_rotates):
            message = message[-1] + message[:-1]
        return message


def duplicate(message, instruction, decrypt):
    """
        Method to duplicate (in place) the letter at index i..by k times
        - Doesn't  work on negative operations
        :parameter: message - the string which is to be encrypted.
        :parameter: instruction - instruction to duplicate the characters.
        :parameter: decrypt - flag for decryption
        :return: the new string after transformation
    """
    if decrypt:
        return "Duplicate cannot be decrypted."
    index_to_be_duplicated = int(instruction[1])
    if index_to_be_duplicated not in range(0, len(message)):
        return "No character found to be duplicated. Index out of range"
    condition_for_k_duplicate = "," in instruction and instruction.split(",")[1] != ""
    duplicate_by_times = 1
    if condition_for_k_duplicate:
        split_message = instruction.split(",")
        duplicate_by_times = int(split_message[1])
    character_to_be_duplicated = message[index_to_be_duplicated]
    return message[0:index_to_be_duplicated + 1] + character_to_be_duplicated * duplicate_by_times + \
           message[index_to_be_duplicated + 1:]


def swap(message, instruction, decrypt):
    """
        Method to swap the letters at index i and index j.
        - Works on negative operations
        :parameter: message - the string which is to be encrypted.
        :parameter: instruction - instruction to swap the characters.
        :parameter: decrypt - flag for decryption
        :return: the new string after transformation
    """
    index_i = int(instruction[1])
    if index_i < 0:
        return "No element to swap. Index smaller than message length"
    index_j = int(instruction.split(",")[1])
    if index_j > len(message):
        return "No element to swap. Index larger than message length"
    if decrypt:
        index_i, index_j = index_j, index_i
    i_character_to_be_swapped = message[index_i]
    j_character_to_be_swapped = message[index_j]
    message = list(message)
    message[index_i] = j_character_to_be_swapped
    message[index_j] = i_character_to_be_swapped
    return "".join(message)


def swap_groups(message, instruction, decrypt):
    """
        Method swap_groups operates a little differently. In this case, we conceptually divide the string to
        g equal-sized groups of letters, and then swap groups i and j..
        - Works on negative operations
        :parameter: message - the string which is to be encrypted.
        :parameter: instruction - instruction to swap the groups.
        :parameter: decrypt - flag for decryption
        :return: the new string after transformation
    """
    index_i = int(instruction[4])
    if index_i < 0:
        return "No element to swap. Index smaller than message length"
    index_j = int(instruction.split(",")[1])
    if index_j > len(message):
        return "No element to swap. Index larger than message length"
    if decrypt:
        index_i, index_j = index_j, index_i
    number_of_groups_needed = int(instruction[2])
    group_size = int(len(message) / number_of_groups_needed)
    message = [message[i:i + group_size] for i in range(0, len(message), group_size)]
    if index_j > len(message):
        return "Index larger than swapping groups"
    i_group_to_be_swapped = message[index_i]
    j_group_to_be_swapped = message[index_j]
    message[index_i] = j_group_to_be_swapped
    message[index_j] = i_group_to_be_swapped
    return "".join(message)


def es_rev(message, decrypt):
    """
        Method to reverse the message and add a "Z" at the end.
        - Works on negative operations
        e.g - HOW -> WOHZ
        :parameter: message - the string which is to be encrypted.
        :parameter: decrypt - flag for decryption
        :return: the new string after transformation
    """
    if decrypt:
        return message[0:len(message)-1][::-1]
    else:
        return message[::-1] + "Z"


def encrypt_decrypt(message_filename, instruction_filename, output_filename, decrypt):
    """
        This method encrypts and decrypts the Messages from message.txt file with the set of instructions from
        instructions.txt file and writes the output to output.txt file
        :parameter: message_filename - messages file name to be read.
        :parameter: instruction_filename - instructions file name to be read.
        :parameter: output_filename - output file name, where result is stored.
        :parameter: decrypt - flag for decryption
        :return: None
    """
    message_list = ""
    instruction_list = ""
    output_list = ""
    try:
        with open(message_filename, "r") as message_file:
            message_list = message_file.readlines()
        with open(instruction_filename, "r") as instruction_filename:
            instruction_list = instruction_filename.readlines()
    except FileNotFoundError as fnf:
        print(fnf)
    for i in range(0, len(message_list)):
        message, instruction = message_list[i], instruction_list[i].strip()
        instruction = instruction.split(";")
        if decrypt:
            instruction = instruction[::-1]
        for j in range(0, len(instruction)):
            if instruction[j].startswith("S"):
                shift_message = shift(message.replace("\n", ""), instruction[j], decrypt)
                message = shift_message
            if instruction[j].startswith("R"):
                rotate_message = rotate(message.replace("\n", ""), instruction[j], decrypt)
                message = rotate_message
            if instruction[j].startswith("D"):
                duplicated_message = duplicate(message.replace("\n", ""), instruction[j], decrypt)
                message = duplicated_message
            if instruction[j].startswith("T") and "(" not in instruction[j]:
                swapped_message = swap(message.replace("\n", ""), instruction[j], decrypt)
                message = swapped_message
            if instruction[j].startswith("T("):
                swapped_group_message = swap_groups(message.replace("\n", ""), instruction[j], decrypt)
                message = swapped_group_message
            if instruction[j].startswith("E"):
                rev_message = es_rev(message.replace("\n", ""), decrypt)
                message = rev_message
        output_list += message.replace("\n", "") + "\n"
    try:
        with open(output_filename, "w") as output_file:
            output_file.write(str(output_list))
    except FileNotFoundError as fnf:
        print(fnf)


def main():
    """
        The main method.
        Arguments are taken in form the command line.
    """
    arguments = sys.argv
    if len(arguments) != 5:
        print("Enter -> message file name -> enter instruction file name -> enter output file name -> e/d")
        return
    message_file_name = arguments[1] + ".txt"
    instruction_file_name = arguments[2] + ".txt"
    output_file_name = arguments[3] + ".txt"
    is_decrypt = arguments[4] == "d"
    if is_decrypt:
        message_file_name = output_file_name
    encrypt_decrypt(message_file_name, instruction_file_name, output_file_name, is_decrypt)


if __name__ == '__main__':
    main()

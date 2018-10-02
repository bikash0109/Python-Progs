"""REMOVE ALL PRINT STATEMENTS"""


def shift_at_index(message, instruction):
    index_to_shifted = int(instruction[1])
    by_times_forward = 1
    condition_for_k_forward = "," in instruction and instruction.split(",")[1] != ""
    if condition_for_k_forward:
        split_message = instruction.split(",")
        by_times_forward = int(split_message[1])
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


def rotate(message, instruction):
    if len(instruction) == 1:
        number_of_characters_to_rotates = 1
    else:
        check_minus = instruction[1]
        if check_minus == "-":
            number_of_characters_to_rotates = int(instruction[2])
            if number_of_characters_to_rotates > len(message):
                return "Not enough string to rotate."
            return message[len(message) - number_of_characters_to_rotates:] + message[0:len(
                message) - number_of_characters_to_rotates]
        else:
            number_of_characters_to_rotates = int(instruction[1])
            if number_of_characters_to_rotates > len(message):
                return "Not enough string to rotate."
    return message[len(message) - number_of_characters_to_rotates:] + message[:-number_of_characters_to_rotates]


def duplicate(message, instruction):
    index_to_be_duplicated = int(instruction[1])
    if index_to_be_duplicated not in range(0, len(message) - 1):
        return "No character found to be duplicated. Index out of range"
    condition_for_k_duplicate = "," in instruction and instruction.split(",")[1] != ""
    duplicate_by_times = 1
    if condition_for_k_duplicate:
        split_message = instruction.split(",")
        duplicate_by_times = int(split_message[1])
    character_to_be_duplicated = message[index_to_be_duplicated]
    return message[0:index_to_be_duplicated + 1] + character_to_be_duplicated * duplicate_by_times + \
           message[index_to_be_duplicated + 1:]


def swap(message, instruction):
    index_i = int(instruction[1])
    if index_i < 0:
        return "No element to swap. Index smaller than message length"
    index_j = int(instruction.split(",")[1])
    if index_j > len(message):
        return "No element to swap. Index larger than message length"
    i_character_to_be_swapped = message[index_i]
    j_character_to_be_swapped = message[index_j]
    message = list(message)
    message[index_i] = j_character_to_be_swapped
    message[index_j] = i_character_to_be_swapped
    return "".join(message)


def swap_with_limiter(message, instruction):
    index_i = int(instruction[4])
    if index_i < 0:
        return "No element to swap. Index smaller than message length"
    index_j = int(instruction.split(",")[1])
    if index_j > len(message):
        return "No element to swap. Index larger than message length"
    number_of_groups_needed = int(instruction[2])
    group_size = int(len(message)/number_of_groups_needed)
    message = [message[i:i + group_size] for i in range(0, len(message), group_size)]
    if index_j > len(message):
        return "Index larger than swapping groups"
    i_group_to_be_swapped = message[index_i]
    j_group_to_be_swapped = message[index_j]
    message[index_i] = j_group_to_be_swapped
    message[index_j] = i_group_to_be_swapped
    return "".join(message)


def main():
    shift_at_index("Z", "S0,-4")
    rotate("SEHOR", "R-3")
    duplicate("HOPED", "D2,4")
    swap("SAUCE", "T3,1")
    swap_with_limiter("BACKHANDES", "T(4)0,2")


if __name__ == '__main__':
    main()

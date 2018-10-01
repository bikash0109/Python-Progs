def shift_at_index(message, instruction):
    index = int(instruction[1])
    condition_for_k_forward = "," in instruction and instruction.split(",", len(instruction) - 1)[1] != ""
    if condition_for_k_forward:
        by_times_forward = int(instruction.split(",", len(instruction) - 1)[1])
    char_acsii_value = ord(message[index])
    if char_acsii_value in range(65, 91):
        if char_acsii_value == 90:
            if condition_for_k_forward:
                char_acsii_value += by_times_forward
            else:
                char_acsii_value = 65
        else:
            if condition_for_k_forward:
                char_acsii_value += by_times_forward
            else:
                char_acsii_value += 1

    new_message = list(message)
    new_message[index] = chr(char_acsii_value)
    new_message = "".join(new_message)
    print(new_message)
    return new_message


def rotate(message, instruction):
    check_minus = instruction[1]
    if check_minus == "-":
        number_of_characters_to_rotates = instruction[2]
    else:
        number_of_characters_to_rotates = instruction[1]
    pass


def main():
    shift_at_index("HORSE", "S4`,4")


if __name__ == '__main__':
    main()

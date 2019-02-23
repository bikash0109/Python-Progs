import sys


def menu(userinput):
    while userinput is not 'q':
        if userinput == '1':
            print(userinput)
        if userinput == '2':
            print(userinput + str(2))
        if userinput == 'q':
            sys.exit(0)
        print("1. GoDie \n 2. GoSwim\n 3. GoDance\n 4. q - Quit")
        userinput = input("Enter your choice: ")


def test():
    print("\n1. GoDie \n 2. GoSwim\n 3. GoDance\n 4. q - Quit")
    userinput = input("Enter your choice: ")
    if userinput == 'q':
        sys.exit(0)
    menu(userinput)


if __name__ == '__main__':
    test()

import sys
import os

from firstPass import *

symbol_table = {'SP': '0000000000000000', 'LCL': '0000000000000001', 'ARG':
                '0000000000000010', 'THIS': '0000000000000011', 'THAT':
                '0000000000000100', 'SCREEN': '0100000000000000', 'KBD':
                '0110000000000000'}


def init_symbol_table(symbol_table):
    """
    init the symbol table with R0-R15
    :param symbol_table:
    :return:
    """
    for i in range(16):
        symbol_table['R' + str(i)] = num_to_binary(str(i))


def main(argv):
    """
    runs the program by getting a path and converting all the asm files in
    the path to binary codes, and writing them to hack files
    :param argv:
    :return:
    """
    # argv[1] is the path
    path = argv[1]
    # if we got a path of file
    if path.endswith('.asm'):
        files = [path]
    else:  # got a directory, so convert all the asm files
        files = [path + '/' + f for f in os.listdir(path) if
                 f.endswith('.asm')]
    for file_path in files:
        init_symbol_table(symbol_table)
        # getting all the lines in the asm file:
        commands_list = first_pass(file_path, symbol_table)
        # converting the asm lines to binary:
        binary_code = line_to_binary(commands_list, symbol_table)
        # write all binary lines in the hack file:
        with open(file_path.strip('.asm')+'.hack', 'w') as file:
            for line in binary_code:
                file.write(line + '\n')
        file.close()


if __name__ == "__main__":
    main(sys.argv)

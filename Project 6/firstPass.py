from secondPass import *

SPACE = ' '
COMMENT = '//'
OPEN_LABEL = '('


def first_pass(path, symbol_table):
    """
    copy all the lines in the asm file to a list and returns it
    :param path: the path of the asm file
    :param symbol_table: the symbol table of the code
    :return: a list of all the lines in the asm code
    """
    with open(path, "r") as file:
        commands = []
        counter = 0
        for line in file:
            line = remove_spaces_comments(line)
            if line == '':
                continue
            elif line[0] == OPEN_LABEL:
                label = line[1:-1]
                symbol_table[label] = num_to_binary(counter)
            else:
                commands.append(line)
                counter += 1
    return commands


def remove_spaces_comments(line):
    """
    remove all the spaces and comments in line
    :param line: the asm code line
    :return: the line after removing the spaces and the comments
    """
    line = line.replace(SPACE, '')
    line = line.split(COMMENT)[0]
    return line.rstrip()


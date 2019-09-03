

DEST = {'null': '000', 'M': '001', 'D': '010', 'MD': '011', 'A': '100',
        'AM': '101', 'AD': '110', 'AMD': '111'}

JMP = {'null': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100',
       'JNE': '101', 'JLE': '110', 'JMP': '111'}

COMP = {'0': '110101010', '1': '110111111', '-1': '110111010',
        'D': '110001100', 'A': '110110000', '!D': '110001101',
        '!A': '110110001', '-D': '110001111', '-A': '110110011', 'D+1':
        '110011111', 'A+1': '110110111', 'D-1': '110001110',
        'A-1': '110110010', 'D+A': '110000010', 'D-A': '110010011', 'A-D':
        '110000111', 'D&A': '110000000', 'D|A': '110010101',
        'M': '111110000', '!M': '111110001', '-M': '111110011', 'M+1':
        '111110111', 'M-1': '111110010', 'D+M': '111000010', 'D-M':
        '111010011', 'M-D': '111000111', 'D&M': '111000000', 'D|M':
        '111010101', 'D<<': '010110000', 'A<<': '010100000', 'M<<':
        '011100000', 'D>>': '010010000', 'A>>': '010000000',  'M>>':
        '011000000'}

NULL = 'null'
EQ = '='
SEMICOLON = ';'
BINARY_LEN = 16


def line_to_binary(lines, symbol_table):
    """
    gets a list of the lines of the asm code and return a list of the lines
    in binary code
    :param lines: an array of the line of the asm code
    :param symbol_table: the symbol table of the code
    :return: list of the lines in binary code
    """
    binary_code = []
    counter = 16
    for line in lines:
        binary_line, counter = read_line(line, symbol_table, counter)
        binary_code.append(binary_line)
    return binary_code


def read_line(line, symbol_table, counter):
    """
    gets the asm line and returns the line converted to binary code
    :param line: the line in the code in asm
    :param symbol_table: the symbol table of the code
    :param counter: num counter for the variables in the code
    :return: the line converted to binary and the counter of the variables
    """
    if line[0] == '@':
        return read_a_instruction(line, symbol_table, counter)

    else:
        return read_c_instruction(line, counter)


def read_c_instruction(ins, counter):
    """
    gets a line of c-instruction of the asm code and convert is to binary
    :param ins: (string) instruction
    :param counter: num counter for the variables in the code
    :return: binary code of ins
    """
    operator_equals = False
    operator_semicolon = False
    for letter in ins:
        if letter == SEMICOLON:
            operator_semicolon = True
        if letter == EQ:
            operator_equals = True

    # disassemble each command and return the binary code
    if operator_equals and operator_semicolon:
        op_equal_list = ins.split(EQ)
        op_semicolon_list = op_equal_list[1].split(SEMICOLON)
        dest = op_equal_list[0]
        comp = op_semicolon_list[0]
        jmp = op_semicolon_list[1]
        return '1' + COMP[comp] + DEST[dest] + JMP[jmp], counter

    elif operator_equals:
        op_equal_list = ins.split(EQ)
        dest = op_equal_list[0]
        comp = op_equal_list[1]
        return '1' + COMP[comp] + DEST[dest] + JMP[NULL], counter

    elif operator_semicolon:
        op_semicolon_list = ins.split(SEMICOLON)
        comp = op_semicolon_list[0]
        jmp = op_semicolon_list[1]
        return '1' + COMP[comp] + DEST[NULL] + JMP[jmp], counter


def read_a_instruction(ins, symbol_table, counter):
    """
    gets a line of a-instruction of the asm code and convert is to binary
    :param ins: string of the address
    :param symbol_table: the symbol table of the code
    :param counter: num counter for the variables in the code
    :return: binary string that represents the address
    """
    ins = ins[1:]
    if ins.isdigit():
        return num_to_binary(ins), counter
    # if the variables already exists
    elif ins in symbol_table:
        return symbol_table[ins], counter
    # if not, create new variable in the symbol table
    else:
        symbol_table[ins] = num_to_binary(counter)
        return symbol_table[ins], counter + 1


def num_to_binary(num):
    """
    convert a num to binary
    :param num: the num to convert
    :return: the num converted to binary string
    """
    binary = bin(int(num))[2:]
    return (BINARY_LEN - len(binary)) * '0' + binary




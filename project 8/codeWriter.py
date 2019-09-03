from parser import *


class CodeWriter:

    def __init__(self, file_name, parser):
        self.name = file_name
        self.parser = parser

    def file_to_list(self ,path):
        """
        :param path: a string representation of file path
        :return: a list of lines from line 0 to line n-1
        """
        with open(path, 'r') as file:
            code_lines = []
            for line in file:
                line = self.remove_spaces_comments(line)
                if line == '':
                    continue
                else:
                    code_lines.append(line)
        return code_lines


    def vm_code_list_to_asm(self ,code_lines):
        """
        takes a list of vm code and translating it to a list of assembler code
        :param code_lines: list of string, each item within the list represents
        a code in vm
        :return: a list of strings, each item within the list represents
        the lines of code that fits the vm list in assembler
        """
        #todo remove init 256
        asm_code = []
        self.parser.file_name = self.name
        for line in code_lines:
            asm_code.append(self.parser.line_to_asm(line))
        return asm_code


    def write_to_file(self ,path, asm_code):
        """
        this function is writing assembler code into a file
        :param path: string, file path
        :param asm_code: the asm code to write to the file
        """
        with open(path, 'w') as file:
            for line in asm_code:
                file.write(line)


    def remove_spaces_comments(self ,line):
        """
        the function removes comments and spaces from the line
        :param line: string, a line
        :return: the strings after deleting irrelevant character
        """
        line = line.split('//')[0]
        line = line.strip()
        return line








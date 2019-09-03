MEMORY_TYPES = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that':
    'THAT', 'temp': '5'}


class Parser:

    def __init__(self, file_name):
        self.counter = 0
        self.file_name = file_name

    def line_to_asm(self, line):
        """
        this function takes a line of vm code and translating it into asm code
        :param line: a line of vm code
        :param counter: a counter of lines
        :return: list of assembler code lines
        """
        self.counter += 1
        if line == 'add':
            return '//ADD\n@SP\nA=M-1\nD=M\nA=A-1\nM=M+D\n@SP\nM=M-1\n'
        elif line == 'sub':
            return '//SUB\n@SP\nA=M-1\nD=M\nA=A-1\nM=M-D\n@SP\nM=M-1\n'
        elif line == 'neg':
            return '//NEG\n@SP\nA=M-1\nD=M\n@0\nD=A-D\n@SP\nA=M-1\nM=D\n'
        elif line == 'eq':
            return '//eq\n@SP\nA=M-1\nD=M\n@NEG_SP-1_'+str(self.counter)+'\nD;JLT\n//SP-1 IS POS\n@SP\nA=M-1\nA=A-1' \
                '\nD=M\n@sub'+str(self.counter)+'\nD;JGE\n' \
                '(NEG_SP-1_'+str(self.counter)+')\n@SP\nA=M-1\n' \
                'A=A-1\nD=M\n@sub'+str(self.counter)+'' \
                '\nD;JLE\n@NOT_EQ'+str(self.counter)+'\n0;JMP\n(sub' \
                ''+str(self.counter)+')\n//EQ\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@isEq'+str(self.counter)+'\n' \
                'D;JEQ\n(NOT_EQ'+str(self.counter)+')\n@0\nD=A\n@SP\nA=M-1\nA=A-1\nM=D\n@END'+str(self.counter)+'\n' \
                '0;JMP\n(isEq'+str(self.counter)+')\n@SP\nA=M-1\nA=A-1\nM=0\nM=M-1\n(END'+str(self.counter)+'' \
                ')\n@SP\nM=M-1\n'
        elif line == 'gt':
            return '//gt\n@SP\nA=M-1\nD=M\n@NEG_SP-1_' + str(self.counter) + '\nD;JLT\n//SP-1 IS POS\n@SP\nA=M-1\n' \
                    'A=A-1\nD=M\n@NOT_GT_' \
                   ''+str(self.counter)+'\nD;JLT\n@SUB_'+str(self.counter)+'\n0;JMP\n(NEG_SP-1_'+str(self.counter)+')' \
                   '\n@SP\nA=M-1\nA=A-1\nD=M\n@isGT_'+str(self.counter)+'\nD;JGT\n(SUB_'+str(self.counter)+')\n//GT\n' \
                    '@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@isGT_'+str(self.counter)+'\nD;JGT\n(NOT_GT_'+str(self.counter)\
                    +')\n@0\nD=A\n@SP\nA=M-1\nA=A-1\nM=D\n@END_'+str(self.counter)+'\n0;JMP\n(isGT_'+str(self.counter)\
                    +')\n@SP\nA=M-1\nA=A-1\nM=0\nM=M-1\n(END_'+str(self.counter)+')\n@SP\nM=M-1\n'
        elif line == 'lt':
            return '//lt\n@SP\nA=M-1\nD=M\n@NEG_SP-1_' + str(self.counter) + '\nD;JLT\n//SP-1 IS POS\n@SP\nA=M-1\n' \
                    'A=A-1\nD=M\n@isLt_' + str(self.counter) + '\nD;JLT\n@SUB_' + str(self.counter) + '\n0;JMP\n' \
                    '(NEG_SP-1_' + str(self.counter) + ')\n@SP\nA=M-1\nA=A-1\nD=M\n@NOT_LT_' + str(self.counter) + \
                    '\nD;JGT\n(SUB_' + str(self.counter) + ')\n//LT\n@SP\nA=M-1\nD=M\nA=A-1\nD=M-D\n@isLt_' +  \
                   str(self.counter) + '\nD;JLT\n(NOT_LT_' + str(self.counter) + ')\n@0\nD=A\n@SP\nA=M-1\nA=A-1\n' \
                    'M=D\n@END_' + str(self.counter) + '\n0;JMP\n(isLt_' + str(self.counter) + ')\n@SP\nA=M-1\n' \
                    'A=A-1\nM=0\nM=M-1\n(END_' + str(self.counter) + ')\n@SP\nM=M-1\n'
        elif line == 'and':
            return '//AND\n@SP\nA=M-1\nD=M\nA=A-1\nM=D&M\n@SP\nM=M-1\n'

        elif line == 'or':
            return '//OR\n@SP\nA=M-1\nD=M\nA=A-1\nM=D|M\n@SP\nM=M-1\n'

        elif line == 'not':
            return '//NOT\n@SP\nA=M-1\nM=!M\n'
        elif line.startswith('pop'):
            return self.pop_to_asm(line)
        elif line.startswith('push'):
            return self.push_to_asm(line)


    def pop_to_asm(self,line):
        """
        translating pop commands
        :param line: a pop command in vm
        :return: pop command in asm
        """
        # @temp=R13, @add = r14
        memory_type, num = self.split_line(line)
        # pointer 0 means this pointer 1 means that
        if memory_type == 'pointer':
            if num == '0':
                memory_type = 'this'
                return '//pop' + memory_type + num + \
                       '\n@SP\nM=M-1\nA=M\nD=M\n@' + MEMORY_TYPES[memory_type] + \
                       '\nM=D\n'
            if num == '1':
                memory_type = 'that'
                return '//pop' + memory_type + num + \
                       '\n@SP\nM=M-1\nA=M\nD=M\n@' + MEMORY_TYPES[memory_type] + \
                       '\nM=D\n'

        if memory_type == 'static':
            return '//pop static\n@SP\nA=M\nA=A-1\nD=M\n@'+self.file_name+'.' + num + '\nM=D\n@SP\nM=M-1\n'

        # pop temp i ==> addr=5+i, SP--, *addr=*SP

        # pop segment i ==> addr = segmentPointer + i, SP--, *addr = *SP

        if memory_type == 'temp':
            return '//pop temp\n@SP\nA=M-1\nD=M\n@R13\nM=D\n@5\nD=A\n@' + num + \
                   '\nD=A+D\n@R14\nM=D\n@R13\nD=M\n@R14\nA=M\nM=D\n@SP\nM=M-1\n'

        return '//pop' + memory_type + num + '\n@SP\nA=M-1\nD=M\n@R13\nM=D\n@' \
               + MEMORY_TYPES[memory_type] + '\nD=M\n@' + num + \
               '\nD=A+D\n@R14\nM=D\n@R13\nD=M\n@R14\nA=M\nM=D\n@SP\nM=M-1\n'


    def push_to_asm(self,line):
        """
        translating push command to asm from vm
        :param line: string, vm code
        :return: push command in asm
        """
        memory_type, num = self.split_line(line)

        # push constant i ==> *sp=i, sp++
        if memory_type == 'constant':
            return '//push constant\n@' + num + '\n' + \
                   'D=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        # push static i, push from RAM[16] until RAM[255]
        if memory_type == 'static':
            return '//static\n@'+ self.file_name+'.' + num + '\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        # push temp i ==> addr=5+i, *SP=*addr, SP++

        # push segment i ==> addr = segmentPointer, *sp=*addr, SP++

        if memory_type == 'temp':
            return '//push temp\n@5\nD=A\n@' + num + '\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        if memory_type == 'pointer':
            if num == '0':
                memory_type = 'this'
                return '//push' + memory_type + num + '\n@' + MEMORY_TYPES[
                    memory_type] + '\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
            if num == '1':
                memory_type = 'that'
                return '//push' + memory_type + num + '\n@' + MEMORY_TYPES[
                           memory_type] + '\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        return '//push' + memory_type + num + '\n@' + MEMORY_TYPES[memory_type] \
               + '\nD=M\n@' + num + '\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'


    def split_line(self,line):
        """
        split line by a white space
        :param line: command line
        :return: the strings that comes after the command. memory type, numer
        """
        parts = ' '.join(line.split()).split(' ')
        return parts[1], parts[2]
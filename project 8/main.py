from codeWriter import *
import sys
import os


def main(argv):
    """
    main function, calls all methods required to translate vm code to
    to assembler
    :param argv: argv[1] path of file/directory with vm code (.vm)
    """
    path = argv[1]
    parts = path.split('/')
    output_name = parts[len(parts)-1].replace('.vm', '')
    if path.endswith('.vm'):
        files = [path]
    else:
        files = [path+'/'+f for f in os.listdir(path) if f.endswith('.vm')]
    vm_code = []
    if not path.endswith('.vm'):
        vm_code.append('call Sys.init')
    asm_code = ['@256\nD=A\n@SP\nM=D\n']
    first_file = True
    pars = Parser(output_name)
    for file in files:
        file_name = file.split('/')
        file_name = file_name[len(file_name)-1].replace('.vm', '')
        code_writer = CodeWriter(file_name, pars)
        if first_file:
            vm_code = vm_code + code_writer.file_to_list(file)
            first_file = False
        else:
            vm_code = code_writer.file_to_list(file)
        asm_code = asm_code + code_writer.vm_code_list_to_asm(vm_code)
    if path.endswith('.vm'):
        code_writer.write_to_file(path.replace('.vm', '.asm'), asm_code)
    else:
        code_writer.write_to_file(path+'/'+output_name+'.asm', asm_code)


if __name__ == '__main__':
    main(sys.argv)
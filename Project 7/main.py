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
    if path.endswith('.vm'):
        files = [path]
    else:
        files = [path+'/'+f for f in os.listdir(path) if f.endswith('.vm')]

    for file in files:
        file_name = file.split('/')
        file_name = file_name[len(file_name)-1].replace('.vm','')
        code_writer = CodeWriter(file_name)

        vm_code = code_writer.file_to_list(file)
        asm_code = code_writer.vm_code_list_to_asm(vm_code)
        code_writer.write_to_file(file.strip('.vm')+'.asm', asm_code)


if __name__ == '__main__':
    main(sys.argv)
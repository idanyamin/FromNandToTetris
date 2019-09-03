class VMWriter:
    """This class writes VM commands into a file. It encapsulates the VM
    command syntax. """

    def __init__(self, output_file):
        """Creates a new file and prepares it for writing VM commands """
        self.file = open(output_file, 'w')

    def write_push(self, segment, index):
        """Writes a VM push command"""
        self.file.write('push '+segment+' '+str(index)+'\n')

    def write_pop(self, segment, index):
        """Writes a VM pop command"""
        self.file.write('pop ' + segment + ' ' + str(index) + '\n')

    def write_arithmetic(self, command):
        """Writes a VM arithmetic command """
        self.file.write(command + '\n')

    def write_label(self, label):
        """Writes a VM label command """
        self.file.write('label ' + label+'\n')

    def write_go_to(self, label):
        """Writes a VM goto command """
        self.file.write('goto ' + label+'\n')

    def write_if(self, label):
        """Writes a VM If-goto command """
        self.file.write('if-goto ' + label+'\n')

    def write_call(self, name, n_args):
        """Writes a VM call command """
        self.file.write('call ' + name + ' ' + str(n_args) + '\n')

    def write_function(self, name, n_locals):
        """Writes a VM function command """
        self.file.write('function ' + name + ' ' + str(n_locals) + '\n')

    def write_return(self):
        """Writes a VM return command """
        self.file.write('return' + '\n')

    def write_string(self, string):
        """writes a string """
        string = string[1:-1]
        self.write_push('constant', str(len(string)))
        self.file.write('call String.new 1\n')
        for char in string:
            self.write_push('constant', ord(char))
            self.file.write('call String.appendChar 2\n')

    def write_multiply(self):
        """writes a multiplication command"""
        self.file.write('call Math.multiply 2\n')

    def write_divide(self):
        """writes a division command"""
        self.file.write('call Math.divide 2\n')

    def write_comment(self, comment):
        """writes a comment"""
        # self.file.write(comment + '\n')
        pass

    def close(self):
        """closes the output file"""
        self.file.close()

import os

from compilationEngine import *
import sys


class JackAnalyzer:

    def __init__(self, compiler, output):
        self.compiler = compiler
        self.output = output

    def write_output(self):
        """writes the xml file - the output of this program"""
        with open(self.output, 'w') as file:
            for tag in self.compiler.tags:
                file.write(tag)


def main(argv):
    path = argv[1]
    if path.endswith('.jack'):
        files = [path]
    else:
        files = [path + '/' + f for f in os.listdir(path) if f.endswith(
            '.jack')]
    for file in files:
        output_name = file.replace('.jack', '.xml')
        tokenizer = JackTokenizer(file)
        tokenizer.open_input_file(file)
        tokenizer.init_tokens()
        compiler = CompilationEngine(tokenizer)
        compiler.compile_class()
        analyzer = JackAnalyzer(compiler, output_name)
        analyzer.write_output()


if __name__ == '__main__':
    main(sys.argv)